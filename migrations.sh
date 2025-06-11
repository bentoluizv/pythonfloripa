#!/bin/sh

set -e

echo "=============================="
echo " Executando migrations"
echo " Data: $(date)"
echo "=============================="

echo "🗂️  Verificando versão atual do Alembic..."
alembic current || echo "⚠️ Nenhuma versão aplicada ainda."

echo "🛠️  Aplicando migrações pendentes com Alembic..."
alembic upgrade head

echo "✅ Migrações aplicadas com sucesso."
echo "=============================="
