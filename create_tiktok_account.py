#!/usr/bin/env python3
"""
TikTok Account Creation Demo

This script demonstrates the TikTok account creation capabilities of the automation bot.
It creates a new TikTok account using temporary email and device fingerprinting.
"""
import time
import logging
import sys
from seleniumbase import Driver
from account_manager import AccountManager, AccountCreator
from proxy_manager import ProxyManager
from email_generator import EmailGenerator
import config


def initialize_driver(proxy_data=None, fingerprint=None):
    """Initialize and return the Selenium WebDriver with optional proxy and fingerprint."""
    try:
        logger.info("Initializing WebDriver...")
        
        # Driver configuration based on settings
        driver_args = {
            'headless': config.HEADLESS,
        }
        
        # Add proxy configuration if provided
        if proxy_data:
            host = proxy_data.get('host')
            port = proxy_data.get('port')
            username = proxy_data.get('username')
            password = proxy_data.get('password')
            
            if username and password:
                proxy_string = f"{username}:{password}@{host}:{port}"
            else:
                proxy_string = f"{host}:{port}"
            
            driver_args['proxy_string'] = proxy_string
            logger.info(f"Configured proxy: {host}:{port}")
        
        # Add fingerprint user agent if provided
        if fingerprint and fingerprint.get('user_agent'):
            driver_args['user_agent'] = fingerprint['user_agent']
            logger.info(f"Using custom user agent")
        
        # Use undetected-chromedriver mode if configured
        if config.BROWSER_MODE == "uc":
            driver_args['uc'] = True
            logger.info("Using undetected-chromedriver mode")

        driver = Driver(**driver_args)
        driver.maximize_window()
        
        # Apply additional fingerprint masking via JavaScript
        if fingerprint:
            from social_media.tiktok import apply_fingerprint
            apply_fingerprint(driver, fingerprint)
        
        logger.info("WebDriver initialized successfully")
        return driver
        
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_tiktok_account():
    """
    Create a TikTok account using the automation bot's account creation functionality.
    """
    print("=" * 70)
    print("TikTok Account Creation Demo")
    print("=" * 70)
    
    # Initialize managers
    account_manager = AccountManager("accounts.json")
    proxy_manager = ProxyManager("proxies.json") if False else None  # Proxies disabled for demo
    
    # Initialize email generator with Guerrilla Mail
    email_generator = EmailGenerator(
        strategy='guerrillamail',
        domains=['gmail.com', 'yahoo.com', 'outlook.com']
    )
    
    # Initialize account creator
    account_creator = AccountCreator(account_manager, proxy_manager, email_generator)
    
    print("\nInitializing WebDriver...")
    driver = initialize_driver()
    
    try:
        print("\n" + "=" * 70)
        print("Step 1: Generating Temporary Email")
        print("=" * 70)
        
        # Generate email
        email = email_generator.generate_email()
        print(f"✓ Generated temporary email: {email}")
        
        print("\n" + "=" * 70)
        print("Step 2: Generating Device Fingerprint")
        print("=" * 70)
        
        from social_media.tiktok import generate_device_fingerprint
        fingerprint = generate_device_fingerprint()
        print(f"✓ Generated fingerprint:")
        print(f"  - Platform: {fingerprint['platform']}")
        print(f"  - Screen: {fingerprint['screen']}")
        print(f"  - User Agent: {fingerprint['user_agent'][:50]}...")
        print(f"  - Timezone: {fingerprint['timezone']}")
        
        print("\n" + "=" * 70)
        print("Step 3: Starting TikTok Account Creation")
        print("=" * 70)
        
        print("\nAttempting to create TikTok account...")
        print("Note: This will:")
        print("  - Navigate to tiktok.com/signup")
        print("  - Fill in email, password, and username")
        print("  - Apply device fingerprint masking")
        print("  - Wait for manual verification (email/captcha)")
        print()
        
        # Create account
        account = account_creator.create_account(
            driver=driver,
            use_proxy=False,
            email=email,
            password=None,  # Will auto-generate
            username=None,  # Will auto-generate
            birth_date=None,  # Will use default
            rotate_proxy=False,
            use_fingerprint=True
        )
        
        if account:
            print("\n" + "=" * 70)
            print("✓ Account Created Successfully!")
            print("=" * 70)
            print(f"Email: {account['email']}")
            print(f"Username: {account['username']}")
            print(f"Password: {account['password']}")
            print(f"Status: {account['status']}")
            print(f"Created: {account['created_at']}")
            print("\n✓ Account saved to accounts.json")
            return True
        else:
            print("\n" + "=" * 70)
            print("✗ Account Creation Failed")
            print("=" * 70)
            print("This is normal when:")
            print("  - TikTok has changed their signup page structure")
            print("  - Captcha is detected and requires manual solving")
            print("  - Email verification is needed")
            print("  - TikTok's anti-bot measures block the automation")
            print()
            print("The account data structure was created, but the actual TikTok")
            print("account needs manual completion of verification steps.")
            return False
            
    except Exception as e:
        logger.error(f"Error during account creation: {e}")
        print(f"\n✗ Error: {e}")
        return False
        
    finally:
        print("\n" + "=" * 70)
        print("Cleaning up...")
        print("=" * 70)
        driver.quit()
        print("✓ WebDriver closed")


def main():
    """Main function."""
    try:
        success = create_tiktok_account()
        
        print("\n" + "=" * 70)
        print("Summary")
        print("=" * 70)
        
        if success:
            print("✓ TikTok account creation process completed successfully!")
            print("\nNext steps:")
            print("  1. Check accounts.json for the saved account details")
            print("  2. Use these credentials to log in to TikTok")
            print("  3. Complete any manual verification steps")
            print("  4. Use the account for TikTok automation tasks")
        else:
            print("⚠️ Account creation encountered issues")
            print("\nThis is common with automated account creation due to:")
            print("  - TikTok's anti-bot detection systems")
            print("  - Frequent changes to the signup page structure")
            print("  - Captcha challenges")
            print("  - Email/phone verification requirements")
            print()
            print("For best results:")
            print("  - Use manual account creation and import to accounts.json")
            print("  - Or run the bot in non-headless mode to solve captcha manually")
        
        print("\n" + "=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
