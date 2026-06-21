Write-Host "⚠️ INICIANDO PROTOCOLO DE EMERGENCIA ⚠️"
Write-Host "Estos son tus puntos de restauración seguros disponibles:"
git tag --list "backup_*" | Sort-Object -Descending | Select-Object -First 5

Write-Host ""
$PUNTO_ELEGIDO = Read-Host "Escribe el nombre EXACTO del punto al que quieres regresar (ej. backup_20260620_161256)"

if (git tag --list | Select-String -Pattern "^$PUNTO_ELEGIDO$") {
    Write-Host "Revertiendo el código a $PUNTO_ELEGIDO..."
    # Forzamos la rama main a volver a ese punto exacto
    git reset --hard "$PUNTO_ELEGIDO"
    git push -f origin main
    Write-Host "✅ ¡Código revertido con éxito!"
    Write-Host "Railway detectará este push y redesplegará tu proyecto con la versión que funcionaba."
} else {
    Write-Host "❌ Error: El punto de restauración '$PUNTO_ELEGIDO' no existe. Ejecución cancelada."
}
