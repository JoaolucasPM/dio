
#!/bin/bash
set -e  # Encerra o script ao primeiro erro

# Migrações com Flask-Migrate
flask --app src.app db upgrade

# Inicia com Gunicorn
gunicorn src.wsgi:app
