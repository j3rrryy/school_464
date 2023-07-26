import os
import glob
import shutil
from zipfile import ZipFile
from distutils.dir_util import copy_tree
from datetime import datetime

from django.core.management import call_command
from yadisk import YaDisk
from yadisk.exceptions import PathNotFoundError

from school_464.settings import env, MEDIA_ROOT, BACKUP_ROOT


def yadisk_setup():
    """
    Get a YaDisk object, check the token
    and create a folder for backups if not exists.
    """

    yadisk = YaDisk(token=env('YADISK_TOKEN'))

    # checks if the token is valid
    if not yadisk.check_token():
        print('TOKEN IS NOT VALID!')

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
    call_command('loaddata', 'backups/database.json')

    # remove used file
    os.remove(os.path.join(BACKUP_ROOT, 'database.json'))

    # remove existing files in the media folder
    for filename in os.listdir(MEDIA_ROOT):
        file_path = os.path.join(MEDIA_ROOT, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # copy new files
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

    backup_name = f'backup-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
    backup_path = os.path.join(BACKUP_ROOT, backup_name)
    media_path = os.path.join(backup_path, 'media')

    # create the backup folder
    os.mkdir(backup_path)

    # create the db backup file
    call_command(
        'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '--exclude=contenttypes',
        '--exclude=admin.logentry',
        '--indent=4',
        f'--output=backups/{backup_name}/database.json'
    )

    yadisk = yadisk_setup()

    # create folder for media files
    os.mkdir(media_path)

    # copy media files to the backup folder
    copy_tree(MEDIA_ROOT, media_path)

    # archive the backup folder
    shutil.make_archive(backup_path, 'zip', backup_path)

    # delete the unarchived backup folder
    shutil.rmtree(backup_path)

    # upload the backup folder
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
        restore_backup(backup)
    else:
        yadisk = yadisk_setup()

        try:
            # try to download the backup from
            # Yandex Disk to the local folder
            yadisk.download(f'/backups/{backup_name}', backup)
            restore_backup(backup)
        except PathNotFoundError:
            raise FileNotFoundError
