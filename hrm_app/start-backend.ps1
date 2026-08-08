# Start the FastAPI backend on port 8010 (handles the '&' folder name safely)
Set-Location "$PSScriptRoot\backend"
& "$PSScriptRoot\..\venv\Scripts\Activate.ps1"
python -m uvicorn app.presentation.main:app --port 8010 --reload
