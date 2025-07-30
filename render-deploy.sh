#!/bin/bash
set -e  # Encerra o script ao primeiro erro

# Instala as dependências do projeto
pip install -r requirements.txt

# Executa as migrações do banco de dados com Flask-Migrate
flask --app src.app db upgrade

# Inicia o servidor com Gunicorn apontando para o app WSGI
exec gunicorn src.wsgi:app
