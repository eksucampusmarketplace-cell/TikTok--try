#!/usr/bin/env python3
"""
Simple script to create a TikTok account using browser automation
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

    # Use random email strategy for testing
    email_generator = EmailGenerator(
        strategy='random',
        domains=config.EMAIL_DOMAINS,
        emails_file=config.CUSTOM_EMAILS_FILE
    )

    account_creator = AccountCreator(account_manager, proxy_manager, email_generator)

    print(f"\nAccount creation will:")
    print(f"- Use browser automation to navigate TikTok signup")
    print(f"- Generate email using random strategy")
    print(f"- Generate secure password")
    print(f"- Generate random username")
    print(f"- Create actual TikTok account")
    print(f"\nNote: You may need to complete captcha or email verification manually.")

    # Create driver for account creation
    try:
        print("\nInitializing browser...")
        driver = initialize_driver()

        # Navigate to TikTok signup page
        print("\nNavigating to TikTok signup...")
        driver.get("https://www.tiktok.com/signup/phone-or-email/email")
        time.sleep(3)

        # Create one account with username
        print("\nCreating account with username...")
        account = account_creator.create_account(driver, use_proxy=config.USE_PROXIES)

        if account:
            print(f"\n✓ Account created successfully!")
            print(f"  Email: {account['email']}")
            print(f"  Password: {account['password']}")
            print(f"  Username: {account.get('username', 'N/A')}")
            if account.get('proxy'):
                print(f"  Proxy: {account['proxy']['host']}:{account['proxy']['port']}")
            print(f"\nAccount saved to: {config.ACCOUNTS_FILE}")
            print(f"\nNext steps:")
            print(f"1. Check your email for verification code")
            print(f"2. Complete any captcha if required")
            print(f"3. Verify email when prompted")
        else:
            print(f"\n✗ Failed to create account")
            print("Check bot.log for details")

        # Wait a bit before closing
        print("\nKeeping browser open for 10 seconds for manual intervention if needed...")
        time.sleep(10)

        driver.quit()

    except Exception as e:
        logger.error(f"Error during account creation: {e}", exc_info=True)
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
