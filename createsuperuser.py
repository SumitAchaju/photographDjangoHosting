import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photographApi.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")


print(f"Creating superuser with username: {username}, email: {email}")
print("Please wait...")

if not username or not email or not password:
    raise ValueError(
        "Please set the environment variables: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD"
    )

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
