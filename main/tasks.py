import os
import glob

from celery import shared_task

from .utils import db_backup, yadisk_setup


@shared_task
def dbbackup_task():
    """
    Do a backup of the db and your files +
    upload it to Yandex Disk
    and delete an old backup +
    remove it from Yandex Disk.
    """

    # do a db backup
    db_backup()

    # delete an old db backup

    backups = glob.glob("backups/backup-*.zip")

    if len(backups) > 5:

        # the oldest backups are located at the beginning
        backups.sort(key=os.path.getctime)

        # get only backups for deletion
        oldest_backups = backups[:-5]

        # delete old backups
        for archive in oldest_backups:
            os.remove(archive)

        # delete the same backups from Yandex Disk
        yadisk = yadisk_setup()
        for archive in oldest_backups:
            archive_name = os.path.basename(archive)
            yadisk.remove(f'/backups/{archive_name}')
