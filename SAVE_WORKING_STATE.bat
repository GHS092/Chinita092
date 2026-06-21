@echo off
echo ========================================================
echo       SISTEMA DE RESPALDO - HERMES EVALUATOR
echo ========================================================
echo.
echo Esto guardara el estado actual de tu proyecto como una version
echo segura en la nube (GitHub) para que puedas volver a ella 
echo si algo se rompe en el futuro.
echo.
set /p desc="Ingresa una breve descripcion de este respaldo (ej: arregle la interfaz): "

echo.
echo Guardando el estado actual...
git add .
git commit -m "backup: %desc%"
git push origin main

echo.
echo ========================================================
echo RESPALDO GUARDADO CON EXITO.
echo ========================================================
pause
