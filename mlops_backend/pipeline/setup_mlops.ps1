# 🛰️ AgriSensa MLOps Setup Script (DVC + MLflow + DagsHub)
# Run this script to configure DVC remote and MLflow tracking environments.

param(
    [string]$Username = "",
    [string]$Token = "",
    [string]$RepoName = "agrisensa_mlops"
)

# 1. Read from .env if variables are not provided as parameters
$envFile = "../.env"
if (Test-Path $envFile) {
    Write-Host "Reading configurations from .env..." -ForegroundColor Cyan
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $name = $Matches[1].Trim()
            $value = $Matches[2].Trim().Trim('"').Trim("'")
            if ($name -eq "DAGSHUB_USERNAME" -and $Username -eq "") { $Username = $value }
            if ($name -eq "DAGSHUB_TOKEN" -and $Token -eq "") { $Token = $value }
            if ($name -eq "DAGSHUB_REPO" -and $RepoName -eq "agrisensa_mlops") { $RepoName = $value }
        }
    }
}

if ([string]::IsNullOrEmpty($Username) -or [string]::IsNullOrEmpty($Token)) {
    Write-Error "Username and Token must be provided! Please set DAGSHUB_USERNAME and DAGSHUB_TOKEN in .env or pass them as parameters."
    exit 1
}

Write-Host "Setting up MLOps configuration for repository: $Username/$RepoName" -ForegroundColor Green

# 2. Initialize DVC
Write-Host "Step 1: Initializing DVC..." -ForegroundColor Cyan
dvc init --force

# 3. Setup DVC Remote Storage to DagsHub
Write-Host "Step 2: Configuring DagsHub DVC remote storage..." -ForegroundColor Cyan
$dvcRemoteUrl = "https://dagshub.com/$Username/$RepoName.dvc"
dvc remote add -d origin $dvcRemoteUrl --force
dvc remote modify origin auth basic
dvc remote modify origin user $Username
dvc remote modify origin password $Token

# 4. Save tracking variables to environment file or output instructions
Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "🎉 MLOps Pipeline Setup Complete!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host "DVC Remote configured to: $dvcRemoteUrl"
Write-Host "Untuk mengirim dataset ke DagsHub, jalankan:"
Write-Host "  dvc add data/raw/yield.csv"
Write-Host "  git add data/raw/yield.csv.dvc .gitignore"
Write-Host "  dvc push -r origin"
Write-Host "`nUntuk melakukan training pipeline via DVC, jalankan:"
Write-Host "  dvc repro"
Write-Host "`nUntuk tracking MLflow, pastikan env variables berikut aktif:"
Write-Host "  `$env:MLFLOW_TRACKING_URI = 'https://dagshub.com/$Username/$RepoName.mlflow'"
Write-Host "  `$env:MLFLOW_TRACKING_USERNAME = '$Username'"
Write-Host "  `$env:MLFLOW_TRACKING_PASSWORD = 'YOUR_DAGSHUB_TOKEN'"
Write-Host "==================================================" -ForegroundColor Green
