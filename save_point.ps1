$PUNTO = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "Creando un punto de restauración seguro..."

git add .
git commit -m "Punto de restauracion: Todo funcional ($PUNTO)"
git tag $PUNTO
git push origin main
git push origin $PUNTO

Write-Host "✅ ¡Punto de restauración '$PUNTO' guardado en GitHub!"
Write-Host "Si algo sale mal con los nuevos cambios, podrás volver a este punto usando .\revert_to_safe.ps1"
