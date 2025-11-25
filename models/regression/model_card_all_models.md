
# Model Card: Regression Models Comparison
**Version:** v1.0  
**Date:** 2025-11-24  
**Owner:** Data & AI Academy  

## Data
- **Source:** QWS dataset ver 1.0
- **Features:** Response Time, Availability, Throughput, Successability, Reliability, Compliance, Documentation
- **Target:** WsRF: Web Service Relevancy Function (%)
- **Train/Test Split:** 70/30

## Models and Performance
| Model             | RMSE   | MAE    | R²    |
|-------------------|--------|--------|-------|
| Linear Regression (Tuned) | 3.71 | 2.62 | 0.930 |
| Random Forest (Tuned) | 4.59 | 3.08 | 0.893 |
| XGBoost (Tuned) | 3.31 | 2.30 | 0.944 |

## Files
- **Models:** best_lr_pipeline.pkl, best_rf_pipeline.pkl, best_xgb_pipeline.pkl
- **Metrics:** Separate JSON/CSV files for each model

## Limitations
- Assumes QoS metrics are stable; may underperform on unseen service types.

## Intended Use
- Predict Web Service Relevancy for ranking and selection.

## Ethical Considerations
- Ensure predictions are not used for discriminatory service filtering.
