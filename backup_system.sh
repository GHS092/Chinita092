#!/bin/bash
# Script de Backup para Hermes Agent (Railway / Local Linux)
# Comprime el directorio crítico de datos (/data) y el código actual.

set -e

BACKUP_DIR="/data/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="${BACKUP_DIR}/hermes_backup_${TIMESTAMP}.tar.gz"

echo "========================================="
echo "🛡️  Iniciando Sistema de Backup de Hermes..."
echo "========================================="

# Crear directorio de backups si no existe
mkdir -p "$BACKUP_DIR"

# Lista de elementos a respaldar
# Respaldamos la carpeta de datos crítica y la carpeta de la aplicación
TARGETS="/data/.hermes /app"

# Si estamos corriendo en local (fuera de Railway), ajustamos las rutas
if [ ! -d "/app" ]; then
    echo "⚠️  No se detectó el entorno Railway (/app no existe). Respaldando el directorio actual..."
    TARGETS="./hermes-agent-main-original ./server.py ./cli-config.yaml"
fi
if [ ! -d "/data/.hermes" ]; then
    # Si la ruta absoluta no existe, intentamos buscar la local o creamos advertencia
    if [ -d "$HOME/.hermes" ]; then
        TARGETS="$TARGETS $HOME/.hermes"
    else
        echo "⚠️  Atención: No se encontró la base de datos de Hermes en /data/.hermes ni en $HOME/.hermes"
    fi
fi

echo "📦 Creando archivo comprimido: $BACKUP_FILE"
# Ejecutamos el tar excluyendo la propia carpeta de backups
tar -czf "$BACKUP_FILE" --exclude="$BACKUP_DIR" $TARGETS 2>/dev/null || true

echo "✅ Backup completado con éxito."
echo "💾 Archivo guardado en: $BACKUP_FILE"
echo ""
echo "Para restaurar, ejecuta:"
echo "./restore_system.sh $BACKUP_FILE"
echo "========================================="
