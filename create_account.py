#!/usr/bin/env python3
"""
Simple script to create a TikTok account using the account creation wizard
"""
import sys
import time
import logging
import config
from account_manager import AccountManager, AccountCreator
from proxy_manager import ProxyManager
from email_generator import EmailGenerator
from main import initialize_driver

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

def main():
    print("\n" + "=" * 60)
    print("TikTok Account Creation Script")
    print("=" * 60)

    # Initialize managers
    account_manager = AccountManager(config.ACCOUNTS_FILE)
    proxy_manager = ProxyManager(config.PROXIES_FILE) if config.USE_PROXIES else None

    # Use random email strategy for simplicity
    email_generator = EmailGenerator(
        strategy='random',
        domains=config.EMAIL_DOMAINS,
        emails_file=config.CUSTOM_EMAILS_FILE
    )

    account_creator = AccountCreator(account_manager, proxy_manager, email_generator)

    print(f"\nAccount creation will:")
    print(f"- Use random email strategy (for testing)")
    print(f"- Generate secure passwords")
    print(f"- Create account data structure")
    print("\n⚠️ Note: This creates the account data structure.")
    print("   Actual TikTok account creation requires manual verification.")

    # Create driver
    try:
        print("\nInitializing browser...")
        driver = initialize_driver()

        # Create one account
        print("\nCreating account...")
        account = account_creator.create_account(driver, use_proxy=config.USE_PROXIES)

        if account:
            print(f"\n✓ Account created successfully!")
            print(f"  Email: {account['email']}")
            print(f"  Password: {account['password']}")
            if account.get('proxy'):
                print(f"  Proxy: {account['proxy']['host']}:{account['proxy']['port']}")
            print(f"\nAccount saved to: {config.ACCOUNTS_FILE}")
        else:
            print(f"\n✗ Failed to create account")

        driver.quit()

    except Exception as e:
        logger.error(f"Error during account creation: {e}", exc_info=True)
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
