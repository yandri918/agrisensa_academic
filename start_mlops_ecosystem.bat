@echo off
echo ==========================================
echo    STARTING AGRISENSA MLOPS THESIS PROJECT
echo ==========================================

echo [1/2] Launching MLOps Backend API (Port 8080)...
start "AgriSensa MLOps API" cmd /k "cd mlops_backend && "C:\Users\yandr\OneDrive\Desktop\agrisensa-api\agrisensa-mlops-api\venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload"

echo [2/2] Launching Thesis Dashboard (Port 8511)...
start "AgriSensa Thesis Frontend" cmd /k "cd thesis_frontend && "C:\Users\yandr\OneDrive\Desktop\agrisensa-api\agrisensa-mlops-api\client_venv\Scripts\python.exe" -m streamlit run Home.py --server.port 8511"

echo.
echo ==========================================
echo    ALL SYSTEMS DEPLOYED SUCCESSFULLY
echo ==========================================
echo.
echo Access the Dashboard at: http://localhost:8511
pause
