from datetime import datetime, timedelta
import pytz
from django.core.management import BaseCommand
from accounts.models import OtpCode


class Command(BaseCommand):
    help = 'Remove all expired otp code'

    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('Removed expired otp')
