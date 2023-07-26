from django.core.management.base import BaseCommand

from main.utils import db_restore


class Command(BaseCommand):
    help = 'run to restore the db from your backup'

    def add_arguments(self, parser):
        parser.add_argument('backup_name', type=str,
                            help='The name of the backup file to restore.')

    def handle(self, *args, **options):
        db_restore(options['backup_name'])
