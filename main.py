#%%
##importing libraries
from flask import Flask, render_template, request
from neo4j import GraphDatabase
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)


# Define the Neo4j connection class
class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self._uri = uri
        self._user = user
        self._password = pwd
        self._driver = None

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        return self

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def query(self, query, parameters=None, db=None):
        assert self._driver is not None, "Driver not initialized!"
        session = self._driver.session(database=db) if db else self._driver.session()
        result = list(session.run(query, parameters))
        session.close()
        return result
    
#%%
# Load university data from CSV
import os

cwd = os.getcwd()
uni = pd.read_csv(cwd+'\\university_data.csv')

# Drop unnecessary columns
uni.drop(['primaryPhoto', 'primaryPhotoThumb', 'sortName', 
         'urlName', 'aliasNames', 'nonResponderText',
         'nonResponder', 'rankingSortRank', 'overallRank',
         'rankingRankStatus', 'xwalkId', 'primaryKey',
         'rankingNoteText','rankingNoteCharacter','rankingMaxPossibleScore',
         'rankingIsTied','ranking','schoolType','rankingType',
         'rankingDisplayName','region','isPublic'], axis=1, inplace=True)


# Handling missing values
columns_to_fill = ['act-avg', 'sat-avg', 'acceptance-rate','hs-gpa-avg','businessRepScore','engineeringRepScore','enrollment','rankingDisplayScore']
for column in columns_to_fill:
    mean_value = uni[column].mean()
    uni[column].fillna(mean_value, inplace=True)

uni[['percent-receiving-aid', 'cost-after-aid']] = uni[['percent-receiving-aid', 'cost-after-aid']].fillna(uni[['percent-receiving-aid', 'cost-after-aid']].median())

#%%
# Create a Neo4j connection
uri = "bolt://localhost:7687"
username = "neo4j"
password = "root@12345"
neo4j_conn = Neo4jConnection(uri, username, password).connect()

#%%
# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    college_name = request.form['college_name']

    # Get recommendations
    recommendations = get_recommendations(neo4j_conn, college_name)

    # Close Neo4j connection
    neo4j_conn.close()
    recommendations_data = recommendations.to_dict(orient='records')

    return render_template('index.html', college_name=college_name, recommendations=recommendations_data)
#%%
##Create relationships between universities based on similarity
similarity_query = '''
MATCH (u1:University), (u2:University)
WHERE id(u1) < id(u2)
WITH u1, u2,
     gds.similarity.euclidean(
         [u1.actAvg, u1.satAvg, u1.acceptanceRate, u1.hsGpaAvg, u1.rankingDisplayRank, u1.businessRepScore, u1.engineeringRepScore],
         [u2.actAvg, u2.satAvg, u2.acceptanceRate, u2.hsGpaAvg, u2.rankingDisplayRank, u2.businessRepScore, u2.engineeringRepScore]
     ) AS euclideanDistance
MERGE (u1)-[similarity:SIMILARITY_EDGE]->(u2)
ON CREATE SET similarity.euclideanDistance = euclideanDistance;
'''
neo4j_conn.query(similarity_query)

#%%
# Create the graph using gds.graph.project
graph_creation_query = """
// Check if the graph exists
CALL gds.graph.exists('myGraph') 
YIELD exists AS graphExists

// If the graph does not exist, create it
WITH 'myGraph' AS graphToCreate, graphExists
WHERE NOT graphExists
CALL gds.graph.project(graphToCreate, 'University', 'SIMILARITY_EDGE', {
  nodeProperties: ['actAvg', 'satAvg', 'acceptanceRate', 'hsGpaAvg', 'rankingDisplayRank', 'businessRepScore', 'engineeringRepScore']
}) YIELD graphName, nodeCount, relationshipCount
RETURN graphName, nodeCount, relationshipCount;
"""
neo4j_conn.query(graph_creation_query)
#%%
# Perform Min-Max scaling
scale_features_query = '''
MATCH (n)
WHERE n.scaledProperties IS NOT NULL
CALL gds.alpha.scaleProperties.mutate('myGraph', {
  nodeProperties: ['actAvg', 'satAvg', 'acceptanceRate', 'hsGpaAvg', 'rankingDisplayRank', 'businessRepScore', 'engineeringRepScore'],
  scaler: "MinMax",
  mutateProperty: "scaledProperties"
})
YIELD nodePropertiesWritten
RETURN nodePropertiesWritten;
'''

neo4j_conn.query(scale_features_query)
#%%
# Function to get recommendations using GDS KNN algorithm
def get_recommendations(connection, college_name):
    query = f"""
    CALL gds.knn.stream('myGraph', {{
        topK: 5,
        nodeProperties: ['actAvg', 'satAvg', 'acceptanceRate', 'hsGpaAvg', 'rankingDisplayRank', 'businessRepScore', 'engineeringRepScore'],
        randomSeed: 1337,
        concurrency: 1,
        sampleRate: 1.0,
        deltaThreshold: 0.0
    }})
    YIELD node1, node2, similarity
    WITH gds.util.asNode(node1) AS university1, gds.util.asNode(node2) AS university2, similarity

    // Use the parameter in the WHERE clause
    WHERE university1.name = $college_name

    RETURN university1.name AS University1, university2.name AS University2, similarity
    ORDER BY similarity DESCENDING, University1, University2;
    """
    parameters = {'college_name': college_name}
    result = connection.query(query, parameters)
    return pd.DataFrame(result)

#%%
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',port=8080)


#%%s






