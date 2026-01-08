#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

from django.contrib.auth import get_user_model

User = get_user_model()

if os.getenv("ADMIN_USERNAME") and os.getenv("ADMIN_PASSWORD"):
    username = os.getenv("shelesh")
    password = os.getenv("123shelesh##")
    email = os.getenv("sheleshc87@gmail.com", "")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )
        print("✅ Admin user created automatically")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
