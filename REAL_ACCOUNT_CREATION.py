#!/usr/bin/env python3
"""
REAL TikTok Account Creation Script

This script guides you through creating an ACTUAL TikTok account
using a REAL temporary email address (Guerilla Mail, Temp Mail, or 10 Minute Mail).

No fake data, no simulators - REAL ACCOUNT CREATION.
"""
import sys
import time
import logging
import config
from main import initialize_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import secrets
import string

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
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

def wait_and_click(driver, selector, description, timeout=10):
    """Wait for element and click it."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(selector)
        )
        element.click()
        logger.info(f"✓ Clicked: {description}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to click {description}: {e}")
        return False

def wait_and_type(driver, selector, text, description, timeout=10, human_like=True):
    """Wait for element and type text into it."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(selector)
        )
        
        if human_like:
            # Type with human-like delays
            for char in text:
                element.send_keys(char)
                time.sleep(0.02)
        else:
            element.send_keys(text)
        
        logger.info(f"✓ Typed {description}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to type {description}: {e}")
        return False

def wait_for_element(driver, selector, description, timeout=10):
    """Wait for element to appear."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(selector)
        )
        logger.info(f"✓ Found: {description}")
        return element
    except Exception as e:
        logger.error(f"✗ Could not find {description}: {e}")
        return None

def main():
    print("\n" + "=" * 60)
    print("REAL TikTok Account Creation - No Simulators")
    print("=" * 60)
    
    print("\n📋 IMPORTANT: This creates REAL TikTok accounts")
    print("   You will need a REAL temporary email address")
    print("   Options: Guerilla Mail, Temp Mail, 10 Minute Mail")
    print("   Email services: guerillamail.com, tempmail.org, 10minutemail.com")
    print("\n" + "=" * 60)
    
    # Get user email
    print("\n📧 STEP 1: Email Address")
    print("-" * 40)
    email = input("Enter your REAL temporary email: ").strip()
    
    if not email:
        print("❌ Email is required!")
        print("   Get a temp email from any of these services:")
        print("   - guerillamail.com")
        print("   - tempmail.org")
        print("   - 10minutemail.com")
        sys.exit(1)
    
    # Generate username
    print("\n👤 STEP 2: Username")
    print("-" * 40)
    username = input("Enter desired username (or press Enter for auto): ").strip()
    
    if not username:
        # Generate random username
        adjectives = ['cool', 'awesome', 'happy', 'lucky', 'smart', 'brave', 'creative', 'wild']
        nouns = ['tiger', 'eagle', 'dolphin', 'wolf', 'bear', 'lion', 'fox', 'hawk']
        import random
        username = f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(100, 999)}"
        print(f"   Auto-generated: {username}")
    
    # Generate password
    password = generate_secure_password(16)
    print(f"\n🔐 STEP 3: Password")
    print("-" * 40)
    print(f"   Generated: {password}")
    
    print("\n" + "=" * 60)
    print("⚙️  STEP 4: Browser Setup")
    print("=" * 60)
    print("Initializing browser...")
    
    # Initialize browser
    try:
        driver = initialize_driver()
        logger.info("Browser initialized")
    except Exception as e:
        logger.error(f"Failed to initialize browser: {e}")
        print(f"\n❌ Error initializing browser: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🌐 STEP 5: Navigate to TikTok")
    print("=" * 60)
    print("Navigating to TikTok signup...")
    
    try:
        driver.get("https://www.tiktok.com/signup/phone-or-email/email")
        time.sleep(3)
        logger.info("Navigated to TikTok signup")
    except Exception as e:
        logger.error(f"Failed to navigate to TikTok: {e}")
        print(f"\n❌ Error navigating to TikTok: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("📝 STEP 6: Select Email Signup")
    print("=" * 60)
    
    # Select email signup option
    email_selectors = [
        (By.CSS_SELECTOR, 'span[data-e2e="email-tab"]'),
        (By.XPATH, '//span[contains(text(), "Email")]'),
        (By.CSS_SELECTOR, '[data-e2e="email-tab"]'),
        (By.XPATH, '//button[contains(@class, "email")]'),
    ]
    
    email_tab_clicked = False
    for selector in email_selectors:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(selector)
            )
            element.click()
            email_tab_clicked = True
            print("✓ Selected Email signup")
            time.sleep(2)
            break
        except:
            continue
    
    if not email_tab_clicked:
        print("⚠️  Could not find Email tab, may already be selected")
    
    print("\n" + "=" * 60)
    print("📧 STEP 7: Enter Email")
    print("=" * 60)
    
    # Enter email address
    email_input_selectors = [
        (By.CSS_SELECTOR, 'input[type="email"]'),
        (By.CSS_SELECTOR, 'input[name="email"]'),
        (By.CSS_SELECTOR, 'input[placeholder*="email"]'),
        (By.CSS_SELECTOR, 'input[placeholder*="Email"]'),
        (By.XPATH, '//input[@type="email"]'),
        (By.XPATH, '//input[@name="email"]'),
    ]
    
    email_entered = False
    for selector in email_input_selectors:
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(selector)
            )
            email_input.clear()
            
            # Type email with small delays
            for char in email:
                email_input.send_keys(char)
                time.sleep(0.03)
            
            email_entered = True
            print(f"✓ Entered email: {email}")
            time.sleep(2)
            break
        except:
            continue
    
    if not email_entered:
        print("❌ Could not find email input field")
        return
    
    print("\n" + "=" * 60)
    print("📝 STEP 8: Click Next")
    print("=" * 60)
    
    # Click next button after email
    next_selectors = [
        (By.XPATH, '//button[contains(text(), "Next")]'),
        (By.CSS_SELECTOR, 'button[type="submit"]'),
        (By.CSS_SELECTOR, '[data-e2e="next"]'),
        (By.XPATH, '//button[@type="submit"]'),
    ]
    
    next_clicked = False
    for selector in next_selectors:
        try:
            next_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(selector)
            )
            next_btn.click()
            next_clicked = True
            print("✓ Clicked Next")
            time.sleep(3)
            break
        except:
            continue
    
    if not next_clicked:
        print("⚠️  Could not click Next button, may need to press Enter")
        try:
            email_input.send_keys(Keys.ENTER)
            print("✓ Pressed Enter")
            time.sleep(3)
        except:
            pass
    
    print("\n" + "=" * 60)
    print("👤 STEP 9: Enter Username")
    print("=" * 60)
    
    # Enter username
    username_input_selectors = [
        (By.CSS_SELECTOR, 'input[name="username"]'),
        (By.CSS_SELECTOR, 'input[placeholder*="username"]'),
        (By.CSS_SELECTOR, 'input[placeholder*="@"]'),
        (By.XPATH, '//input[@name="username"]'),
        (By.XPATH, '//input[contains(@placeholder, "username")]'),
        (By.XPATH, '//input[contains(@placeholder, "@")]'),
    ]
    
    username_entered = False
    for selector in username_input_selectors:
        try:
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(selector)
            )
            username_input.clear()
            
            # Type username with small delays
            for char in username:
                username_input.send_keys(char)
                time.sleep(0.03)
            
            username_entered = True
            print(f"✓ Entered username: {username}")
            time.sleep(2)
            break
        except:
            continue
    
    if not username_entered:
        print("⚠️  Could not find username input field, may not be required yet")
    
    print("\n" + "=" * 60)
    print("🔐 STEP 10: Enter Password")
    print("=" * 60)
    
    # Enter password
    password_input_selectors = [
        (By.CSS_SELECTOR, 'input[type="password"]'),
        (By.CSS_SELECTOR, 'input[name="password"]'),
        (By.CSS_SELECTOR, 'input[placeholder*="password"]'),
        (By.XPATH, '//input[@type="password"]'),
        (By.XPATH, '//input[@name="password"]'),
        (By.XPATH, '//input[contains(@placeholder, "password")]'),
    ]
    
    password_entered = False
    for selector in password_input_selectors:
        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(selector)
            )
            password_input.clear()
            
            # Type password with small delays
            for char in password:
                password_input.send_keys(char)
                time.sleep(0.03)
            
            password_entered = True
            print("✓ Entered password")
            time.sleep(2)
            break
        except:
            continue
    
    if not password_entered:
        print("❌ Could not find password input field")
        return
    
    print("\n" + "=" * 60)
    print("📝 STEP 11: Click Next/Continue")
    print("=" * 60)
    
    # Click next button after password
    next_selectors = [
        (By.XPATH, '//button[contains(text(), "Next")]'),
        (By.XPATH, '//button[contains(text(), "Continue")]'),
        (By.CSS_SELECTOR, 'button[type="submit"]'),
        (By.XPATH, '//button[@type="submit"]'),
        (By.CSS_SELECTOR, '[data-e2e="next"]'),
        (By.CSS_SELECTOR, '[data-e2e="continue"]'),
    ]
    
    next_clicked = False
    for selector in next_selectors:
        try:
            next_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(selector)
            )
            next_btn.click()
            next_clicked = True
            print("✓ Clicked Next/Continue")
            time.sleep(4)
            break
        except:
            continue
    
    print("\n" + "=" * 60)
    print("📋 STEP 12: Email Verification")
    print("=" * 60)
    print("⏳ Waiting for email verification code...")
    print("   Check your email: " + email)
    print("   Look for 6-digit verification code from TikTok")
    
    # Wait for user to manually enter verification code
    print("\n" + "=" * 60)
    print("⌨️  STEP 13: Enter Verification Code")
    print("=" * 60)
    
    verification_code_input_selectors = [
        (By.CSS_SELECTOR, 'input[placeholder*="code"]'),
        (By.CSS_SELECTOR, 'input[name="code"]'),
        (By.CSS_SELECTOR, 'input[type="text"]'),
        (By.XPATH, '//input[contains(@placeholder, "code")]'),
        (By.XPATH, '//input[@name="code"]'),
    ]
    
    code = input("Enter the 6-digit code from your email: ").strip()
    
    if code and len(code) >= 4:
        print(f"\n📧 Entering code: {code}")
        
        for selector in verification_code_input_selectors:
            try:
                code_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(selector)
                )
                code_input.clear()
                
                # Type code with small delays
                for char in code:
                    code_input.send_keys(char)
                    time.sleep(0.05)
                
                print(f"✓ Entered verification code")
                time.sleep(2)
                break
            except:
                continue
        
        print("\n" + "=" * 60)
        print("📝 STEP 14: Submit Verification")
        print("=" * 60)
        
        # Click submit button
        submit_selectors = [
            (By.XPATH, '//button[contains(text(), "Submit")]'),
            (By.XPATH, '//button[contains(text(), "Verify")]'),
            (By.CSS_SELECTOR, 'button[type="submit"]'),
            (By.XPATH, '//button[@type="submit"]'),
        ]
        
        submitted = False
        for selector in submit_selectors:
            try:
                submit_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(selector)
                )
                submit_btn.click()
                submitted = True
                print("✓ Clicked Submit")
                time.sleep(5)
                break
            except:
                continue
        
        if not submitted:
            print("⚠️  Could not find submit button, may need to press Enter")
            try:
                code_input.send_keys(Keys.ENTER)
                print("✓ Pressed Enter")
            except:
                pass
    
    print("\n" + "=" * 60)
    print("🎉 ACCOUNT CREATION IN PROGRESS")
    print("=" * 60)
    print("⏳ Account is being created...")
    print("   Please wait for TikTok to process the verification")
    print("   You may need to complete a captcha if shown")
    
    # Wait for final success
    print("\n" + "=" * 60)
    print("⏳ WAITING FOR FINAL CONFIRMATION...")
    print("=" * 60)
    
    input("Press Enter once you see a success message or complete captcha...")
    
    # Save account data
    account_data = {
        'email': email,
        'password': password,
        'username': username,
        'status': 'created',
        'created_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'last_used': None,
        'cookies': {}
    }
    
    # Save to file
    import json
    accounts_file = 'accounts.json'
    
    try:
        # Load existing accounts
        if os.path.exists(accounts_file):
            with open(accounts_file, 'r') as f:
                accounts = json.load(f)
        else:
            accounts = []
        
        # Add new account
        accounts.append(account_data)
        
        # Save accounts
        with open(accounts_file, 'w') as f:
            json.dump(accounts, f, indent=2)
        
        print(f"\n✅ Account data saved to: {accounts_file}")
        logger.info(f"Account created: {email}")
        
    except Exception as e:
        logger.error(f"Failed to save account data: {e}")
        print(f"\n❌ Error saving account data: {e}")
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("\n✅ Account creation completed!")
    print("   Next steps:")
    print("   1. Check your email for verification")
    print("   2. Complete any captcha if shown")
    print("   3. Set up your TikTok profile")
    print("   4. Account saved to accounts.json")
    print("\n" + "=" * 60)
    print("🔒 Keep this session open for manual intervention...")
    print("   You can interact with the browser if needed")
    print("=" * 60)
    
    input("Press Enter to close browser and save cookies (optional)...")
    
    # Save cookies if requested
    save_cookies = input("Save session cookies? (y/n): ").strip().lower() == 'y'
    
    if save_cookies:
        try:
            cookies = driver.get_cookies()
            print(f"✅ Saved {len(cookies)} cookies")
            logger.info(f"Saved {len(cookies)} cookies")
            
            # Save cookies to account
            account_data['cookies'] = {c['name']: c['value'] for c in cookies}
            
            # Update accounts file with cookies
            if os.path.exists(accounts_file):
                with open(accounts_file, 'r') as f:
                    accounts = json.load(f)
                
                # Update the last account with cookies
                if accounts:
                    accounts[-1]['cookies'] = account_data['cookies']
                
                with open(accounts_file, 'w') as f:
                    json.dump(accounts, f, indent=2)
                
                print(f"✅ Updated {accounts_file} with cookies")
            
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
            print(f"\n❌ Error saving cookies: {e}")
    
    # Close browser
    driver.quit()
    print("\n✅ Browser closed")
    print("\n🎯 Account is ready for use!")
    print(f"   Credentials saved in: {accounts_file}")
    print("   You can now use this account with the bot's other features")
    print("=" * 60)

if __name__ == "__main__":
    main()
