
# Model Card: XGBoost Relevancy Predictor

**Version:** v1.0  
**Date:** 2025-11-17  
**Owner:** Data & AI Academy  

## Data
- **Source:** QWS dataset ver 1.0
- **Features:** Response Time, Availability, Throughput, Successability, Reliability, Compliance, Documentation
- **Target:** WsRF: Web Service Relevancy Function (%)
- **Train/Test Split:** 80/20 (Train: 291 rows, Test: 73 rows)

## Model
- **Type:** XGBoost Regressor
- **Hyperparameters:** n_estimators=300, max_depth=6, learning_rate=0.1, subsample=0.8
- **Pipeline:** Imputer (median) + Model

## Performance
- **RMSE:** 1.66
- **MAE:** 1.80
- **R²:** 0.958

## Files
- **Model:** models/regression/best_xgb_pipeline.pkl
- **Metrics:** metrics.json

## Limitations
- Assumes QoS metrics are stable; may underperform on unseen service types.

## Intended Use
- Predict Web Service Relevancy for ranking and selection.

## Ethical Considerations
- Ensure predictions are not used for discriminatory service filtering.
