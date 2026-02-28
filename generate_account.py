#!/usr/bin/env python3
"""
Simple script to generate TikTok account data structure
"""
import sys
import secrets
import string
import logging
from datetime import datetime
import config
from account_manager import AccountManager, AccountCreator
from proxy_manager import ProxyManager
from email_generator import EmailGenerator

# Configure logging
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
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def main():
    print("\n" + "=" * 60)
    print("TikTok Account Generator")
    print("=" * 60)

    # Initialize managers
    account_manager = AccountManager(config.ACCOUNTS_FILE)

    # Use random email strategy
    email_generator = EmailGenerator(
        strategy='random',
        domains=config.EMAIL_DOMAINS,
        emails_file=config.CUSTOM_EMAILS_FILE
    )

    account_creator = AccountCreator(account_manager, None, email_generator)

    print(f"\nGenerating TikTok account data...")
    print(f"- Email strategy: random")
    print(f"- Generating secure password")
    print(f"- Creating account data structure")

    # Generate account data directly without browser
    try:
        email = email_generator.generate_email()
        password = generate_secure_password(16)

        account_data = {
            'email': email,
            'password': password,
            'username': None,  # Can be set later
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'cookies': {}
        }

        # Add to account manager
        if account_manager.add_account(account_data):
            print(f"\n✓ Account generated successfully!")
            print(f"  Email: {email}")
            print(f"  Password: {password}")
            print(f"\nAccount saved to: {config.ACCOUNTS_FILE}")
            print(f"\nNote: This is just account data generation.")
            print(f"      To create an actual TikTok account, you'll need to:")
            print(f"      1. Go to tiktok.com/signup")
            print(f"      2. Use the generated email and password")
            print(f"      3. Complete the verification process (email/phone)")
            print(f"      4. The account is then ready to use with the bot")
        else:
            print(f"\n✗ Failed to generate account")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error during account generation: {e}", exc_info=True)
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
