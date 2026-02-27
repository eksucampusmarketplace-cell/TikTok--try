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


def signup(driver, email, password, username=None, birth_date=None, email_provider=None):
    """
    Create a new TikTok account.
    
    Args:
        driver: Selenium WebDriver instance
        email: Email address for the account
        password: Password for the account
        username: Optional username (will be generated if not provided)
        birth_date: Optional birth date dict with 'month', 'day', 'year' keys
        email_provider: Optional email provider instance for verification
    
    Returns:
        dict: Account data if successful, None otherwise
    """
    bot = TikTokBot(driver)
    
    try:
        logger.info("Starting TikTok account signup process...")
        
        # Navigate to TikTok signup page
        driver.get("https://www.tiktok.com/signup")
        time.sleep(5)
        
        # Check if we need to accept cookies
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept") or contains(text(), "Accept all")]'))
            )
            cookie_btn.click()
            logger.info("Accepted cookies")
            time.sleep(1)
        except:
            pass
        
        # Click on "Use phone or email" option
        try:
            phone_email_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Use phone or email") or contains(@data-e2e, "phone-email")]'))
            )
            phone_email_btn.click()
            logger.info("Selected phone/email signup")
            time.sleep(2)
        except TimeoutException:
            # Try alternative selectors
            try:
                alt_btn = driver.find_element(By.XPATH, '//div[contains(@class, "channel-item") and contains(text(), "email")]')
                alt_btn.click()
                logger.info("Selected email signup (alternative)")
                time.sleep(2)
            except:
                logger.error("Could not find email signup option")
                return None
        
        # Switch to email tab if needed
        try:
            email_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Email") or @data-e2e="email-tab"]'))
            )
            email_tab.click()
            logger.info("Switched to email tab")
            time.sleep(1)
        except:
            logger.info("Email tab not needed or already selected")
        
        # Fill in birth date if required
        if birth_date:
            try:
                # Month dropdown
                month_dropdown = driver.find_element(By.XPATH, '//select[contains(@name, "month") or @data-e2e="month"]')
                month_dropdown.click()
                month_option = driver.find_element(By.XPATH, f'//option[@value="{birth_date["month"]}"]')
                month_option.click()
                time.sleep(0.5)
                
                # Day dropdown
                day_dropdown = driver.find_element(By.XPATH, '//select[contains(@name, "day") or @data-e2e="day"]')
                day_dropdown.click()
                day_option = driver.find_element(By.XPATH, f'//option[@value="{birth_date["day"]}"]')
                day_option.click()
                time.sleep(0.5)
                
                # Year dropdown
                year_dropdown = driver.find_element(By.XPATH, '//select[contains(@name, "year") or @data-e2e="year"]')
                year_dropdown.click()
                year_option = driver.find_element(By.XPATH, f'//option[@value="{birth_date["year"]}"]')
                year_option.click()
                time.sleep(0.5)
                
                logger.info("Entered birth date")
                
                # Click next/continue after birth date
                try:
                    next_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Next") or contains(text(), "Continue")]')
                    next_btn.click()
                    time.sleep(2)
                except:
                    pass
                    
            except Exception as e:
                logger.warning(f"Could not enter birth date: {e}")
        else:
            # Use a default birth date (over 18)
            try:
                # Check if birth date form is visible
                month_selectors = [
                    (By.XPATH, '//select[contains(@name, "month")]'),
                    (By.XPATH, '//div[@data-e2e="month"]//select'),
                ]
                
                month_elem = bot.find_element_multiple_selectors(month_selectors, timeout=3)
                if month_elem:
                    # Select January
                    month_elem.click()
                    time.sleep(0.3)
                    driver.find_element(By.XPATH, '//option[@value="1" or text()="January"]').click()
                    
                    # Select day 15
                    day_elem = driver.find_element(By.XPATH, '//select[contains(@name, "day")]')
                    day_elem.click()
                    time.sleep(0.3)
                    driver.find_element(By.XPATH, '//option[@value="15"]').click()
                    
                    # Select year 1995
                    year_elem = driver.find_element(By.XPATH, '//select[contains(@name, "year")]')
                    year_elem.click()
                    time.sleep(0.3)
                    driver.find_element(By.XPATH, '//option[@value="1995"]').click()
                    
                    logger.info("Entered default birth date")
                    
                    # Click next
                    try:
                        next_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Next")]')
                        next_btn.click()
                        time.sleep(2)
                    except:
                        pass
            except:
                logger.info("Birth date form not present or already passed")
        
        # Enter email - try multiple selectors for different TikTok page versions
        email_selectors = [
            (By.XPATH, '//input[@type="email"]'),
            (By.XPATH, '//input[@name="email"]'),
            (By.XPATH, '//input[contains(@placeholder, "email")]'),
            (By.XPATH, '//input[@type="text"]'),
            (By.CSS_SELECTOR, 'input[type="email"]'),
            (By.CSS_SELECTOR, 'input[name="email"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="email"]'),
        ]
        
        email_input = bot.find_element_multiple_selectors(email_selectors, timeout=10)
        if email_input:
            email_input.clear()
            for char in email:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.02, 0.05))
            logger.info(f"Entered email: {email}")
        else:
            logger.error("Could not find email input field")
            return None
        
        time.sleep(1)
        
        # Click Next button after email (TikTok uses multi-step signup)
        logger.info("Looking for Next button after email...")
        next_selectors = [
            (By.XPATH, '//button[contains(text(), "Next")]'),
            (By.XPATH, '//button[@type="submit"]'),
            (By.XPATH, '//button[contains(@class, "next")]'),
            (By.CSS_SELECTOR, 'button[type="submit"]'),
            (By.XPATH, '//div[contains(@role, "button") and contains(text(), "Next")]'),
            (By.XPATH, '//button//span[contains(text(), "Next")]'),
            (By.XPATH, '//input[@type="submit"]'),
        ]
        
        next_clicked = False
        for selector in next_selectors:
            try:
                next_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(selector)
                )
                next_btn.click()
                logger.info("Clicked Next button after email")
                next_clicked = True
                time.sleep(3)
                break
            except:
                continue
        
        if not next_clicked:
            # Try pressing Enter as fallback
            try:
                from selenium.webdriver.common.keys import Keys
                email_input.send_keys(Keys.ENTER)
                logger.info("Pressed Enter to proceed")
                time.sleep(3)
            except:
                pass
        
        time.sleep(2)
        
        # Enter password - try multiple selectors for different TikTok page versions
        logger.info("Looking for password input field...")
        password_selectors = [
            (By.XPATH, '//input[@type="password"]'),
            (By.XPATH, '//input[@name="password"]'),
            (By.XPATH, '//input[contains(@placeholder, "password")]'),
            (By.CSS_SELECTOR, 'input[type="password"]'),
            (By.CSS_SELECTOR, 'input[name="password"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="password"]'),
            (By.XPATH, '//div[contains(@class, "password")]//input'),
            (By.XPATH, '//input[contains(@class, "password")]'),
            (By.XPATH, '//input[@autocomplete="new-password"]'),
            (By.XPATH, '//input[@id="password"]'),
        ]
        
        password_input = None
        for _ in range(3):  # Try 3 times with delays
            password_input = bot.find_element_multiple_selectors(password_selectors, timeout=10)
            if password_input:
                break
            logger.info("Password field not found, waiting...")
            time.sleep(3)
        
        if password_input:
            try:
                password_input.clear()
            except:
                pass
            for char in password:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.02, 0.05))
            logger.info("Entered password")
        else:
            logger.error("Could not find password input field")
            logger.info("Page source snippet for debugging:")
            try:
                # Log some page info for debugging
                page_url = driver.current_url
                logger.info(f"Current URL: {page_url}")
            except:
                pass
            return None
        
        time.sleep(1)
        
        # Enter username if field is present
        if username:
            username_selectors = [
                (By.XPATH, '//input[@name="username"]'),
                (By.XPATH, '//input[contains(@placeholder, "username")]'),
            ]
            
            username_input = bot.find_element_multiple_selectors(username_selectors, timeout=5)
            if username_input:
                username_input.clear()
                for char in username:
                    username_input.send_keys(char)
                    time.sleep(random.uniform(0.02, 0.05))
                logger.info(f"Entered username: {username}")
        
        # Click sign up button
        signup_selectors = [
            (By.XPATH, '//button[@type="submit"]'),
            (By.XPATH, '//button[contains(text(), "Sign up")]'),
            (By.XPATH, '//button[contains(text(), "Next")]'),
        ]
        
        for selector in signup_selectors:
            try:
                signup_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(selector)
                )
                signup_btn.click()
                logger.info("Clicked signup button")
                break
            except:
                continue
        
        time.sleep(5)
        
        # Check for captcha
        try:
            captcha_frame = driver.find_element(By.XPATH, '//iframe[contains(@src, "captcha")]')
            logger.warning("Captcha detected! Manual intervention required.")
            print("\n" + "="*60)
            print("CAPTCHA DETECTED!")
            print("Please solve the captcha manually in the browser window.")
            print("="*60 + "\n")
            
            # Wait for user to solve captcha
            input("Press Enter after solving the captcha...")
            time.sleep(3)
        except:
            pass
        
        # Check for email verification
        try:
            verification_code_input = driver.find_element(By.XPATH, '//input[contains(@placeholder, "code") or @name="code"]')
            logger.info("Email verification code required")
            
            if email_provider:
                # Wait for verification email
                print("\n" + "="*60)
                print(f"Waiting for verification email at: {email}")
                print("This may take up to 2 minutes...")
                print("="*60 + "\n")
                
                verification_email = email_provider.wait_for_email(email, timeout=120)
                
                if verification_email:
                    # Extract verification code from email body
                    import re
                    body = verification_email.get('body', '')
                    code_match = re.search(r'\b(\d{4,6})\b', body)
                    
                    if code_match:
                        code = code_match.group(1)
                        logger.info(f"Found verification code: {code}")
                        
                        verification_code_input.clear()
                        for char in code:
                            verification_code_input.send_keys(char)
                            time.sleep(0.1)
                        
                        logger.info("Entered verification code")
                        time.sleep(2)
                    else:
                        print(f"\nEmail body: {body[:500]}")
                        code = input("Enter the verification code manually: ").strip()
                        verification_code_input.clear()
                        verification_code_input.send_keys(code)
                        time.sleep(2)
                else:
                    code = input("Enter the verification code manually: ").strip()
                    verification_code_input.clear()
                    verification_code_input.send_keys(code)
                    time.sleep(2)
            else:
                print("\n" + "="*60)
                print(f"Please check your email: {email}")
                print("Enter the verification code from TikTok's email.")
                print("="*60 + "\n")
                code = input("Enter the verification code: ").strip()
                verification_code_input.clear()
                verification_code_input.send_keys(code)
                time.sleep(2)
                
        except NoSuchElementException:
            logger.info("No verification code input found - account may be created")
        
        # Wait for account creation to complete
        time.sleep(5)
        
        # Check if we're on the home page or if account was created
        current_url = driver.current_url
        
        if 'signup' not in current_url.lower() or 'foryou' in current_url.lower():
            logger.info("Account creation successful!")
            
            # Get cookies
            cookies = driver.get_cookies()
            
            # Generate username if not provided
            if not username:
                username = f"user{random.randint(100000, 999999)}"
            
            account_data = {
                'email': email,
                'password': password,
                'username': username,
                'status': 'active',
                'created_at': datetime.now().isoformat(),
                'cookies': cookies,
                'last_used': None
            }
            
            log_report(f"Created TikTok account: {email}")
            return account_data
        else:
            logger.warning("Account creation may need additional steps")
            print("\nPlease complete any remaining steps in the browser window.")
            input("Press Enter when done...")
            
            cookies = driver.get_cookies()
            
            if not username:
                username = f"user{random.randint(100000, 999999)}"
            
            account_data = {
                'email': email,
                'password': password,
                'username': username,
                'status': 'created',
                'created_at': datetime.now().isoformat(),
                'cookies': cookies,
                'last_used': None
            }
            
            return account_data
            
    except Exception as e:
        logger.error(f"Error during signup: {e}")
        return None


def check_username_availability(driver, username):
    """
    Check if a TikTok username is available.
    
    Args:
        driver: Selenium WebDriver instance
        username: Username to check
    
    Returns:
        bool: True if username is available
    """
    try:
        driver.get(f"https://www.tiktok.com/@{username}")
        time.sleep(3)
        
        # Check if we got a "user not found" page
        page_source = driver.page_source.lower()
        if 'couldn\'t find this account' in page_source or 'user not found' in page_source:
            logger.info(f"Username @{username} is available")
            return True
        
        logger.info(f"Username @{username} is taken")
        return False
        
    except Exception as e:
        logger.error(f"Error checking username: {e}")
        return False


# Maintain backward compatibility with the old class name
tiktok_bot = TikTokBot
