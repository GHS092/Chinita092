#!/bin/bash
# Script de Restauración para Hermes Agent (Railway / Local Linux)
# Restaura un backup previo de /data y /app

set -e

if [ -z "$1" ]; then
    echo "❌ Error: Debes especificar el archivo de backup a restaurar."
    echo "Uso: ./restore_system.sh /data/backups/hermes_backup_YYYY-MM-DD_HH-MM-SS.tar.gz"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Error: El archivo $BACKUP_FILE no existe."
    exit 1
fi

echo "========================================="
echo "⚠️  ADVERTENCIA: Iniciando Restauración de Sistema"
echo "Esto sobrescribirá la base de datos actual y el código."
echo "Restaurando desde: $BACKUP_FILE"
echo "========================================="

# Extraer el archivo tar.gz desde el directorio raíz (/) para respetar las rutas absolutas (/app, /data)
# Si estamos en local, se extraerá en la ruta relativa actual si el backup se hizo así
echo "📦 Extrayendo archivos..."
tar -xzf "$BACKUP_FILE" -C /

echo "✅ Restauración completada con éxito."
echo "🔄 Por favor, reinicia el servidor o el contenedor para aplicar los cambios."
echo "========================================="
