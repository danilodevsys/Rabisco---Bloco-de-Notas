@echo off
echo === Instalando o Chocolatey (requer permissões de administrador) ===

powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"

if %errorlevel% neq 0 (
    echo ❌ Falha ao instalar o Chocolatey.
) else (
    echo ✅ Chocolatey instalado com sucesso!
)
pause
