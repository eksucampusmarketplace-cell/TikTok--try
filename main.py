"""
TikTok Automation Bot - Main Entry Point

This bot automates various TikTok tasks including:
- Login (cookie-based or manual)
- Commenting on user videos
- Following users
- Video uploading
"""
import time
import os
import sys
import logging
from seleniumbase import Driver

# Import configuration and bot modules
import config
from social_media import tiktok

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
            print("5. Exit")
            print("-" * 60)
            
            choice = input("\nSelect a task (1-5): ").strip()
            
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
