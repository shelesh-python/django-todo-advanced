from django.apps import AppConfig
from django.contrib.auth.models import User
import os


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # Auto-create superuser on Render (Free plan workaround)
        username = os.getenv("shelesh")
        password = os.getenv("123shelesh##")
        email = os.getenv("sheleshc87@gmail.com")

        if username and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    password=password,
                    email=email
                )
                print("✅ Admin user created automatically")
