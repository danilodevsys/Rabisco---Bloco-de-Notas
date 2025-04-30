@echo off
REM === Build Rabisco (Windows, portável e sem console) ===

REM Limpeza
if exist build rmdir /s /q build
if exist dist\Rabisco rmdir /s /q dist\Rabisco
if exist Rabisco.spec del Rabisco.spec

REM Compilação com PyInstaller
pyinstaller --noconsole --windowed ^
--name Rabisco ^
--icon=assets\icons\logo_rabisco.ico ^
--add-data "assets;assets" ^
--add-data "src;src" ^
--paths src ^
--distpath dist ^
main.py

echo.
echo ===============================
echo ✅ Build finalizado com sucesso!
echo 📁 Verifique: dist\Rabisco
echo ===============================
pause
