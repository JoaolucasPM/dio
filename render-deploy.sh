#!/bin/bash
set -e  # Encerra o script em caso de erro

# Instala dependências do requirements.txt (sem reinstalar o pacote atual)
pip install --no-root

# Executa migrações do banco de dados
flask --app src.app db upgrade

# Inicia o servidor com Gunicorn apontando para o app WSGI
gunicorn src.wsgi:app
