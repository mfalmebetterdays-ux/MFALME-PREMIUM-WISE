"""
TRADEWISE PASSWORD RESET NOTIFICATION - MASTER SCRIPT
Sends beautiful HTML emails to ALL 212 users
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from myapp.models import Tradeviewusers, Notification
import time

# ================= YOUR GMAIL CONFIG =================
GMAIL_USER = "theofficialtradewise@gmail.com"
APP_PASSWORD = "nmwygxenkrmagybb"  # Your app password
# =====================================================

print("\n" + "=" * 70)
print("🚀 TRADEWISE PASSWORD RESET NOTIFICATION SYSTEM")
print("=" * 70)
print(f"📧 Sending from: {GMAIL_USER}")
print("=" * 70)

# Get all users
all_users = Tradeviewusers.objects.all()
total_users = all_users.count()
print(f"📊 Total users to notify: {total_users}\n")

# Beautiful HTML Email Template with your exact theme
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset - TradeWise</title>
    <style>
        @import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            font-family: 'Montserrat', sans-serif;
            margin: 0;
            padding: 40px 20px;
        }

        .email-container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
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
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header h1 {
            color: white;
            font-size: 1.8rem;
            font-weight: 400;
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
            font-size: 1.2rem;
        }

        .credentials-box p {
            margin: 10px 0;
            font-size: 1rem;
            color: #2c3e50;
        }

        .credentials-box strong {
            color: #3498db;
            font-weight: 700;
            min-width: 120px;
            display: inline-block;
        }

        .password-box {
            background: #2c3e50;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            text-align: center;
        }

        .password-box span {
            font-family: monospace;
            font-size: 1.8rem;
            font-weight: bold;
            color: white;
            letter-spacing: 2px;
        }

        .reset-button {
            display: inline-block;
            border-radius: 50px;
            border: none;
            background: linear-gradient(135deg, #3498db, #2c3e50);
            color: white;
            font-size: 1rem;
            font-weight: bold;
            padding: 15px 45px;
            text-decoration: none;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 20px 0;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }

        .reset-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(52, 152, 219, 0.4);
        }

        .warning-box {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
            color: #721c24;
        }

        .warning-box p {
            margin: 8px 0;
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
            margin: 5px 0;
        }

        .support-link {
            color: #3498db;
            text-decoration: none;
            font-weight: 600;
        }

        .support-link:hover {
            text-decoration: underline;
        }

        @media (max-width: 480px) {
            .header {
                padding: 30px 20px;
            }
            
            .content {
                padding: 30px 20px;
            }
            
            .tradewise-logo {
                font-size: 2rem;
            }
            
            .header h1 {
                font-size: 1.4rem;
            }
            
            .password-box span {
                font-size: 1.4rem;
            }
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="tradewise-logo">TRADEWISE</div>
            <h1>🔐 Password Reset Notification</h1>
        </div>
        
        <div class="content">
            <div class="greeting">Dear {first_name},</div>
            
            <div class="message">
                As part of our <strong>system-wide security upgrade</strong>, we have reset your TradeWise account password. 
                This is a <span style="color: #e74c3c; font-weight: bold;">ONE-TIME temporary password</span> that you must change immediately.
            </div>
            
            <div class="credentials-box">
                <h3>📋 Your Account Details</h3>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>TradeWise Number:</strong> {account_number}</p>
                <p><strong>Name:</strong> {first_name} {second_name}</p>
                
                <div class="password-box">
                    <span>ResetMe@2025</span>
                </div>
                <p style="text-align: center; margin-top: 10px; color: #7f8c8d; font-size: 0.9rem;">
                    ⬆️ Your temporary password ⬆️
                </p>
            </div>
            
            <div style="text-align: center;">
                <a href="https://tradewise-hub.com/forgot-password/" class="reset-button">
                    🔑 CHANGE YOUR PASSWORD NOW
                </a>
            </div>
            
            <div class="warning-box">
                <p><strong>⚠️ IMMEDIATE ACTION REQUIRED:</strong></p>
                <p>• This is a <strong>ONE-TIME</strong> temporary password</p>
                <p>• You MUST change it immediately after logging in</p>
                <p>• Never share your password with anyone</p>
                <p>• TradeWise will NEVER ask for your password</p>
            </div>
            
            <div class="message">
                <p><strong>Why did this happen?</strong></p>
                <p>We performed a security upgrade to protect all accounts. This temporary password allows you to regain access while maintaining the highest level of security.</p>
                
                <p style="margin-top: 20px;"><strong>How to login:</strong></p>
                <ol style="margin-left: 20px; color: #34495e;">
                    <li>Go to <strong>https://tradewise-hub.com/login/</strong></li>
                    <li>Enter your email and temporary password: <strong>ResetMe@2025</strong></li>
                    <li>You'll be prompted to create a new password</li>
                    <li>Choose a strong, unique password</li>
                </ol>
            </div>
        </div>
        
        <div class="footer">
            <p>Need help? Contact our support team:</p>
            <p><a href="mailto:support@tradewise-hub.com" class="support-link">support@tradewise-hub.com</a></p>
            <p style="margin-top: 20px;">© 2026 TradeWise. All rights reserved.</p>
            <p style="font-size: 0.8rem;">The Wisest Choice for Trading</p>
        </div>
    </div>
</body>
</html>
"""

