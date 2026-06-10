"""
TRADEWISE ONE-TIME PROFILE UPDATE NOTIFICATION
Sends beautiful HTML emails to users without phone numbers
"""

import os
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ CORRECT PROJECT NAME - YOUR PROJECT IS 'dict'
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
print("🚀 TRADEWISE ONE-TIME PROFILE UPDATE NOTIFICATION SYSTEM")
print("=" * 70)
print(f"📧 Sending from: {GMAIL_USER}")
print("=" * 70)

# Get users without phone numbers
users_without_phone = Tradeviewusers.objects.filter(
    models.Q(phone__isnull=True) | models.Q(phone='')
)

total_users = users_without_phone.count()
print(f"\n📊 Users WITHOUT phone numbers to notify: {total_users}")
print("=" * 70)

# Beautiful HTML Email Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Your Profile - TradeWise</title>
    <style>
        body {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 40px 20px;
        }
        .email-container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 14px 28px rgba(0,0,0,0.25);
        }
        .header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            padding: 40px 30px;
            text-align: center;
        }
        .tradewise-logo {
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
        }
        .header h1 {
            color: white;
            font-size: 1.8rem;
            margin-top: 10px;
        }
        .content {
            padding: 40px 30px;
            background: white;
        }
        .greeting {
            font-size: 1.2rem;
            color: #2c3e50;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .message {
            color: #34495e;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        .credentials-box {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
            border-left: 5px solid #3498db;
        }
        .credentials-box h3 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .credentials-box p {
            margin: 10px 0;
        }
        .credentials-box strong {
            color: #3498db;
        }
        .update-button {
            display: inline-block;
            border-radius: 50px;
            background: linear-gradient(135deg, #3498db, #2c3e50);
            color: white;
            font-size: 1rem;
            font-weight: bold;
            padding: 15px 45px;
            text-decoration: none;
            margin: 20px 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffecb5;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
            color: #856404;
        }
        .footer {
            background-color: #f8f9fa;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #dee2e6;
        }
        .footer p {
            color: #7f8c8d;
            font-size: 0.9rem;
        }
        .support-link {
            color: #3498db;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="tradewise-logo">TRADEWISE</div>
            <h1>📝 Complete Your Profile</h1>
        </div>
        
        <div class="content">
            <div class="greeting">Dear {first_name},</div>
            
            <div class="message">
                We noticed that your profile is missing some <strong>important information</strong>. 
                To continue enjoying full access to TradeWise features, please update your profile.
            </div>
            
            <div class="credentials-box">
                <h3>📋 What's Missing?</h3>
                <p><strong>📱 Phone Number:</strong> Required for account recovery and notifications</p>
                <p><strong>🔐 Password:</strong> Recommended to update for security</p>
            </div>
            
            <div style="text-align: center;">
                <a href="https://tradewise-hub.com/force-profile-update/" class="update-button">
                    📝 UPDATE YOUR PROFILE NOW
                </a>
            </div>
            
            <div class="warning-box">
                <p><strong>⚠️ ONE-TIME ACTION REQUIRED:</strong></p>
                <p>• Click the button above to update your profile</p>
                <p>• Enter your <strong>phone number</strong> (required)</p>
                <p>• You can also <strong>change your password</strong> (recommended)</p>
                <p>• This is a <strong>ONE-TIME</strong> process</p>
            </div>
            
            <div class="message">
                <p><strong>What to expect:</strong></p>
                <ol>
                    <li>Click the <strong>Update Your Profile Now</strong> button</li>
                    <li>Enter your <strong>phone number</strong> (required field)</li>
                    <li>Optionally, choose a <strong>new password</strong></li>
                    <li>Click update - you're done! ✅</li>
                </ol>
            </div>
        </div>
        
        <div class="footer">
            <p>Need help? Contact us: <a href="mailto:support@tradewise-hub.com" class="support-link">support@tradewise-hub.com</a></p>
            <p>© 2026 TradeWise. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

# Plain text version
PLAIN_TEMPLATE = """
TRADEWISE - ONE-TIME PROFILE UPDATE REQUIRED
=============================================

Dear {first_name},

We noticed that your profile is missing important information.

WHAT'S MISSING:
---------------
• Phone Number - Required for account recovery
• Password - Recommended to update for security

ONE-TIME ACTION REQUIRED:
-------------------------
Click the link below to update your profile:
https://tradewise-hub.com/force-profile-update/

WHAT YOU NEED TO DO:
--------------------
1. Click the link above
2. Enter your phone number (required)
3. Optionally change your password
4. Click update - you're done!

Need help? Contact: support@tradewise-hub.com

Best regards,
TradeWise Team
"""

def send_email_smtp(to_email, subject, html_content, plain_content):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"TradeWise Support <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(plain_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")
        return False

# ================= MAIN EXECUTION =================

print("\n📨 SENDING ONE-TIME PROFILE UPDATE EMAILS...")
print("-" * 70)

sent_count = 0
error_count = 0
error_list = []

for i, user in enumerate(users_without_phone, 1):
    try:
        print(f"📧 [{i:3d}/{total_users}] Processing: {user.email[:35]:35}", end=" ")
        
        html_content = HTML_TEMPLATE.format(
            first_name=user.first_name,
            second_name=user.second_name,
            email=user.email,
            account_number=user.account_number
        )
        
        plain_content = PLAIN_TEMPLATE.format(
            first_name=user.first_name,
            email=user.email,
            account_number=user.account_number
        )
        
        success = send_email_smtp(
            to_email=user.email,
            subject='📝 ONE-TIME ACTION: Complete Your TradeWise Profile',
            html_content=html_content,
            plain_content=plain_content
        )
        
        if success:
            sent_count += 1
            print("✅ Sent")
        else:
            error_count += 1
            error_list.append(user.email)
            print("❌ Failed")
        
        if i % 20 == 0:
            print(f"\n📊 Progress: {i}/{total_users} ({int(i/total_users*100)}%) - {sent_count} sent\n")
            time.sleep(2)
            
    except Exception as e:
        error_count += 1
        error_list.append(user.email)
        print(f"❌ Error: {str(e)[:50]}")

# Final Summary
print("\n" + "=" * 70)
print("📊 FINAL REPORT")
print("=" * 70)
print(f"✅ Successfully sent: {sent_count} emails")
print(f"❌ Failed: {error_count} emails")
print(f"📧 Total users processed: {total_users}")

if error_count > 0:
    print("\n📋 Failed emails:")
    for email in error_list[:10]:
        print(f"   • {email}")

print("\n🎉 ONE-TIME PROFILE UPDATE NOTIFICATION COMPLETE!")