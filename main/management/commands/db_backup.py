from django.core.management.base import BaseCommand

from main.utils import db_backup


class Command(BaseCommand):
    help = 'run to create a db backup'

    def handle(self, *args, **options):
        db_backup()
