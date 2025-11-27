# Regression Model Evaluation Report

## Metrics
|    | Model            |    RMSE |   RMSE_std |     MAE |   MAE_std |         R² |   R²_std |
|---:|:-----------------|--------:|-----------:|--------:|----------:|-----------:|---------:|
|  0 | LinearRegression | 7.86955 |   10.5562  | 4.46456 |   4.27608 | -0.425485  | 2.54392  |
|  1 | RandomForest     | 6.36631 |    2.42768 | 5.26948 |   1.85085 |  0.449872  | 0.190881 |
|  2 | XGBoost          | 7.83578 |    1.88315 | 6.47227 |   1.91578 |  0.0261546 | 0.485539 |

## Drift Analysis
|    | Feature        |       PSI | PSI_Interpretation   |   KS_Statistic |   KS_p_value |
|---:|:---------------|----------:|:---------------------|---------------:|-------------:|
|  4 | Reliability    | 1.90517   | Significant drift    |      0.122644  |     0.72187  |
|  2 | Throughput     | 0.95647   | Significant drift    |      0.068838  |     0.997119 |
|  3 | Successability | 0.9407    | Significant drift    |      0.107969  |     0.845488 |
|  1 | Availability   | 0.598314  | Significant drift    |      0.0632307 |     0.999162 |
|  6 | Documentation  | 0.440201  | Significant drift    |      0.206872  |     0.1406   |
|  0 | Response Time  | 0.190055  | Moderate drift       |      0.146266  |     0.508647 |
|  5 | Compliance     | 0.0669367 | No drift             |      0.10964   |     0.832711 |

### Drift Interpretation

- **PSI > 0.25** indicates significant drift. Five features show major drift: Reliability, Throughput, Successability, Availability, and Documentation.
- Response Time shows moderate drift, while Compliance remains stable.
- KS p-values > 0.05 suggest shape differences are not statistically significant, but PSI captures magnitude shifts.

## Drift Plots (Top 3 Features)
![Drift for Reliability](artifacts_regression/rmance plots)![Drift for Throughput](artifacts_regression/rmance plots)![Drift for Successability](artifacts_regression/rmance plots)## Model Performance Plots
!Linear Regression Tuned Pred vs Actual
!Random Forest Tuned Pred vs Actual
!XGBoost Tuned Pred vs Actual
