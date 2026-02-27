"""
TikTok Automation Bot - Main Entry Point

This bot automates various TikTok tasks including:
- Login (cookie-based or manual)
- Commenting on user videos
- Following users
- Video uploading
- Multi-account management
- Account creation with proxy support
"""
import time
import os
import sys
import random
import logging
from seleniumbase import Driver

# Import configuration and bot modules
import config
from social_media import tiktok
from account_manager import AccountManager, AccountCreator
from proxy_manager import ProxyManager
from email_generator import EmailGenerator
from multi_account_bot import MultiAccountBotManager

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


def initialize_driver():
    """
    Initialize and return the Selenium WebDriver.
    
    Returns:
        WebDriver: Configured Selenium driver instance
    """
    try:
        logger.info("Initializing WebDriver...")
        
        # Driver configuration based on settings
        driver_args = {
            'headless': config.HEADLESS,
        }
        
        # Use undetected-chromedriver mode if configured
        if config.BROWSER_MODE == "uc":
            driver_args['uc'] = True
            logger.info("Using undetected-chromedriver mode")
        
        driver = Driver(**driver_args)
        driver.maximize_window()
        
        logger.info("WebDriver initialized successfully")
        return driver
        
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        sys.exit(1)


def run_bot():
    """
    Main bot function that handles TikTok automation tasks.
    """
    # Initialize driver
    driver = initialize_driver()
    
    try:
        # Get credentials
        email = config.TIKTOK_EMAIL
        password = config.TIKTOK_PASSWORD
        
        # Prompt for credentials if not provided
        if email == "youremail@example.com" or password == "yourpassword":
            logger.info("Please provide your TikTok credentials:")
            email = input("Email: ").strip()
            password = input("Password: ").strip()
        
        # Load cookies for login
        cookies = tiktok.load_cookies(config.COOKIE_FILE)

        # Perform login
        logger.info("Attempting to login...")
        login_success = tiktok.login(driver, email, password, cookies)
        
        if not login_success:
            logger.warning("Login was not fully successful. You may need to complete some steps manually.")
            input("Press Enter after completing any manual steps to continue...")
        
        # Task 1: Comment on user videos
        logger.info("=" * 60)
        logger.info("TASK: Commenting on user videos")
        logger.info("=" * 60)
        
        if config.DEFAULT_COMMENT_COUNT > 0:
            try:
                comments_posted = tiktok.comment_user_video(
                    driver,
                    config.DEFAULT_COMMENT_USER,
                    config.COMMENTS,
                    config.DEFAULT_COMMENT_COUNT
                )
                logger.info(f"Comment task completed. Posted {comments_posted}/{config.DEFAULT_COMMENT_COUNT} comments")
            except Exception as e:
                logger.error(f"Comment task failed: {e}")
        else:
            logger.info("Comment task skipped (comment count set to 0)")
        
        time.sleep(5)

        # Task 2: Follow user
        logger.info("=" * 60)
        logger.info("TASK: Following user")
        logger.info("=" * 60)
        
        if config.DEFAULT_FOLLOW_USER:
            try:
                follow_success = tiktok.follow(driver, config.DEFAULT_FOLLOW_USER)
                if follow_success:
                    logger.info(f"Follow task completed successfully")
                else:
                    logger.warning("Follow task may not have completed successfully")
            except Exception as e:
                logger.error(f"Follow task failed: {e}")
        else:
            logger.info("Follow task skipped (no user specified)")
        
        time.sleep(3)

        # Task 3: Upload video
        logger.info("=" * 60)
        logger.info("TASK: Uploading video")
        logger.info("=" * 60)
        
        if os.path.exists(config.VIDEO_FILE_PATH):
            try:
                upload_success = tiktok.upload(
                    driver,
                    config.VIDEO_FILE_PATH,
                    config.DEFAULT_VIDEO_CAPTION
                )
                if upload_success:
                    logger.info("Upload task initiated successfully")
                else:
                    logger.warning("Upload task may not have completed successfully")
            except Exception as e:
                logger.error(f"Upload task failed: {e}")
        else:
            logger.info(f"Upload task skipped (video file not found: {config.VIDEO_FILE_PATH})")
            logger.info("To enable video upload, place your video file at the specified path or update config.py")

        # Final message
        logger.info("=" * 60)
        logger.info("Bot execution completed!")
        logger.info("=" * 60)
        
        # Allow some time before closing for user to see results
        logger.info("Waiting 10 seconds before closing...")
        time.sleep(10)
        
    except KeyboardInterrupt:
        logger.info("Bot execution interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error during bot execution: {e}", exc_info=True)
    finally:
        # Clean up
        logger.info("Closing driver...")
        try:
            driver.quit()
        except:
            pass


