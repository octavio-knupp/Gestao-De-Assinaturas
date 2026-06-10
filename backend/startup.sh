#!/bin/bash
# Instala dependências
pip install -r requirements.txt

# Executa migrations
python manage.py migrate

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Inicia o Django com Gunicorn
gunicorn config.wsgi:application
