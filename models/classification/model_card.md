
# Model Card: Logistic Regression Tuned

## Model Details
- Algorithm: Logistic Regression Tuned
- Version: 1.0
- Framework: scikit-learn / XGBoost

## Data
- Source: Contains measurements of nine Quality of Service (QoS) per web service for 365 web services and includes two additional attributes: (a) a rank of web services based on our Web Service Relevancy Function (WsRF) and (b) a class which classifies web services based on their overall performance.


- Preprocessing: scaling, feature engineering

## Features
- Response Time, Availability, Throughput, Successability, Reliability, Compliance, Best Practices, Latency, Documentation

## Metrics
- Accuracy: 0.7123
- Precision: 0.7383
- Recall: 0.7506
- F1 Score: 0.7163
- ROC-AUC: 0.9299

## Limitations
- May underperform on unseen distributions
- Sensitive to feature scaling

## Intended Use
- Predictive analytics for [specific domain]
- Not for high-stakes decisions without human review.