def multi_account_menu():
    """
    Display multi-account management menu.
    """
    while True:
        print("\n" + "=" * 60)
        print("Multi-Account Management")
        print("=" * 60)
        print("1. View all accounts")
        print("2. Add new account")
        print("3. Import accounts from file")
        print("4. Delete account")
        print("5. Enable/Disable account")
        print("6. Execute task on all accounts")
        print("7. Batch comment with multiple accounts")
        print("8. Batch follow with multiple accounts")
        print("9. Account creation wizard")
        print("10. Proxy management")
        print("11. Back to main menu")
        print("-" * 60)
        
        choice = input("\nSelect an option (1-11): ").strip()
        
        account_manager = AccountManager(config.ACCOUNTS_FILE)
        
        if choice == "1":
            # View all accounts
            print("\n" + "-" * 60)
            print("All Accounts:")
            print("-" * 60)
            accounts = account_manager.get_all_accounts()
            
            if not accounts:
                print("No accounts found.")
            else:
                for i, account in enumerate(accounts, 1):
                    status = account.get('status', 'unknown')
                    print(f"{i}. {account.get('email')} - Status: {status}")
                    if account.get('proxy'):
                        print(f"   Proxy: {account['proxy']['host']}:{account['proxy']['port']}")
                    print()
        
        elif choice == "2":
            # Add new account
            print("\n" + "-" * 60)
            print("Add New Account")
            print("-" * 60)
            
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            username = input("Username (optional): ").strip()
            
            account_data = {
                'email': email,
                'password': password,
                'username': username if username else None
            }
            
            # Ask about proxy
            use_proxy = input("Use proxy? (y/n): ").strip().lower()
            if use_proxy == 'y':
                proxy_host = input("Proxy host: ").strip()
                proxy_port = input("Proxy port: ").strip()
                proxy_protocol = input("Proxy protocol (http/https): ").strip() or "http"
                
                account_data['proxy'] = {
                    'host': proxy_host,
                    'port': int(proxy_port),
                    'protocol': proxy_protocol
                }
            
            if account_manager.add_account(account_data):
                print(f"\n✓ Account added successfully: {email}")
            else:
                print(f"\n✗ Failed to add account: {email}")
        
        elif choice == "3":
            # Import accounts from file
            filepath = input("Enter file path (JSON or TXT): ").strip()
            if os.path.exists(filepath):
                count = account_manager.import_accounts(filepath)
                print(f"\n✓ Imported {count} accounts")
            else:
                print(f"\n✗ File not found: {filepath}")
        
        elif choice == "4":
            # Delete account
            email = input("Enter account email to delete: ").strip()
            if account_manager.delete_account(email):
                print(f"\n✓ Account deleted: {email}")
            else:
                print(f"\n✗ Failed to delete account: {email}")
        
        elif choice == "5":
            # Enable/Disable account
            email = input("Enter account email: ").strip()
            action = input("Enable or disable? (e/d): ").strip().lower()
            
            if action == 'e':
                if account_manager.enable_account(email):
                    print(f"\n✓ Account enabled: {email}")
                else:
                    print(f"\n✗ Failed to enable account")
            elif action == 'd':
                if account_manager.disable_account(email):
                    print(f"\n✓ Account disabled: {email}")
                else:
                    print(f"\n✗ Failed to disable account")
            else:
                print("\n✗ Invalid option")
        
        elif choice == "6":
            # Execute task on all accounts
            print("\n" + "-" * 60)
            print("Execute Task on All Accounts")
            print("-" * 60)
            print("Available tasks:")
            print("1. Comment on user videos")
            print("2. Follow user")
            
            task_choice = input("Select task (1-2): ").strip()
            
            if task_choice == "1":
                user = input("Enter username to comment on: ").strip()
                count = int(input("Comments per account: ").strip())
                
                # Initialize multi-account manager
                proxy_manager = ProxyManager(config.PROXIES_FILE) if config.USE_PROXIES else None
                multi_bot = MultiAccountBotManager(account_manager, proxy_manager, config.MAX_CONCURRENT_BOTS)
                
                results = multi_bot.batch_comment(user, config.COMMENTS, count)
                
                successful = sum(1 for r in results.values() if r)
                print(f"\n✓ Completed: {successful}/{len(results)} accounts")
                
            elif task_choice == "2":
                users_input = input("Enter usernames (comma-separated): ").strip()
                users = [u.strip() for u in users_input.split(',')]
                
                proxy_manager = ProxyManager(config.PROXIES_FILE) if config.USE_PROXIES else None
                multi_bot = MultiAccountBotManager(account_manager, proxy_manager, config.MAX_CONCURRENT_BOTS)
                
                results = multi_bot.batch_follow(users)
                
                print(f"\n✓ Batch follow completed")
            else:
                print("\n✗ Invalid task selection")
        
        elif choice == "7":
            # Batch comment
            user = input("Enter username to comment on: ").strip()
            count = int(input("Comments per account: ").strip())
            
            proxy_manager = ProxyManager(config.PROXIES_FILE) if config.USE_PROXIES else None
            multi_bot = MultiAccountBotManager(account_manager, proxy_manager, config.MAX_CONCURRENT_BOTS)
            
            print(f"\nExecuting batch comment with {account_manager.get_account_count(status='active')} accounts...")
            results = multi_bot.batch_comment(user, config.COMMENTS, count)
            
            successful = sum(1 for r in results.values() if r)
            print(f"\n✓ Completed: {successful}/{len(results)} accounts")
        
        elif choice == "8":
            # Batch follow
            users_input = input("Enter usernames (comma-separated): ").strip()
            users = [u.strip() for u in users_input.split(',')]
            
            proxy_manager = ProxyManager(config.PROXIES_FILE) if config.USE_PROXIES else None
            multi_bot = MultiAccountBotManager(account_manager, proxy_manager, config.MAX_CONCURRENT_BOTS)
            
            print(f"\nExecuting batch follow with {account_manager.get_account_count(status='active')} accounts...")
            results = multi_bot.batch_follow(users)
            
            print(f"\n✓ Batch follow completed")
        
        elif choice == "9":
            # Account creation wizard
            account_creation_wizard(account_manager)
        
        elif choice == "10":
            # Proxy management
            proxy_management_menu()
        
        elif choice == "11":
            # Back to main menu
            break
        else:
            print("\n✗ Invalid choice")


