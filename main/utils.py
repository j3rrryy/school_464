import os
import glob
import shutil
from zipfile import ZipFile
from distutils.dir_util import copy_tree
from datetime import datetime

from django.core.management import call_command
from yadisk import YaDisk
from yadisk.exceptions import PathNotFoundError

from .models import YandexDiskToken
from backend.settings import MEDIA_ROOT, BACKUP_ROOT


def yadisk_setup() -> YaDisk | None:
    """
    Get a YaDisk object, check the token
    and create a folder for backups if not exists.
    """

    if token := YandexDiskToken.objects.first():
        yadisk = YaDisk(token=token.token)
    else:
        print('THE TOKEN IS MISSING FROM THE DB!')
        return None

    # checks if the token is valid
    if not yadisk.check_token():
        print('THE TOKEN IS INVALID!')
        return None

    # create the backup folder if not exists
    if not yadisk.exists('/backups'):
        yadisk.mkdir('/backups')

    return yadisk


def restore_backup(backup_path: str):
    """
    Extract files from the backup
    and complete the restoration.
    """

    with ZipFile(backup_path) as backup:
        backup.extractall(BACKUP_ROOT)

    # restore the db
    print('Restoring the database...')
    call_command('flush', '--no-input')
    call_command('loaddata', 'backups/database.json')

    # remove used file
    os.remove(os.path.join(BACKUP_ROOT, 'database.json'))

    # remove existing files in the media folder
    for filename in os.listdir(MEDIA_ROOT):
        file_path = os.path.join(MEDIA_ROOT, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # copy new files
    print('Restoring media files...')
    for filename in os.listdir(os.path.join(BACKUP_ROOT, 'media')):
        src_file = os.path.join(BACKUP_ROOT, 'media', filename)
        dst_file = os.path.join(MEDIA_ROOT, filename)
        shutil.move(src_file, dst_file)

    # remove used folder
    shutil.rmtree(os.path.join(BACKUP_ROOT, 'media'))


def db_backup():
    """
    Do backup of the db and your files +
    upload it to Yandex Disk.
    """

    yadisk = yadisk_setup()
    backup_name = f'backup-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
    backup_path = os.path.join(BACKUP_ROOT, backup_name)
    media_path = os.path.join(backup_path, 'media')

    # create the backup folder
    os.mkdir(backup_path)

    # create the db backup file
    print('Creating the database backup file...')
    call_command(
        'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '--exclude=contenttypes',
        '--exclude=admin.logentry',
        '--indent=4',
        f'--output=backups/{backup_name}/database.json'
    )

    # create folder for media files
    os.mkdir(media_path)

    # copy media files to the backup folder
    print('Copying media files to the backup folder...')
    copy_tree(MEDIA_ROOT, media_path)

    # archive the backup folder
    shutil.make_archive(backup_path, 'zip', backup_path)

    # delete the unarchived backup folder
    shutil.rmtree(backup_path)

    if yadisk:
        # upload the backup folder
        print('Uploading the backup folder to Yandex Disk...')
        yadisk.upload(f'{backup_path}.zip',
                      f'/backups/{backup_name}.zip',
                      overwrite=True)


def db_restore(backup_name: str):
    """
    Restore files and the db using your backup file.
    """

    # path of backup file in the local folder
    backup = os.path.join(BACKUP_ROOT, backup_name)

    # search for backups in the local folder
    backups = glob.glob(os.path.join(BACKUP_ROOT, 'backup-*.zip'))

    if backup in backups:
        print('Restoring a backup from system files...')
        restore_backup(backup)
    else:
        yadisk = yadisk_setup()

        if yadisk:
            try:
                # try to download the backup from
                # Yandex Disk to the local folder
                print('Restoring a backup from Yandex Disk...')
                yadisk.download(f'/backups/{backup_name}', backup)
                restore_backup(backup)
            except PathNotFoundError:
                raise FileNotFoundError
        else:
            raise FileNotFoundError
