"""
TRADEWISE ONE-TIME PROFILE UPDATE EMAILS - PLAIN TEXT VERSION
Run this file to send update links to all users without phone numbers
"""

import os
import sys
import django
import smtplib
from email.mime.text import MIMEText

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dict.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from myapp.models import Tradeviewusers
from django.db import models

# ================= CONFIGURATION =================
GMAIL_USER = "theofficialtradewise@gmail.com"
APP_PASSWORD = "nmwygxenkrmagybb"
# =================================================

print("\n" + "=" * 70)
print("🚀 TRADEWISE PROFILE UPDATE EMAIL SENDER")
print("=" * 70)
print(f"📧 From: {GMAIL_USER}")
print("=" * 70)

# Get users without phone numbers
users_without_phone = Tradeviewusers.objects.filter(
    models.Q(phone__isnull=True) | models.Q(phone='')
).exclude(email='system@tradewise.com')

total_users = users_without_phone.count()
print(f"\n📊 Users without phone numbers: {total_users}")
print("=" * 70)

if total_users == 0:
    print("\n✅ No users found without phone numbers. Nothing to do.")
    sys.exit(0)

# Email content - PLAIN TEXT ONLY
SUBJECT = "ONE-TIME ACTION: Complete Your TradeWise Profile"
UPDATE_LINK = "https://tradewise-hub.com/update-profile/"

EMAIL_TEMPLATE = """
TRADEWISE - ONE-TIME PROFILE UPDATE REQUIRED

Dear {first_name},

We noticed your TradeWise profile is missing important information.

ONE-TIME ACTION REQUIRED:
-------------------------
Click the link below to update your profile:
{update_link}

WHAT YOU NEED TO DO:
--------------------
1. Enter your email address
2. Enter your phone number (required)
3. Optionally change your password
4. Click update - you're done!

No login required. This is a ONE-TIME process.

After you update your profile once, you will never see this again.

Need help? Reply to this email.

Best regards,
TradeWise Team
https://tradewise-hub.com
"""

def send_email(to_email, first_name):
    """Send plain text email to single user"""
    try:
        # Create plain text content
        content = EMAIL_TEMPLATE.format(first_name=first_name, update_link=UPDATE_LINK)
        
        # Create message
        msg = MIMEText(content, 'plain')
        msg['From'] = f"TradeWise Support <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = SUBJECT
        
        # Send
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"   Error: {str(e)[:80]}")
        return False

# ================= SEND EMAILS =================
print("\n📨 SENDING EMAILS...")
print("-" * 70)

sent = 0
failed = 0
failed_emails = []

for i, user in enumerate(users_without_phone, 1):
    print(f"[{i:3d}/{total_users}] {user.email[:35]:35}", end=" ")
    
    if send_email(user.email, user.first_name):
        sent += 1
        print("✅ Sent")
    else:
        failed += 1
        failed_emails.append(user.email)
        print("❌ Failed")

# ================= RESULTS =================
print("\n" + "=" * 70)
print("📊 FINAL REPORT")
print("=" * 70)
print(f"✅ Successfully sent: {sent}")
print(f"❌ Failed: {failed}")
print(f"📧 Total users: {total_users}")
print(f"🔗 Update link: {UPDATE_LINK}")

if failed_emails:
    print("\n📋 Failed emails:")
    for email in failed_emails[:10]:
        print(f"   • {email}")
    if len(failed_emails) > 10:
        print(f"   ... and {len(failed_emails) - 10} more")

print("\n" + "=" * 70)
print("🎉 DONE!")
print("=" * 70)