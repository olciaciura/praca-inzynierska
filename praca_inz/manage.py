#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from model.utils import load_model, predict

MODEL = load_model('./model/model.p')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'praca_inz.settings')
    # predict(MODEL, './model/photos/train/28.jpg')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    #TODO dodać ładowanie modelu  do zmiennej globalnej

if __name__ == '__main__':
    main()
