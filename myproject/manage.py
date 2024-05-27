#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import shutil

def clear_media():
    media_dirs = ['media/encodings', 'media/videos']
    for media_dir in media_dirs:
        if os.path.exists(media_dir):
            shutil.rmtree(media_dir)
            os.makedirs(media_dir)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    clear_media()  # 서버 시작 전에 미디어 폴더를 정리합니다.
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)



def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
