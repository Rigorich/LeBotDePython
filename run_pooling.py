import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from dtb.settings import DEBUG
from tgbot.handlers.dispatcher import run_pooling

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO if not DEBUG else logging.DEBUG
    )
    run_pooling()
