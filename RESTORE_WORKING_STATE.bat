@echo off
echo ========================================================
echo       SISTEMA DE RESTAURACION - HERMES EVALUATOR
echo ========================================================
echo.
echo ADVERTENCIA: Esto borrara todos los cambios actuales que 
echo hayas hecho y restaurara el proyecto EXACTAMENTE a la version
echo estable y funcional.
echo.
set /p confirm=¿Estas seguro que deseas restaurar el sistema? (S/N): 

if /i "%confirm%" neq "S" (
    echo.
    echo Restauracion cancelada. No se modifico nada.
    pause
    exit /b
)

echo.
echo Restaurando a la version estable (v1.0-stable-working)...
git fetch --all
git reset --hard v1.0-stable-working
git clean -fd

echo.
echo ========================================================
echo RESTAURACION COMPLETADA CON EXITO.
echo El sistema ha vuelto a su estado funcional.
echo ========================================================
pause
