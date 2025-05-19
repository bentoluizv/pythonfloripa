#!/bin/sh

set -e

echo "=============================="
echo " Inicializando aplicação FastAPI"
echo " Data: $(date)"
echo "=============================="

echo "🗂️  Verificando versão atual do Alembic..."
alembic current || echo "⚠️ Nenhuma versão aplicada ainda."

echo "🛠️  Aplicando migrações pendentes com Alembic..."
alembic upgrade head

echo "✅ Migrações aplicadas com sucesso."
echo "=============================="

echo "🚀 Iniciando o servidor Uvicorn..."
exec uvicorn src.app:app --host 0.0.0.0 --port 8000

echo "👋 Aplicação iniciada com sucesso."
echo "=============================="
