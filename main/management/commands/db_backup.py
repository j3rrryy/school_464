from django.core.management.base import BaseCommand, CommandError

from main.utils import db_backup


class Command(BaseCommand):
    help = 'run to create a db backup'

    def handle(self, *args, **options):
        self.stdout.write('Starting the database backup process...')
        try:
            db_backup()
            self.stdout.write('Database backup completed successfully.')
        except Exception as error:
            raise CommandError(f'Database backup failed: {str(error)}')
