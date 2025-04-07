#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser only if not exists
echo "from django.contrib.auth import get_user_model; \
      User = get_user_model(); \
      User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists() or \
      User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" \
      | python manage.py shell

exec "$@"
