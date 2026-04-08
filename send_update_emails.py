"""
TRADEWISE ONE-TIME PROFILE UPDATE EMAILS
Run this file to send update links to all users without phone numbers
"""

import os
import sys
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Email content
SUBJECT = "📝 ONE-TIME ACTION: Complete Your TradeWise Profile"
UPDATE_LINK = "https://tradewise-hub.com/update-profile/"

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Complete Your Profile - TradeWise</title>
<style>
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#2c3e50,#3498db);margin:0;padding:40px 20px}
.container{max-width:550px;margin:0 auto;background:white;border-radius:15px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
.header{background:linear-gradient(135deg,#2c3e50,#3498db);color:white;padding:30px;text-align:center}
.header h2{margin:0;font-size:1.8rem}
.content{padding:30px}
.warning{background:#fff3cd;border-left:4px solid #ffc107;padding:15px;margin-bottom:25px;border-radius:8px}
.btn{display:inline-block;background:linear-gradient(135deg,#3498db,#2c3e50);color:white;padding:14px 30px;text-decoration:none;border-radius:50px;font-weight:bold;margin:20px 0}
.footer{background:#f8f9fa;padding:20px;text-align:center;font-size:0.8rem;color:#7f8c8d}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h2>📝 Complete Your Profile</h2>
</div>
<div class="content">
<p>Dear <strong>{first_name}</strong>,</p>
<p>We noticed your TradeWise profile is missing important information.</p>
<div class="warning">
<strong>⚠️ One-Time Action Required:</strong> Please update your phone number to continue.
</div>
<p><strong>What you need to do:</strong></p>
<ul>
<li>📱 Enter your <strong>phone number</strong> (required)</li>
<li>🔐 Optionally change your <strong>password</strong></li>
</ul>
<div style="text-align:center;">
<a href="{update_link}" class="btn">🔑 UPDATE YOUR PROFILE NOW</a>
</div>
<p>This is a <strong>ONE-TIME</strong> process. After updating, you're all set!</p>
<p><strong>No login required</strong> - Just enter your email and phone number.</p>
</div>
<div class="footer">
<p>Need help? <a href="mailto:support@tradewise-hub.com">support@tradewise-hub.com</a></p>
<p>© 2026 TradeWise. All rights reserved.</p>
</div>
</div>
</body>
</html>"""

PLAIN_TEMPLATE = """TRADEWISE - ONE-TIME PROFILE UPDATE REQUIRED

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

Need help? Reply to this email.

Best regards,
TradeWise Team
https://tradewise-hub.com"""

def send_email(to_email, first_name):
    """Send email to single user"""
    try:
        # Create HTML content
        html_content = HTML_TEMPLATE.format(first_name=first_name, update_link=UPDATE_LINK)
        plain_content = PLAIN_TEMPLATE.format(first_name=first_name, update_link=UPDATE_LINK)
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"TradeWise Support <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = SUBJECT
        
        # Attach parts
        msg.attach(MIMEText(plain_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
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