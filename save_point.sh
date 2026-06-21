#!/bin/bash
# save_point.sh
echo "Creando un punto de restauración seguro..."
PUNTO="backup_$(date +"%Y%m%d_%H%M%S")"

git add .
git commit -m "Punto de restauracion: Todo funcional ($PUNTO)" || true
git tag "$PUNTO"
git push origin main
git push origin "$PUNTO"

echo "✅ ¡Punto de restauración '$PUNTO' guardado en GitHub!"
echo "Si algo sale mal con los nuevos cambios, podrás volver a este punto usando ./revert_to_safe.sh"
