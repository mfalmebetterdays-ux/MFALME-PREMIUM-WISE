"""
VERIFY INJECTION RESULTS
Run this to check what was injected
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from myapp.models import Tradeviewusers, Affiliate, Referral
from django.db.models import Count, Sum

print("\n" + "=" * 60)
print("📊 TRADEWISE DATABASE VERIFICATION")
print("=" * 60)

# User statistics
total_users = Tradeviewusers.objects.count()
active_users = Tradeviewusers.objects.filter(is_active=True).count()
verified_users = Tradeviewusers.objects.filter(is_email_verified=True).count()

print(f"\n👤 USER STATISTICS:")
print(f"   - Total Users: {total_users}")
print(f"   - Active Users: {active_users}")
print(f"   - Verified Users: {verified_users}")

# Sample users
print(f"\n📋 SAMPLE USERS (first 10):")
for user in Tradeviewusers.objects.all().order_by('-created_at')[:10]:
    print(f"   - {user.email} (TWN: {user.account_number}) - {user.first_name}")

# Affiliate statistics
total_affiliates = Affiliate.objects.count()
total_referrals = Referral.objects.count()
total_coins = Affiliate.objects.aggregate(Sum('coin_balance'))['coin_balance__sum'] or 0
total_coins_earned = Affiliate.objects.aggregate(Sum('total_coins_earned'))['total_coins_earned__sum'] or 0

print(f"\n🤝 AFFILIATE STATISTICS:")
print(f"   - Total Affiliates: {total_affiliates}")
print(f"   - Total Referrals: {total_referrals}")
print(f"   - Total Coin Balance: {total_coins}")
print(f"   - Total Coins Earned: {total_coins_earned}")

# Top referrers
print(f"\n🏆 TOP REFERRERS:")
top_affiliates = Affiliate.objects.order_by('-total_referrals')[:5]
for aff in top_affiliates:
    print(f"   - {aff.user.email}: {aff.total_referrals} referrals, {aff.coin_balance} coins")

print("\n✅ Verification complete!")