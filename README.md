# AgriSensa Thesis MLOps

This is a clean, academic-focused project directory tailored for a Master's (S2) thesis on **Scalable MLOps Architecture for Precision Agriculture**.

## Directory Structure
- `data/`: Raw and processed agricultural datasets (CSV/JSON).
- `models_registry/`: The centralized storage for trained ML models (.pkl files).
- `mlops_backend/`: FastAPI application serving the ML models as microservices.
- `thesis_frontend/`: Streamlit dashboard focusing purely on Predictive ML analysis and data visualization.

## How to Run Locally
Simply run the batch script provided in the root directory:
```bash
start_mlops_ecosystem.bat
```
This will launch both the backend API and the frontend dashboard.
