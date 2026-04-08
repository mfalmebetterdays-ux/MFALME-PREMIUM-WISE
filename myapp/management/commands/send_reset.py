from django.core.management.base import BaseCommand
from myapp.models import Tradeviewusers, Notification
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Command(BaseCommand):
    help = 'Send password reset emails'

    def handle(self, *args, **options):
        GMAIL_USER = "theofficialtradewise@gmail.com"
        APP_PASSWORD = "nmwygxenkrmagybb"
        
        users = Tradeviewusers.objects.all()
        self.stdout.write(f"Sending to {users.count()} users...")
        
        for user in users:
            # Your email logic here
            self.stdout.write(f"Sent to {user.email}")