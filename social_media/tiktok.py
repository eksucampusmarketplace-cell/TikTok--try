import time
import json
import random
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

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


class TikTokBot:
    """Enhanced TikTok automation bot with better error handling and logging."""
    
    def __init__(self, driver):
        self.driver = driver
        self.retries = 3
        self.wait_time = 10
    
    def wait_and_click(self, path, timeout=10, description="element"):
        """Wait for an element to be clickable and click it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, path))
            )
            element.click()
            logger.info(f"Successfully clicked on {description}")
            return True
        except TimeoutException:
            logger.error(f"Timeout waiting for {description} with path: {path}")
            return False
        except Exception as e:
            logger.error(f"Error clicking {description}: {e}")
            return False
    
    def wait_and_type(self, path, text, timeout=10, description="element", human_like=True):
        """Wait for an element and type text into it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            
            if human_like:
                # Type with human-like delays
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.02, 0.08))
            else:
                element.send_keys(text)
            
            logger.info(f"Successfully typed text into {description}")
            return True
        except TimeoutException:
            logger.error(f"Timeout waiting for {description} with path: {path}")
            return False
        except Exception as e:
            logger.error(f"Error typing into {description}: {e}")
            return False
    
    def wait_and_comment(self, path, text, timeout=10, description="comment box"):
        """Wait for a comment box, type text and submit."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            
            # Type with human-like delays
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(0.02, 0.08))
            
            # Submit with Enter key
            element.send_keys(Keys.ENTER)
            logger.info(f"Successfully posted comment: {text[:50]}...")
            return True
        except TimeoutException:
            logger.error(f"Timeout waiting for {description} with path: {path}")
            return False
        except Exception as e:
            logger.error(f"Error posting comment: {e}")
            return False
    
    def find_element_multiple_selectors(self, selectors, timeout=10):
        """Try multiple selectors to find an element."""
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(selector)
                )
                return element
            except TimeoutException:
                continue
        return None
    
    def scroll_to_element(self, element):
        """Scroll to make an element visible."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            return True
        except Exception as e:
            logger.error(f"Error scrolling to element: {e}")
            return False


def save_cookies(cookies, filename):
    """Save cookies to a file."""
    try:
        with open(filename, 'w') as file:
            json.dump(cookies, file)
        logger.info(f"Cookies saved to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving cookies: {e}")
        return False


def load_cookies(filename):
    """Load cookies from a file."""
    try:
        with open(filename, 'r') as file:
            cookies = json.load(file)
            logger.info(f"Cookies loaded from {filename}")
            return cookies
    except FileNotFoundError:
        logger.warning(f"Cookie file {filename} not found")
        return None
    except Exception as e:
        logger.error(f"Error loading cookies: {e}")
        return None


def login(driver, email, password, cookies):
    """
    Login to TikTok using cookies or credentials.
    
    Args:
        driver: Selenium WebDriver instance
        email: TikTok email/username
        password: TikTok password
        cookies: Optional cookies for auto-login
    
    Returns:
        bool: True if login successful, False otherwise
    """
    bot = TikTokBot(driver)
    
    try:
        # Navigate to TikTok homepage first
        logger.info("Navigating to TikTok homepage...")
        driver.get("https://www.tiktok.com")
        time.sleep(3)

        # Check if cookies are available for login
        if cookies:
            logger.info("Attempting to login with cookies...")
            try:
                # Load cookies into the browser
                for cookie in cookies:
                    try:
                        driver.add_cookie(cookie)
                    except Exception as e:
                        logger.warning(f"Failed to add cookie: {e}")

                # Refresh to apply cookies
                driver.refresh()
                time.sleep(5)

                # Check if we're logged in by looking for login elements
                try:
                    WebDriverWait(driver, 10).until_not(
                        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Log in")]'))
                    )
                    logger.info("Successfully logged in using cookies")
                    log_report("Logged in using cookies.")
                    return True
                except TimeoutException:
                    logger.warning("Cookie login may have failed, trying manual login...")
            except Exception as e:
                logger.error(f"Error during cookie login: {e}")

        # No cookies or cookie login failed, proceed with manual login
        logger.info("Attempting manual login...")
        driver.get('https://www.tiktok.com/login/phone-or-email/email')
        time.sleep(5)

        # Multiple selector strategies for email input
        email_selectors = [
            (By.XPATH, '//input[@type="text"]'),
            (By.XPATH, '//input[@name="username"]'),
            (By.XPATH, '//input[contains(@placeholder, "email")]'),
        ]
        
        # Multiple selector strategies for password input
        password_selectors = [
            (By.XPATH, '//input[@type="password"]'),
            (By.XPATH, '//input[@name="password"]'),
            (By.XPATH, '//input[contains(@placeholder, "password")]'),
        ]
        
        # Find and fill email
        email_element = bot.find_element_multiple_selectors(email_selectors, timeout=15)
        if email_element:
            email_element.clear()
            for char in email:
                email_element.send_keys(char)
                time.sleep(0.05)
            logger.info("Email entered")
        else:
            logger.error("Could not find email input field")
            return False
        
        time.sleep(1)
        
        # Find and fill password
        password_element = bot.find_element_multiple_selectors(password_selectors, timeout=10)
        if password_element:
            password_element.clear()
            for char in password:
                password_element.send_keys(char)
                time.sleep(0.05)
            logger.info("Password entered")
        else:
            logger.error("Could not find password input field")
            return False
        
        time.sleep(1)

        start_url = driver.current_url

        # Try multiple submit button strategies
        submit_selectors = [
            (By.XPATH, '//button[@type="submit"]'),
            (By.XPATH, '//button[contains(text(), "Log in")]'),
            (By.XPATH, '//button[contains(@class, "submit")]'),
        ]
        
        submit_clicked = False
        for selector in submit_selectors:
            try:
                submit_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(selector)
                )
                submit_button.click()
                submit_clicked = True
                logger.info("Login form submitted")
                break
            except TimeoutException:
                continue
        
        if not submit_clicked:
            logger.warning("Could not find submit button, trying Enter key...")
            password_element.send_keys(Keys.ENTER)

        # Wait for login to process
        time.sleep(10)

        # Check if login failed by comparing URLs
        if driver.current_url == start_url or 'login' in driver.current_url:
            logger.warning("Automatic login may have failed. Please log in manually.")
            log_report("Manual login required.")
            return False

        # Get cookies after successful login
        cookies = driver.get_cookies()
        save_cookies(cookies, 'tiktok_cookies.txt')
        
        logger.info("Login successful. Credentials saved for future sessions.")
        log_report("Logged in successfully with credentials.")
        return True
        
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return False


