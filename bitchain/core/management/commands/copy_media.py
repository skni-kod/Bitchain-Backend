# /bitchain/bitchain/management/commands/copy_media.py

import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Copy media files to another directory'

    def handle(self, *args, **options):
        source_dir = os.path.abspath(os.path.join(settings.BASE_DIR, 'media'))
        destination_dir = os.path.abspath(os.path.join(settings.MEDIA_ROOT, ))
        print('absSource:', source_dir)
        print('absDestination:', destination_dir)
        try:
            # Utwórz katalog docelowy, jeśli nie istnieje
            os.makedirs(destination_dir, exist_ok=True)
            
            # Skopiuj katalog źródłowy wraz z zawartością do katalogu docelowego
            shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)

            self.stdout.write(self.style.SUCCESS('Media files copied successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error copying media files: {str(e)}'))
