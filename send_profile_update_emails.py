"""
TRADEWISE ONE-TIME PROFILE UPDATE NOTIFICATION - SIMPLE VERSION
Sends plain text emails to users without phone numbers
"""

import os
import django
import smtplib
from email.mime.text import MIMEText

# ✅ CORRECT PROJECT NAME
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dict.settings')

django.setup()

from myapp.models import Tradeviewusers
from django.db import models
import time

# ================= YOUR GMAIL CONFIG =================
GMAIL_USER = "theofficialtradewise@gmail.com"
APP_PASSWORD = "nmwygxenkrmagybb"
# =====================================================

print("\n" + "=" * 70)
print("🚀 TRADEWISE ONE-TIME PROFILE UPDATE NOTIFICATION")
print("=" * 70)

# Get users without phone numbers
users_without_phone = Tradeviewusers.objects.filter(
    models.Q(phone__isnull=True) | models.Q(phone='')
)

total_users = users_without_phone.count()
print(f"📊 Users to notify: {total_users}\n")

def send_simple_email(to_email, first_name):
    """Send plain text email"""
    try:
        subject = "📝 ONE-TIME ACTION: Complete Your TradeWise Profile"
        
        message = f"""Dear {first_name},

We noticed your TradeWise profile is missing important information.

ACTION REQUIRED (ONE-TIME):
---------------------------
Click the link below to update your profile:
https://tradewise-hub.com/force-profile-update/

WHAT YOU NEED TO DO:
--------------------
1. Click the link above
2. Enter your phone number (required)
3. Optionally change your password
4. Click update - you're done!

This is a ONE-TIME process. After updating, you'll never see this again.

Need help? Reply to this email.

Best regards,
TradeWise Support Team
https://tradewise-hub.com"""

        # Create message
        msg = MIMEText(message, 'plain')
        msg['From'] = f"TradeWise Support <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"   Error: {str(e)[:60]}")
        return False

# Test connection first
print("🔌 Testing Gmail connection...")
try:
    test_server = smtplib.SMTP('smtp.gmail.com', 587)
    test_server.starttls()
    test_server.login(GMAIL_USER, APP_PASSWORD)
    test_server.quit()
    print("✅ Gmail connection successful!\n")
except Exception as e:
    print(f"❌ Gmail connection failed: {e}")
    print("\n💡 TROUBLESHOOTING:")
    print("1. Make sure you're using an App Password, not your regular Gmail password")
    print("2. Go to: https://myaccount.google.com/apppasswords")
    print("3. Generate a new app password for 'Mail'")
    print("4. Update APP_PASSWORD in this script")
    exit()

# Send emails
print("📨 SENDING EMAILS...")
print("-" * 70)

sent_count = 0
error_count = 0
skip_count = 0

for i, user in enumerate(users_without_phone, 1):
    # Skip system account
    if user.email == 'system@tradewise.com':
        skip_count += 1
        print(f"[{i:3d}/{total_users}] ⏭️  Skipping system account: {user.email}")
        continue
    
    print(f"[{i:3d}/{total_users}] Sending to: {user.email[:35]:35}", end=" ")
    
    if send_simple_email(user.email, user.first_name):
        sent_count += 1
        print("✅ Sent")
    else:
        error_count += 1
        print("❌ Failed")
    
    # Small delay between emails
    time.sleep(1)

# Final Summary
print("\n" + "=" * 70)
print("📊 FINAL REPORT")
print("=" * 70)
print(f"✅ Successfully sent: {sent_count}")
print(f"❌ Failed: {error_count}")
print(f"⏭️  Skipped: {skip_count}")
print(f"📧 Total users: {total_users}")
print("=" * 70)

if sent_count > 0:
    print(f"\n🎉 Successfully sent {sent_count} profile update notifications!")
    print("🔗 Update link: https://tradewise-hub.com/force-profile-update/")
else:
    print("\n⚠️ No emails were sent. Please check your Gmail configuration.")
    print("\n💡 FIX: Generate a new App Password:")
    print("   1. Go to https://myaccount.google.com/apppasswords")
    print("   2. Select 'Mail' and 'Windows Computer'")
    print("   3. Copy the 16-character password")
    print("   4. Update APP_PASSWORD in this script")