def account_creation_wizard(account_manager: AccountManager):
    """
    Account creation wizard.
    """
    print("\n" + "=" * 60)
    print("Account Creation Wizard")
    print("=" * 60)
    
    # Email strategy selection
    print("\nSelect Email Strategy:")
    print("1. Random (for testing - won't work for real accounts)")
    print("2. Guerrilla Mail (temp mail service)")
    print("3. 10 Minute Mail (temp mail service)")
    print("4. Temp Mail (temp-mail.org)")
    print("5. Custom Email List (use your own emails)")
    print("-" * 60)
    
    strategy_choice = input("Select email strategy (1-5): ").strip()
    
    strategy_map = {
        '1': 'random',
        '2': 'guerrillamail',
        '3': '10minutemail',
        '4': 'tempmail',
        '5': 'custom'
    }
    
    strategy = strategy_map.get(strategy_choice)
    if not strategy:
        print("\n✗ Invalid choice. Using default strategy.")
        strategy = config.EMAIL_GENERATION_STRATEGY
    
    # Initialize managers
    proxy_manager = ProxyManager(config.PROXIES_FILE) if config.USE_PROXIES else None
    email_generator = EmailGenerator(
        strategy=strategy,
        domains=config.EMAIL_DOMAINS,
        emails_file=config.CUSTOM_EMAILS_FILE
    )
    
    account_creator = AccountCreator(account_manager, proxy_manager, email_generator)
    
    print(f"\nAccount creation will:")
    print(f"- Use {strategy} email strategy")
    print("- Generate secure passwords")
    print("- Assign proxies (if enabled)")
    print("- Create TikTok accounts")
    print("\n⚠️ Note: Actual TikTok account creation requires manual verification")
    print("   (email/phone verification, captcha, etc.)")
    print("   This will create the account data structure for you.")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("\n✗ Account creation cancelled")
        return
    
    count = int(input(f"How many accounts to create? (default: {config.ACCOUNTS_TO_CREATE}): ").strip() or str(config.ACCOUNTS_TO_CREATE))
    
    print(f"\nCreating {count} accounts...")
    
    # Create driver for account creation
    try:
        driver = initialize_driver()
        
        for i in range(count):
            print(f"\n[{i+1}/{count}] Creating account...")
            
            account = account_creator.create_account(driver, use_proxy=config.USE_PROXIES)
            
            if account:
                print(f"✓ Created: {account['email']}")
                print(f"  Password: {account['password']}")
                print(f"  Proxy: {account.get('proxy', 'None')}")
            else:
                print(f"✗ Failed to create account")
            
            # Delay between account creations
            if i < count - 1:
                delay = random.uniform(5, 15)
                print(f"  Waiting {delay:.1f}s before next account...")
                time.sleep(delay)
        
        driver.quit()
        
    except Exception as e:
        logger.error(f"Error during account creation: {e}")
        print(f"\n✗ Error: {e}")


