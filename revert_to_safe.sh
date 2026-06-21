#!/bin/bash
# revert_to_safe.sh
echo "⚠️ INICIANDO PROTOCOLO DE EMERGENCIA ⚠️"
echo "Estos son tus puntos de restauración seguros disponibles:"
git tag --list "backup_*" | sort -r | head -n 5

echo ""
read -p "Escribe el nombre EXACTO del punto al que quieres regresar (ej. backup_20260620_161256): " PUNTO_ELEGIDO

if git rev-parse "$PUNTO_ELEGIDO" >/dev/null 2>&1; then
    echo "Revertiendo el código a $PUNTO_ELEGIDO..."
    # Forzamos la rama main a volver a ese punto exacto
    git reset --hard "$PUNTO_ELEGIDO"
    git push -f origin main
    echo "✅ ¡Código revertido con éxito!"
    echo "Railway detectará este push y redesplegará tu proyecto con la versión que funcionaba."
else
    echo "❌ Error: El punto de restauración '$PUNTO_ELEGIDO' no existe. Ejecución cancelada."
fi
