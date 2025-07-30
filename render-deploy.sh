#!/bin/bash
set -e  # Encerra o script em caso de erro

# Instala dependências do requirements.txt
pip install -r requirements.txt

# Executa migrações do banco de dados (Flask-Migrate)
flask --app src.app db upgrade

# Inicia o servidor com Gunicorn apontando para o app WSGI
gunicorn src.wsgi:app
