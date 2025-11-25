
# Model Card: Classification Models Comparison
**Version:** v1.0  
**Date:** 2025-11-24  
**Owner:** Data & AI Academy  

## Data
- Source: QWS dataset (QoS metrics for web services)
- Target: Service Class (1-4)
- Preprocessing: Scaling, encoding

## Features
- Response Time, Availability, Throughput, Successability, Reliability, Compliance, Best Practices, Latency, Documentation

## Models and Performance
| Model                  | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|------------------------|----------|-----------|--------|----------|---------|
| LogisticRegression_Tuned | 0.7792 | 0.7829 | 0.8085 | 0.7794 | 0.9459 |
| RandomForest_Tuned | 0.7273 | 0.7503 | 0.7326 | 0.7294 | 0.9199 |
| XGBoost_Tuned | 0.7273 | 0.7503 | 0.7326 | 0.7294 | 0.9196 |

## Limitations
- May underperform on unseen distributions
- Sensitive to feature scaling

## Intended Use
- Predictive analytics for service classification
- Not for high-stakes decisions without human review.
