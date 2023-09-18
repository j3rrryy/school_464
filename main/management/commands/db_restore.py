from django.core.management.base import BaseCommand, CommandError

from main.utils import db_restore


class Command(BaseCommand):
    help = 'run to restore the db from your backup'

    def add_arguments(self, parser):
        parser.add_argument('backup_name', type=str,
                            help='The name of the backup file to restore.')

    def handle(self, *args, **options):
        self.stdout.write('Starting the database restoration process...')
        try:
            db_restore(options['backup_name'])
            self.stdout.write(f"Database and media files are restored successfully from {options['backup_name']}.")
        except Exception as error:
            raise CommandError(f"Failed to restore the database from {options['backup_name']}: {str(error)}")