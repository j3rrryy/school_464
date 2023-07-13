import os
import glob
from datetime import datetime

from django.core.management import call_command
from celery import shared_task


@shared_task
def dbbackup_task():
    """
    Do a database backup
    """
    call_command(
        'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '--exclude=contenttypes',
        '--exclude=admin.logentry',
        '--indent=4',
        f'--output=backup/database-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json'
    )


@shared_task
def dbbackup_cleanup_task():
    """
    Delete an old database backup
    """
    backup_files = glob.glob("backup/database-*.json")
    backup_files.sort(key=os.path.getctime)
    if len(backup_files) > 2:
        oldest_backup = backup_files[0]
        os.remove(oldest_backup)
