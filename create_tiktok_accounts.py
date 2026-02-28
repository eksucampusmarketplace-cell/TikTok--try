#!/usr/bin/env python3
"""
TikTok Account Creator Script

This script creates TikTok account entries in the system.
It generates account data with random emails and secure passwords.
"""
import secrets
import string
import json
import logging
from datetime import datetime
import config
from account_manager import AccountManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def generate_secure_password(length=16):
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def generate_username():
    """Generate a random username."""
    adjectives = ['cool', 'awesome', 'happy', 'lucky', 'smart', 'brave', 'creative', 'wild', 
                 ' epic', 'super', 'mega', 'hyper', ' turbo', 'pro', 'master', 'chief']
    nouns = ['tiger', 'eagle', 'dolphin', 'wolf', 'bear', 'lion', 'fox', 'hawk', 
             'player', 'gamer', 'star', 'king', 'queen', 'lord', 'champ', 'boss']
    num = secrets.randbelow(1000)
    return f"{secrets.choice(adjectives).strip()}{secrets.choice(nouns)}{num}"


def generate_random_email():
    """Generate a random email address."""
    prefixes = ['user', 'player', 'gamer', 'tech', 'cool', 'awesome', 'happy', 'lucky',
                'alex', 'john', 'mike', 'sarah', 'emma', 'david', 'chris', 'jessica']
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'mail.com']
    prefix = secrets.choice(prefixes)
    number = secrets.randbelow(10000)
    domain = secrets.choice(domains)
    return f"{prefix}{number}@{domain}"


def create_accounts(num_accounts=5):
    """
    Create multiple TikTok account entries.
    
    Args:
        num_accounts: Number of accounts to create
    """
    account_manager = AccountManager(config.ACCOUNTS_FILE)
    
    print("\n" + "=" * 60)
    print("TikTok Account Creator")
    print("=" * 60)
    print(f"\nCreating {num_accounts} TikTok account entries...")
    
    created_accounts = []
    
    for i in range(num_accounts):
        email = generate_random_email()
        password = generate_secure_password(16)
        username = generate_username()
        
        account_data = {
            'email': email,
            'password': password,
            'username': username,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'cookies': {}
        }
        
        if account_manager.add_account(account_data):
            created_accounts.append(account_data)
            print(f"  ✓ Created: {email} (username: {username})")
        else:
            print(f"  ✗ Failed to create: {email}")
    
    print(f"\n{'=' * 60}")
    print(f"Summary: {len(created_accounts)}/{num_accounts} accounts created")
    print(f"{'=' * 60}")
    print(f"\nAccounts saved to: {config.ACCOUNTS_FILE}")
    print("\nIMPORTANT NOTE:")
    print("These are account DATA ENTRIES only.")
    print("To use these accounts with TikTok, you need to:")
    print("  1. Go to tiktok.com/signup")
    print("  2. Use the generated email and password")
    print("  3. Complete email/phone verification")
    print("  4. Set the username")
    print("\nThese credentials are for the bot's record-keeping.")
    
    return created_accounts


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Create TikTok account entries')
    parser.add_argument('-n', '--number', type=int, default=5, 
                        help='Number of accounts to create (default: 5)')
    args = parser.parse_args()
    
    create_accounts(args.number)


if __name__ == "__main__":
    main()
