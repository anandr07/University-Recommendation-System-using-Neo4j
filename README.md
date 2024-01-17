# University Recommendation System using Neo4j
Built a recommendation system for Recommending Similar Universities. 

![image](https://github.com/anandr07/University-Recommendation-System/assets/66896800/607279e9-1ba7-4c3c-9994-33a128c34cbb)

## Introduction
- Leveraging NEO4J, we aim to revolutionize higher education by offering tailored university recommendations, unlocking every student's potential for a transformative educational future.
- Traditional university recommendation systems, often static and one-size-fits-all, fail to meet individual student needs and aspirations.
- NEO4J's graph database reimagines higher education by enabling highly personalized, context-aware university recommendations, transforming the educational landscape.

## Recommendation systems
- Handling Complex Relationships
- Dynamic and Real-Time
- Personalized Recommendations
- Visualizing Recommendations
- Data Accuracy and Completeness

## Why Neo4j?
- Graph Database Architecture
- Flexible Query Language (Cypher)
- Performance Advantage (efficient traversal & graph algorithms)
- Intuitive Data Model
- Compatibility with Python

## Dataset

The dataset contains information about educational institutions in USA, with various columns providing details about rankings, enrollment, location, and other relevant metrics.

Column Explanations:

1. act-avg: Average ACT scores for admitted students.
2. sat-avg: Average SAT scores for admitted students.
3. enrollment: Total student enrollment.
4. city: Location city of the institution.
5. zip: ZIP code of the institution's location.
6. acceptance-rate: Percentage of applicants accepted.
7. percent-receiving-aid: Percentage of students receiving financial aid.
8. cost-after-aid: Cost for students after receiving financial aid.
9. state: State where the institution is located.
10. hs-gpa-avg: Average high school GPA of admitted students.
11. rankingDisplayRank: Displayed rank in rankings.
12. businessRepScore: Reputation score for the business department.
13. tuition: Tuition fees for students.
14. engineeringRepScore: Reputation score for the engineering department.
15. displayName: Name used for display purposes.
16. institutionalControl: Control of the institution (e.g., public, private).

Source : Kaggle
Number of Rows : 311 
Number of Columns: 39

## Data Pre-Processing 
- Dropping the unnecessary Columns
- Handling the Missing Values

## Universities Graph in Neo4j

![image](https://github.com/anandr07/University-Recommendation-System/assets/66896800/05bf809a-66a2-4820-9024-d004634bb3d3)

The image above shows a network of universities. The nodes represent the universities having properties such as acceptance rate, average act score, average sat score, average gpa, city, state, etc. The edges between the nodes named as 'Similarity_edge' represent relationships between the universities. The similarity score between the universities is calculated based on various criteria such as ACT scores, SAT scores, GPA, Acceptance Rate, and reputation scores likeBusiness Reputation Score and Engineering Reputation Score by calculating the Euclidean Distance between these features. The image below shows the euclidean distance between the John Hopkins and Northwestern universities. 

![image](https://github.com/anandr07/University-Recommendation-System/assets/66896800/e5ee9ba9-d14f-438d-90df-a0fc3a466f9b)

## Model - K-Nearest Neighbors algorithm
K-Nearest Neighbors (KNN) is a machine learning algorithm used for classification and regression tasks. This algorithm is employed to recommend the top five similar universities based on the similarity score.

## Flask
- Ease of Setup and Flexibility
- Integration with Neo4j
- User Interface and Visualization
- Scalability and Deployment

## Input Screen

![image](https://github.com/anandr07/University-Recommendation-System/assets/66896800/0dbbe709-9102-400d-bbcd-30f22f9b1d41)

## Output Screen 

![image](https://github.com/anandr07/University-Recommendation-System/assets/66896800/cda09ebd-1855-4522-9489-87034b5927d3)
