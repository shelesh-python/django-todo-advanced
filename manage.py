#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')

    try:
        from django.core.management import execute_from_command_line
        import django
        django.setup()   # 👈 MOST IMPORTANT LINE
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc

    # ✅ AUTO CREATE ADMIN (SAFE PLACE)
    from django.contrib.auth import get_user_model

    User = get_user_model()

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_email = os.getenv("ADMIN_EMAIL", "")

    if admin_username and admin_password:
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                password=admin_password,
                email=admin_email
            )
            print("✅ Admin user auto-created")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