def comment_user_video(driver, user, comments, n):
    """
    Posts comments on a user's TikTok videos.
    
    Args:
        driver: Selenium WebDriver instance
        user: TikTok username
        comments: List of comments to choose from
        n: Number of comments to post
    
    Returns:
        int: Number of successfully posted comments
    """
    bot = TikTokBot(driver)
    successful_comments = 0
    
    try:
        # Navigate to the user's TikTok profile
        logger.info(f"Navigating to @{user}'s profile...")
        driver.get(f"https://www.tiktok.com/@{user}")
        time.sleep(5)

        # Wait for the user profile to fully load with multiple selectors
        video_selectors = [
            (By.XPATH, '//div[@data-e2e="user-post-item"]'),
            (By.XPATH, '//div[contains(@class, "video-card")]'),
            (By.XPATH, '//a[contains(@href, "/video/")]'),
        ]
        
        first_video = bot.find_element_multiple_selectors(video_selectors, timeout=15)
        if not first_video:
            logger.error(f"Could not find videos on @{user}'s profile")
            return 0

        # Click on the first video
        first_video.click()
        logger.info(f"Opened @{user}'s video")
        time.sleep(3)

        # Loop to post multiple comments
        for i in range(n):
            try:
                comment = random.choice(comments)
                logger.info(f"Attempting to post comment {i+1}/{n}: {comment[:50]}...")

                # Multiple selector strategies for comment input
                comment_selectors = [
                    (By.XPATH, '//div[@role="textbox"]'),
                    (By.XPATH, '//textarea[@placeholder="Add comment..."]'),
                    (By.XPATH, '//div[contains(@class, "comment-input")]'),
                ]
                
                comment_input = bot.find_element_multiple_selectors(comment_selectors, timeout=10)
                if not comment_input:
                    logger.warning(f"Could not find comment input for comment {i+1}")
                    continue

                # Type the comment
                for char in comment:
                    comment_input.send_keys(char)
                    time.sleep(random.uniform(0.02, 0.08))
                
                # Submit with Enter
                comment_input.send_keys(Keys.ENTER)
                time.sleep(2)
                
                successful_comments += 1
                logger.info(f"Successfully posted comment {i+1} on @{user}'s video")
                log_report(f"Posted comment on @{user}'s video: {comment[:50]}...")

                # Random delay between comments to appear more natural
                if i < n - 1:
                    time.sleep(random.uniform(3, 6))

            except Exception as e:
                logger.error(f"Error posting comment {i+1}: {e}")
                continue

        logger.info(f"Successfully posted {successful_comments}/{n} comments on @{user}'s videos")
        return successful_comments
        
    except Exception as e:
        logger.error(f"Error in comment_user_video: {e}")
        return successful_comments


