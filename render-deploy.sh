#!/bin/bash
set -e  # Encerra o script ao primeiro erro

# Executa as migrações do banco de dados com Flask-Migrate
flask --app src.app db upgrade

# Inicia o servidor com Gunicorn
exec gunicorn src.wsgi:app
