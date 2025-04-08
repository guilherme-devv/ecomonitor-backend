#!/bin/bash
set -e

echo "::: Iniciando configuração do Django :::"

until python manage.py migrate 2>&1; do
  echo "Aguardando banco de dados..."
  sleep 3
done

python manage.py collectstatic --noinput --clear

echo "::: Configuração concluída com sucesso! :::"

exec "$@"
