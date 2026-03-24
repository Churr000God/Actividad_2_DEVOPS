# Setup Maestro - Python Environment Configuration
# E:\Escuela\4to Semestre\Fundamentos Devops\Actividad-2\setup.ps1

Write-Host "Iniciando configuración del entorno virtual Python..." -ForegroundColor Cyan

# 1. Verificar versión de Python
$requiredVersion = "3.12.2"
$pythonVersion = python --version 2>$null

if ($pythonVersion -match $requiredVersion) {
    Write-Host "Versión de Python detectada: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "ADVERTENCIA: No se detectó Python $requiredVersion. Se intentará usar la versión disponible." -ForegroundColor Yellow
    if (-not $pythonVersion) {
        Write-Error "Python no está instalado o no está en el PATH."
        exit 1
    }
}

# 2. Crear entorno virtual
Write-Host "Creando entorno virtual en .venv..." -ForegroundColor Cyan
python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Error "Error al crear el entorno virtual."
    exit 1
}

# 3. Activar entorno virtual y actualizar pip
Write-Host "Actualizando pip e instalando dependencias..." -ForegroundColor Cyan
& ".\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. Verificar instalación
Write-Host "Verificando instalación de boto3..." -ForegroundColor Cyan
python -c "import boto3; print('Boto3 instalado correctamente. Versión:', boto3.__version__)"

Write-Host "Configuración completada con éxito." -ForegroundColor Green
