"""
TRADEWISE GMAIL SCRAPER - SENT BOX VERSION
Scans SENT emails (where your account emails and referral notifications are)
"""

import imaplib
import email
from email.header import decode_header
import re
import pandas as pd
from datetime import datetime
import time

# ================= CONFIGURATION =================
GMAIL_USER = "theofficialtradewise@gmail.com"
APP_PASSWORD = "nmwygxenkrmagybb"
# =================================================

class GmailAppScraper:
    def __init__(self, email_address, app_password):
        self.email = email_address
        self.password = app_password.replace(' ', '')
        self.imap = None
        
    def connect(self):
        """Connect to Gmail IMAP"""
        try:
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
            self.imap.login(self.email, self.password)
            print("✅ Connected to Gmail!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def search_sent_emails(self):
        """Search ALL emails in SENT folder"""
        if not self.imap:
            print("❌ Not connected.")
            return []
        
        # Select SENT folder (Gmail uses "[Gmail]/Sent Mail")
        print("\n📂 Opening SENT folder...")
        status, folders = self.imap.list()
        
        # Try different possible sent folder names
        sent_folders = ['"[Gmail]/Sent Mail"', 'Sent', '"Sent Mail"', '[Gmail]/Sent']
        
        for folder in sent_folders:
            try:
                self.imap.select(folder)
                print(f"✅ Selected folder: {folder}")
                break
            except:
                continue
        
        # Get ALL emails in sent folder
        result, data = self.imap.search(None, 'ALL')
        email_ids = data[0].split()
        
        print(f"📧 Found {len(email_ids)} TOTAL emails in Sent folder")
        return email_ids
    
    def fetch_email(self, email_id):
        """Fetch full email by ID"""
        result, data = self.imap.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        return email.message_from_bytes(raw_email)
    
    def get_email_body(self, msg):
        """Extract plain text body from email"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        continue
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return body
    
    def is_account_email(self, subject, body):
        """Check if this is an account creation email"""
        subject = subject.lower()
        body_lower = body.lower()
        
        keywords = ['tradewise number', 'account created', 'welcome', 'credentials']
        return any(k in subject or k in body_lower for k in keywords)
    
    def is_referral_email(self, subject, body):
        """Check if this is a referral notification email"""
        subject = subject.lower()
        body_lower = body.lower()
        
        keywords = ['referral', 'coins awarded', 'referred', 'new referral']
        return any(k in subject or k in body_lower for k in keywords)
    
    def extract_account_data(self, body):
        """Extract account creation data"""
        data = {}
        
        patterns = {
            'tradewise_number': r'TradeWise Number:\s*(\d+)',
            'name': r'Name:\s*([^\n]+)',
            'email': r'Email:\s*([^\n@]+@[^\n]+)',
            'password': r'Password:\s*([^\n]+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                data[key] = match.group(1).strip()
        
        return data
    
    def extract_referral_data(self, body):
        """Extract referral notification data"""
        data = {}
        
        patterns = {
            'referrer_name': r'Congratulations\s+([^!]+)',
            'new_user_name': r'New User:\s+([^\n]+)',
            'new_user_email': r'Email:\s*([^\n@]+@[^\n]+)',
            'new_user_number': r'TradeWise Number:\s*(\d+)',
            'coins_awarded': r'(\d+)\s*TWC coins',
            'new_balance': r'New Balance:\s*(\d+)\s*TWC',
            'total_referrals': r'Total Referrals:\s*(\d+)',
            'total_coins_earned': r'Total Coins Earned:\s*(\d+)',
            'cash_value': r'Cash Value:\s*KES\s*(\d+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                data[key] = match.group(1).strip()
        
        return data
    
    def extract_email(self, text):
        """Extract email address from string"""
        if not text:
            return ""
        match = re.search(r'<([^>]+)>|([^\s@]+@[^\s@]+)', text)
        if match:
            return match.group(1) or match.group(2)
        return text.strip()
    
    def scrape_all_sent_emails(self):
        """Scrape ALL sent emails and categorize them"""
        print(f"\n{'='*60}")
        print("📋 SCRAPING ALL SENT EMAILS - EVER!")
        print('='*60)
        
        # Get all sent emails
        email_ids = self.search_sent_emails()
        total = len(email_ids)
        
        if total == 0:
            print("❌ No emails found in Sent folder!")
            return [], []
        
        accounts = []
        referrals = []
        
        print(f"\n⏳ Processing {total} sent emails...")
        print("📊 Categories: Account Creation Emails vs Referral Emails\n")
        
        start_time = time.time()
        
        for i, eid in enumerate(email_ids, 1):
            # Progress indicator
            if i % 10 == 0 or i == total:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                remaining = (total - i) / rate if rate > 0 else 0
                print(f"  Progress: {i}/{total} ({int(i/total*100)}%) - {len(accounts)} accounts, {len(referrals)} referrals | ETA: {int(remaining)}s", end='\r')
            
            try:
                msg = self.fetch_email(eid)
                subject = msg.get('Subject', '')
                body = self.get_email_body(msg)
                to_field = msg.get('To', '')
                date = msg.get('Date', '')
                
                if not body:
                    continue
                
                # Check if it's an account creation email
                if self.is_account_email(subject, body):
                    data = self.extract_account_data(body)
                    if data:
                        data['date'] = date
                        data['subject'] = subject
                        data['to'] = self.extract_email(to_field)
                        data['to_email'] = self.extract_email(to_field)
                        accounts.append(data)
                
                # Check if it's a referral email
                if self.is_referral_email(subject, body):
                    data = self.extract_referral_data(body)
                    if data:
                        data['date'] = date
                        data['subject'] = subject
                        data['to'] = self.extract_email(to_field)
                        data['referrer_email'] = self.extract_email(to_field)
                        referrals.append(data)
                
                time.sleep(0.02)  # Be nice to Gmail
                
            except Exception as e:
                print(f"\n⚠️ Error on email {i}: {e}")
                continue
        
        print(f"\n\n✅ COMPLETE!")
        print(f"   - Account emails found: {len(accounts)}")
        print(f"   - Referral emails found: {len(referrals)}")
        print(f"   - Total emails processed: {total}")
        
        return accounts, referrals
    
    def save_to_excel(self, accounts, referrals):
        """Save data to Excel file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'tradewise_SENT_DATA_{timestamp}.xlsx'
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Accounts sheet
            if accounts:
                df_accounts = pd.DataFrame(accounts)
                # Reorder columns
                cols = ['date', 'to_email', 'name', 'email', 'tradewise_number', 'password', 'subject']
                available_cols = [c for c in cols if c in df_accounts.columns]
                df_accounts = df_accounts[available_cols]
                df_accounts.to_excel(writer, sheet_name='Account Creations', index=False)
            
            # Referrals sheet
            if referrals:
                df_referrals = pd.DataFrame(referrals)
                # Reorder columns
                cols = ['date', 'referrer_email', 'referrer_name', 'new_user_name', 
                       'new_user_email', 'new_user_number', 'coins_awarded', 
                       'new_balance', 'total_referrals', 'total_coins_earned',
                       'cash_value', 'subject']
                available_cols = [c for c in cols if c in df_referrals.columns]
                df_referrals = df_referrals[available_cols]
                df_referrals.to_excel(writer, sheet_name='Referrals', index=False)
            
            # Summary sheet
            summary = pd.DataFrame({
                'Metric': [
                    'Total Account Emails (SENT)',
                    'Total Referral Emails (SENT)',
                    'Total Emails Processed',
                    'Export Date',
                    'Email Account',
                    'Folder'
                ],
                'Value': [
                    len(accounts),
                    len(referrals),
                    len(accounts) + len(referrals),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    self.email,
                    'SENT'
                ]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"\n✅ Data saved to {filename}")
        return filename
    
    def generate_referrer_stats(self, referrals):
        """Generate statistics by referrer"""
        if not referrals:
            return pd.DataFrame()
        
        stats = {}
        for ref in referrals:
            email = ref.get('referrer_email', 'unknown')
            name = ref.get('referrer_name', '')
            
            if email not in stats:
                stats[email] = {
                    'referrer_email': email,
                    'referrer_name': name,
                    'total_referrals': 0,
                    'total_coins_awarded': 0,
                    'current_balance': 0,
                }
            
            stats[email]['total_referrals'] += 1
            coins = int(ref.get('coins_awarded', 0)) if ref.get('coins_awarded') else 0
            stats[email]['total_coins_awarded'] += coins
            stats[email]['current_balance'] = int(ref.get('new_balance', 0)) if ref.get('new_balance') else 0
        
        return pd.DataFrame(list(stats.values()))

def main():
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   TRADEWISE GMAIL SCRAPER - SENT BOX VERSION     ║
    ║   Scanning SENT emails (where your emails are!)   ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    # Your credentials
    email = "theofficialtradewise@gmail.com"
    app_password = "nmwygxenkrmagybb"
    
    print(f"📧 Email: {email}")
    print(f"🔑 Password: [hidden]")
    
    # Create scraper
    scraper = GmailAppScraper(email, app_password)
    
    # Connect
    if not scraper.connect():
        print("❌ Failed to connect. Check your email and app password.")
        return
    
    # Scrape ALL sent emails
    accounts, referrals = scraper.scrape_all_sent_emails()
    
    if len(accounts) == 0 and len(referrals) == 0:
        print("\n❌ No account or referral emails found in Sent folder!")
        print("   This could mean:")
        print("   1. The emails are in a different folder (try 'All Mail')")
        print("   2. The search patterns need adjustment")
        print("   3. Your sent folder is empty")
        return
    
    # Save to Excel
    filename = scraper.save_to_excel(accounts, referrals)
    
    # Generate referrer stats
    if referrals:
        stats_df = scraper.generate_referrer_stats(referrals)
        stats_file = f'tradewise_referrer_stats_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        stats_df.to_csv(stats_file, index=False)
        print(f"✅ Referrer stats saved to {stats_file}")
    
    # Show final stats
    print(f"\n{'='*60}")
    print(f"📊 FINAL STATISTICS - SENT EMAILS")
    print(f"{'='*60}")
    print(f"   - Account emails found: {len(accounts)}")
    print(f"   - Referral emails found: {len(referrals)}")
    
    if accounts:
        print(f"\n📋 Sample accounts (first 5):")
        for i, acc in enumerate(accounts[:5]):
            print(f"   {i+1}. {acc.get('name', 'N/A')} - {acc.get('email', 'N/A')} - TWN: {acc.get('tradewise_number', 'N/A')}")
    
    if referrals:
        total_coins = sum(int(r.get('coins_awarded', 0)) for r in referrals if r.get('coins_awarded'))
        unique_referrers = len(set(r.get('referrer_email', '') for r in referrals if r.get('referrer_email')))
        print(f"\n💰 Referral Summary:")
        print(f"   - Total coins awarded: {total_coins}")
        print(f"   - Unique referrers: {unique_referrers}")
        
        print(f"\n📋 Sample referrals (first 5):")
        for i, ref in enumerate(referrals[:5]):
            print(f"   {i+1}. {ref.get('referrer_name', 'N/A')} referred {ref.get('new_user_name', 'N/A')} - {ref.get('coins_awarded', '0')} coins")
    
    print(f"\n✅ COMPLETE! Check {filename}")

if __name__ == '__main__':
    main()