def proxy_management_menu():
    """
    Proxy management menu.
    """
    print("\n" + "=" * 60)
    print("Proxy Management")
    print("=" * 60)
    
    proxy_manager = ProxyManager(config.PROXIES_FILE)
    
    while True:
        print("\nOptions:")
        print("1. View all proxies")
        print("2. Add proxy")
        print("3. Import proxies from file")
        print("4. Delete proxy")
        print("5. Check proxy")
        print("6. Back")
        print("-" * 60)
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == "1":
            # View all proxies
            print("\n" + "-" * 60)
            print("All Proxies:")
            print("-" * 60)
            proxies = proxy_manager.get_all_proxies()
            
            if not proxies:
                print("No proxies found.")
            else:
                for i, proxy in enumerate(proxies, 1):
                    status = proxy.get('status', 'unknown')
                    print(f"{i}. {proxy['host']}:{proxy['port']} ({proxy['protocol']}) - Status: {status}")
                    if proxy.get('username'):
                        print(f"   Auth: {proxy['username']}:****")
                    print()
        
        elif choice == "2":
            # Add proxy
            print("\n" + "-" * 60)
            print("Add Proxy")
            print("-" * 60)
            
            host = input("Proxy host: ").strip()
            port = input("Proxy port: ").strip()
            protocol = input("Protocol (http/https): ").strip() or "http"
            username = input("Username (optional): ").strip()
            password = input("Password (optional): ").strip()
            
            proxy_data = {
                'host': host,
                'port': int(port),
                'protocol': protocol
            }
            
            if username and password:
                proxy_data['username'] = username
                proxy_data['password'] = password
            
            if proxy_manager.add_proxy(proxy_data):
                print(f"\n✓ Proxy added: {host}:{port}")
            else:
                print(f"\n✗ Failed to add proxy")
        
        elif choice == "3":
            # Import proxies
            filepath = input("Enter file path: ").strip()
            if os.path.exists(filepath):
                count = proxy_manager.import_proxies(filepath)
                print(f"\n✓ Imported {count} proxies")
            else:
                print(f"\n✗ File not found: {filepath}")
        
        elif choice == "4":
            # Delete proxy
            proxy_str = input("Enter proxy (host:port): ").strip()
            if proxy_manager.delete_proxy(proxy_str):
                print(f"\n✓ Proxy deleted: {proxy_str}")
            else:
                print(f"\n✗ Failed to delete proxy")
        
        elif choice == "5":
            # Check proxy
            proxy_str = input("Enter proxy (host:port): ").strip()
            proxy_data = proxy_manager.get_proxy()
            
            if proxy_data:
                if proxy_manager.check_proxy(proxy_data):
                    print(f"\n✓ Proxy is working")
                else:
                    print(f"\n✗ Proxy is not working")
            else:
                print(f"\n✗ No proxies available")
        
        elif choice == "6":
            # Back
            break
        else:
            print("\n✗ Invalid choice")


