#!/bin/bash
set -e  # Encerra o script ao primeiro erro


# Executa as migrações do banco de dados com Flask-Migrate
python run flask --app src.app db upgrade
python run gunicorn src.wsgi:app
