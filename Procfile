web: gunicorn ai_chatbot.wsgi && python manage.py makemigrations && python manage.py migrate --settings=ai_chatbot.settings.production && python manage.py runserver &&  python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn ai_chatbot.wsgi:application --bind 0.0.0.0:$PORT