def interactive_mode():
    """
    Run the bot in interactive mode, allowing user to choose tasks.
    """
    print("\n" + "=" * 60)
    print("TikTok Automation Bot - Interactive Mode")
    print("=" * 60)
    
    # Initialize driver
    driver = initialize_driver()
    
    try:
        # Get credentials
        email = config.TIKTOK_EMAIL
        password = config.TIKTOK_PASSWORD
        
        if email == "youremail@example.com" or password == "yourpassword":
            print("\nPlease provide your TikTok credentials:")
            email = input("Email: ").strip()
            password = input("Password: ").strip()
        
        # Login
        cookies = tiktok.load_cookies(config.COOKIE_FILE)
        login_success = tiktok.login(driver, email, password, cookies)
        
        if not login_success:
            input("\nPress Enter after completing any manual login steps...")
        
        while True:
            print("\n" + "-" * 60)
            print("Available tasks:")
            print("1. Comment on user videos")
            print("2. Follow a user")
            print("3. Upload a video")
            print("4. Run all default tasks")
            print("5. Multi-Account Management")
            print("6. Exit")
            print("-" * 60)
            
            choice = input("\nSelect a task (1-6): ").strip()
            
            if choice == "1":
                # Comment task
                user = input("Enter username to comment on: ").strip()
                count = int(input("Enter number of comments: ").strip())
                
                comments_posted = tiktok.comment_user_video(
                    driver,
                    user,
                    config.COMMENTS,
                    count
                )
                print(f"\nPosted {comments_posted}/{count} comments")
            
            elif choice == "2":
                # Follow task
                user = input("Enter username to follow: ").strip()
                
                success = tiktok.follow(driver, user)
                if success:
                    print(f"\nSuccessfully followed @{user}")
                else:
                    print(f"\nFailed to follow @{user}")
            
            elif choice == "3":
                # Upload task
                path = input("Enter path to video file: ").strip()
                caption = input("Enter video caption: ").strip() or config.DEFAULT_VIDEO_CAPTION
                
                success = tiktok.upload(driver, path, caption)
                if success:
                    print(f"\nUpload initiated successfully")
                else:
                    print(f"\nUpload failed")
            
            elif choice == "4":
                # Run all tasks
                print("\nRunning all default tasks...")
                comments_posted = tiktok.comment_user_video(
                    driver,
                    config.DEFAULT_COMMENT_USER,
                    config.COMMENTS,
                    config.DEFAULT_COMMENT_COUNT
                )
                
                tiktok.follow(driver, config.DEFAULT_FOLLOW_USER)
                
                if os.path.exists(config.VIDEO_FILE_PATH):
                    tiktok.upload(driver, config.VIDEO_FILE_PATH, config.DEFAULT_VIDEO_CAPTION)
                else:
                    print("Video file not found, skipping upload")
                
                print("\nAll tasks completed!")
            
            elif choice == "5":
                # Multi-Account Management
                multi_account_menu()
            
            elif choice == "6":
                # Exit
                print("\nExiting...")
                break
            
            else:
                print("\nInvalid choice. Please try again.")
        
    except KeyboardInterrupt:
        print("\n\nExiting due to user interrupt...")
    except Exception as e:
        logger.error(f"Error in interactive mode: {e}", exc_info=True)
    finally:
        driver.quit()


if __name__ == "__main__":
    # Print welcome message
    print("""
    **************************************************
    Welcome to the TikTok Automation Bot!
    
    Developed by: mysterecode (mysteredev)
    Available for collaboration and freelance projects.
    
    Contact me on Telegram: mysteredev
    **************************************************
    """)
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Run in interactive mode
        interactive_mode()
    else:
        # Run in default automated mode
        run_bot()