def follow(driver, user):
    """
    Follow a TikTok user.
    
    Args:
        driver: Selenium WebDriver instance
        user: TikTok username to follow
    
    Returns:
        bool: True if successful, False otherwise
    """
    bot = TikTokBot(driver)
    
    try:
        logger.info(f"Navigating to @{user}'s profile to follow...")
        driver.get(f"https://www.tiktok.com/@{user}")
        time.sleep(5)

        # Multiple selector strategies for follow button
        follow_selectors = [
            (By.XPATH, '//button[@data-e2e="follow-button"]'),
            (By.XPATH, '//button[contains(@data-e2e, "follow")]'),
            (By.XPATH, '//button[contains(text(), "Follow")]'),
            (By.XPATH, '//div[contains(@class, "follow-btn")]//button'),
        ]
        
        follow_button = bot.find_element_multiple_selectors(follow_selectors, timeout=15)
        if not follow_button:
            logger.error(f"Could not find follow button for @{user}")
            return False

        # Check if already following
        button_text = follow_button.text.lower()
        if 'following' in button_text or 'unfollow' in button_text:
            logger.info(f"Already following @{user}")
            return True

        bot.scroll_to_element(follow_button)
        follow_button.click()
        time.sleep(2)
        
        logger.info(f"Successfully followed @{user}")
        log_report(f"Followed @{user}")
        return True
        
    except Exception as e:
        logger.error(f"Error following @{user}: {e}")
        return False


def upload(driver, path, titre):
    """
    Upload a video to TikTok.
    
    Args:
        driver: Selenium WebDriver instance
        path: Path to the video file
        titre: Caption/title for the video
    
    Returns:
        bool: True if successful, False otherwise
    """
    bot = TikTokBot(driver)
    
    # Check if file exists
    import os
    if not os.path.exists(path):
        logger.error(f"Video file not found: {path}")
        return False
    
    try:
        logger.info(f"Navigating to TikTok upload page...")
        driver.get("https://www.tiktok.com/creator-center/upload")
        time.sleep(10)

        # Look for iframe (TikTok sometimes uses iframes for upload)
        try:
            iframe = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(iframe)
            logger.info("Switched to upload iframe")
            time.sleep(2)
        except TimeoutException:
            logger.info("No iframe found, continuing with main page")
        
        # Find file input
        file_selectors = [
            (By.CSS_SELECTOR, 'input[type="file"]'),
            (By.XPATH, '//input[@type="file"]'),
        ]
        
        file_input = bot.find_element_multiple_selectors(file_selectors, timeout=30)
        if not file_input:
            logger.error("Could not find file input")
            return False

        # Upload the file
        logger.info(f"Uploading video: {path}")
        file_input.send_keys(os.path.abspath(path))
        time.sleep(10)
        
        # Find and fill caption
        caption_selectors = [
            (By.XPATH, '//div[@role="combobox"]'),
            (By.XPATH, '//div[contains(@class, "caption-input")]'),
            (By.XPATH, '//textarea[contains(@placeholder, "caption")]'),
            (By.XPATH, '//div[contains(@placeholder, "caption")]'),
        ]
        
        caption_element = bot.find_element_multiple_selectors(caption_selectors, timeout=30)
        if caption_element:
            bot.scroll_to_element(caption_element)
            caption_element.click()
            time.sleep(1)
            
            # Clear any existing text
            try:
                caption_element.clear()
            except:
                pass
            
            # Type the caption
            for char in titre:
                caption_element.send_keys(char)
                time.sleep(0.05)
            
            logger.info(f"Caption added: {titre[:50]}...")
        else:
            logger.warning("Could not find caption input, continuing...")

        time.sleep(5)

        # Find and click post/upload button
        post_selectors = [
            (By.XPATH, '//button[contains(text(), "Post")]'),
            (By.XPATH, '//button[contains(@class, "post-button")]'),
            (By.XPATH, '//button[@data-e2e="post-btn"]'),
            (By.XPATH, '//button[contains(text(), "Upload")]'),
        ]
        
        # Try to find post button with more flexible matching
        try:
            # Look for any button that might be the post button
            all_buttons = driver.find_elements(By.TAG_NAME, 'button')
            for btn in all_buttons:
                btn_text = btn.text.lower()
                if 'post' in btn_text or 'upload' in btn_text:
                    if btn.is_enabled() and btn.is_displayed():
                        bot.scroll_to_element(btn)
                        btn.click()
                        logger.info("Post button clicked")
                        break
        except Exception as e:
            logger.error(f"Error clicking post button: {e}")

        time.sleep(10)
        
        logger.info(f"Video upload process initiated for '{titre}'")
        log_report(f"Video uploaded: {titre}")
        return True
        
    except Exception as e:
        logger.error(f"Error uploading video: {e}")
        return False
    finally:
        # Switch back to main content if we were in an iframe
        try:
            driver.switch_to.default_content()
        except:
            pass


def log_report(message):
    """Log a message to the report file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("report.txt", "a") as file:
            file.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        logger.error(f"Error writing to report file: {e}")


# Maintain backward compatibility with the old class name
tiktok_bot = TikTokBot