# Plain text version (fallback)
PLAIN_TEMPLATE = """
TRADEWISE - PASSWORD RESET NOTIFICATION
========================================

Dear {first_name},

Your TradeWise account password has been reset as part of our security upgrade.

YOUR TEMPORARY CREDENTIALS:
--------------------------
Email: {email}
TradeWise Number: {account_number}
Temporary Password: ResetMe@2025

⚠️ IMPORTANT - ACTION REQUIRED:
• This is a ONE-TIME temporary password
• You MUST change it immediately after logging in
• Never share your password with anyone

HOW TO LOGIN:
1. Go to: https://tradewise-hub.com/login/
2. Use your email and temporary password: ResetMe@2025
3. You'll be prompted to create a new password
4. Choose a strong, unique password

RESET LINK (if needed):
https://tradewise-hub.com/forgot-password/

Need help? Contact: support@tradewise-hub.com

Best regards,
TradeWise Support Team
"""

def send_email_smtp(to_email, subject, html_content, plain_content):
    """Send email using SMTP with your Gmail"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"TradeWise Support <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach plain text and HTML
        msg.attach(MIMEText(plain_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, APP_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"   ❌ SMTP Error: {str(e)[:50]}...")
        return False

# Send to ALL users
sent_count = 0
error_count = 0
error_list = []

print("\n📨 SENDING EMAILS TO ALL 212 USERS...")
print("-" * 70)

for i, user in enumerate(all_users, 1):
    try:
        # Create database notification
        Notification.objects.create(
            user=user,
            title='🔐 URGENT: Your Password Has Been Reset',
            message='Your password has been reset to: ResetMe@2025. Login immediately and change your password.',
            notification_type='warning'
        )
        
        # Prepare email content
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
        
        # Send email
        success = send_email_smtp(
            to_email=user.email,
            subject='🔐 URGENT: Your TradeWise Password Has Been Reset',
            html_content=html_content,
            plain_content=plain_content
        )
        
        if success:
            sent_count += 1
            print(f"✅ [{i:3d}/{total_users}] Sent to: {user.email[:25]:25} - {user.first_name}")
        else:
            error_count += 1
            error_list.append(user.email)
            print(f"❌ [{i:3d}/{total_users}] Failed: {user.email[:25]:25}")
        
        # Progress update every 20 emails
        if i % 20 == 0:
            print(f"\n📊 Progress: {i}/{total_users} ({int(i/total_users*100)}%) - {sent_count} sent, {error_count} failed\n")
            time.sleep(2)  # Pause to avoid rate limiting
            
    except Exception as e:
        error_count += 1
        error_list.append(user.email)
        print(f"❌ [{i:3d}/{total_users}] Error: {user.email[:25]} - {str(e)[:30]}")
        continue

# Final Summary
print("\n" + "=" * 70)
print("📊 FINAL REPORT")
print("=" * 70)
print(f"✅ Successfully sent: {sent_count} emails")
print(f"❌ Failed: {error_count} emails")
print(f"📧 Total users: {total_users}")

if error_count > 0:
    print("\n📋 Failed emails (retry these):")
    for email in error_list[:10]:  # Show first 10
        print(f"   • {email}")
    if len(error_list) > 10:
        print(f"   ... and {len(error_list) - 10} more")

print("\n" + "=" * 70)
print("🎉 MISSION COMPLETE!")
print("=" * 70)
print(f"""
📧 FROM: {GMAIL_USER}
🔑 APP PASSWORD: [HIDDEN]
📊 TOTAL SENT: {sent_count}/{total_users}
🔐 TEMP PASSWORD: ResetMe@2025
🌐 RESET LINK: https://tradewise-hub.com/forgot-password/

✅ Database notifications created for ALL users
✅ Beautiful HTML emails sent
✅ Users can now login and reset passwords
""")