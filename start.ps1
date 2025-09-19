# Usage: Right-click -> Run with PowerShell (or execute in a PowerShell window)
param(
  [int]$Port = 8000,
  [string]$BindHost = "0.0.0.0"
)

$ErrorActionPreference = "Stop"

# Ensure we're running from the script directory
Set-Location -Path $PSScriptRoot

function Ensure-Venv($PythonTag) {
  $venv = Join-Path $PSScriptRoot ".venv"
  $activate = Join-Path $venv "Scripts/Activate.ps1"
  if (!(Test-Path $activate)) {
    Write-Host "Creating virtual environment with Python $PythonTag..." -ForegroundColor Cyan
    & py -$PythonTag -m venv $venv
  }
  return $activate
}

# Prefer Python 3.11 for SQLModel + Pydantic v1 compatibility
$activate = $null
try {
  $activate = Ensure-Venv "3.11"
} catch {
  Write-Warning "Python 3.11 not found via 'py -3.11'. Falling back to default 'py -3'. Consider installing Python 3.11 for best compatibility: https://www.python.org/downloads/release/python-3110/"
  $activate = Ensure-Venv "3"
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
. $activate

Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install --upgrade pip > $null
pip install -r (Join-Path $PSScriptRoot "requirements.txt")

Write-Host ("Starting server on http://{0}:{1}" -f $BindHost, $Port) -ForegroundColor Green
python -m uvicorn app.main:app --reload --host $BindHost --port $Port --app-dir "$PSScriptRoot"
