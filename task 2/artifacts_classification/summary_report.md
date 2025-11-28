# Classification Model Evaluation Report

## Metrics
|    | Model                    |   Accuracy |   Accuracy_std |       F1 |   F1_std |   Precision |   Precision_std |   Recall |   Recall_std |      AUC |   AUC_std |
|---:|:-------------------------|-----------:|---------------:|---------:|---------:|------------:|----------------:|---------:|-------------:|---------:|----------:|
|  0 | LogisticRegression_Tuned |   0.552381 |       0.220415 | 0.499365 | 0.236587 |    0.499206 |        0.287204 | 0.552381 |     0.220415 | 0.808333 |  0.136253 |
|  1 | RandomForest_Tuned       |   0.547619 |       0.168359 | 0.503016 | 0.169377 |    0.509524 |        0.220401 | 0.547619 |     0.168359 | 0.8375   |  0.142156 |
|  2 | XGBoost_Tuned            |   0.419048 |       0.153012 | 0.373424 | 0.151622 |    0.357143 |        0.172608 | 0.419048 |     0.153012 | 0.698437 |  0.150533 |

## Drift Analysis
|    | Feature        |       PSI | PSI_Interpretation   |   KS_Statistic |   KS_p_value |
|---:|:---------------|----------:|:---------------------|---------------:|-------------:|
|  1 | Availability   | 1.55996   | Significant drift    |      0.113815  |     0.798721 |
|  3 | Successability | 1.45133   | Significant drift    |      0.1199    |     0.746071 |
|  2 | Throughput     | 0.93709   | Significant drift    |      0.0959198 |     0.924028 |
|  8 | Documentation  | 0.873396  | Significant drift    |      0.140778  |     0.556638 |
|  6 | Best Practices | 0.616145  | Significant drift    |      0.0835123 |     0.974861 |
|  0 | Response Time  | 0.378854  | Significant drift    |      0.141255  |     0.552432 |
|  7 | Latency        | 0.254779  | Significant drift    |      0.108566  |     0.840511 |
|  4 | Reliability    | 0.250942  | Significant drift    |      0.138034  |     0.58102  |
|  5 | Compliance     | 0.0993827 | No drift             |      0.0564304 |     0.999889 |

### Drift Interpretation

- **PSI > 0.25** indicates significant drift. Review top drifted features for potential retraining.
- Features with moderate drift may require monitoring.
- KS p-values > 0.05 suggest shape differences are not statistically significant, but PSI captures magnitude shifts.

## Drift Plots (Top 3 Features)
![Drift for Availability](artifacts_classification/Performance Plots)![Drift for Successability](artifacts_classification/Performance Plots)![Drift for Throughput](artifacts_classification/Performance Plots)## Model Performance Plots
![Performance for Logistic Regression Tuned](artifacts_classification/Logistic Regression Tuned_confusion for Logistic Regression Tuned
!PR Curve for Logistic Regression Tuned
![Performance for Random Forest Tuned](artifacts_classification/Random Forest Tuned_confusion for Random Forest Tuned
!PR Curve for Random Forest Tuned
![Performance for XGBoost Tuned](artifacts_classification/XGBoost Tuned_confusion for XGBoost Tuned
!PR Curve for XGBoost Tuned
