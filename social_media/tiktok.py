import time
import json
import random
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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


def human_like_scroll(driver, scrolls=None):
    """Perform human-like scrolling behavior."""
    if scrolls is None:
        scrolls = random.randint(1, 3)
    
    for _ in range(scrolls):
        # Random scroll amount
        scroll_amount = random.randint(200, 500)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(0.5, 1.5))
        
        # Sometimes scroll back up a bit
        if random.random() > 0.7:
            driver.execute_script(f"window.scrollBy(0, -{random.randint(100, 200)});")
            time.sleep(random.uniform(0.3, 0.8))


def human_like_mouse_movement(driver, element=None):
    """Simulate human-like mouse movements."""
    try:
        actions = ActionChains(driver)
        
        # Get viewport size
        viewport_width = driver.execute_script("return window.innerWidth;")
        viewport_height = driver.execute_script("return window.innerHeight;")
        
        # Move mouse in random patterns before reaching target
        if element:
            # Get element location
            location = element.location
            size = element.size
            
            target_x = location['x'] + size['width'] // 2
            target_y = location['y'] + size['height'] // 2
            
            # Create random intermediate points
            for _ in range(random.randint(3, 6)):
                intermediate_x = random.randint(0, viewport_width)
                intermediate_y = random.randint(0, viewport_height)
                actions.move_by_offset(intermediate_x, intermediate_y)
                actions.pause(random.uniform(0.1, 0.3))
            
            # Move to element
            actions.move_to_element(element)
        else:
            # Random mouse movements
            for _ in range(random.randint(5, 10)):
                x = random.randint(0, viewport_width)
                y = random.randint(0, viewport_height)
                actions.move_by_offset(x, y)
                actions.pause(random.uniform(0.05, 0.2))
        
        actions.perform()
    except Exception as e:
        logger.debug(f"Mouse movement error: {e}")


def random_mouse_click(driver, element):
    """Click an element with human-like behavior."""
    try:
        # Move mouse to element with human-like motion
        human_like_mouse_movement(driver, element)
        
        # Small random delay
        time.sleep(random.uniform(0.1, 0.3))
        
        # Click
        element.click()
        return True
    except Exception as e:
        logger.debug(f"Click error: {e}")
        # Fallback to regular click
        try:
            element.click()
            return True
        except:
            return False


def check_and_solve_captcha(driver, max_attempts=3):
    """
    Detect and handle CAPTCHA challenges.
    Returns True if CAPTCHA was detected and handled (or needs manual intervention).
    """
    captcha_detected = False
    
    # Check for various CAPTCHA indicators
    captcha_selectors = [
        (By.XPATH, '//iframe[contains(@src, "captcha")]'),
        (By.XPATH, '//div[contains(@class, "captcha")]'),
        (By.XPATH, '//img[contains(@alt, "captcha")]'),
        (By.XPATH, '//input[@id="captcha"]'),
        (By.XPATH, '//div[contains(text(), "验证")]'),  # Chinese verification
        (By.XPATH, '//div[contains(text(), "Verify")]'),
        (By.XPATH, '//div[contains(text(), "human")]'),
        (By.XPATH, '//div[contains(@class, "verify")]'),
        (By.XPATH, '//div[@data-e2e="captcha"]'),
        (By.XPATH, '//svg[@aria-label="captcha"]'),
    ]
    
    for selector in captcha_selectors:
        try:
            element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(selector)
            )
            if element:
                captcha_detected = True
                logger.warning("CAPTCHA detected!")
                break
        except:
            continue
    
    if captcha_detected:
        print("\n" + "="*60)
        print("🤖 CAPTCHA DETECTED!")
        print("="*60)
        print("Please solve the CAPTCHA manually in the browser window.")
        print("Press Enter after completing the CAPTCHA...")
        print("="*60 + "\n")
        
        input("Press Enter after solving the CAPTCHA...")
        time.sleep(2)
        
        # Check if CAPTCHA is still present
        for selector in captcha_selectors:
            try:
                element = driver.find_element(*selector)
                if element:
                    logger.warning("CAPTCHA still present after manual intervention")
                    if max_attempts > 1:
                        return check_and_solve_captcha(driver, max_attempts - 1)
            except:
                pass
        
        logger.info("CAPTCHA appears to be resolved")
        return True
    
    return False


def simulate_human_typing(element, text, fast=False):
    """Type text with human-like delays."""
    element.clear()
    
    if fast:
        # Faster typing for some fields
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.02, 0.05))
    else:
        # Human-like typing
        for char in text:
            element.send_keys(char)
            # Random delay between keystrokes
            time.sleep(random.uniform(0.05, 0.15))
            
            # Occasionally pause (like thinking)
            if random.random() > 0.9:
                time.sleep(random.uniform(0.1, 0.3))


def random_jitter_mouse(driver):
    """Add random mouse jitter to appear more human."""
    try:
        actions = ActionChains(driver)
        for _ in range(random.randint(3, 8)):
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-50, 50)
            actions.move_by_offset(x_offset, y_offset)
            actions.pause(random.uniform(0.02, 0.08))
        actions.perform()
    except:
        pass


def check_for_blocks(driver):
    """Check if TikTok has blocked or rate-limited the request."""
    page_source = driver.page_source.lower()
    block_indicators = [
        'too many requests',
        'rate limit',
        'access denied',
        'blocked',
        'suspicious activity',
        'try again later',
        '暂时无法访问',  # Chinese - temporarily unavailable
    ]
    
    for indicator in block_indicators:
        if indicator in page_source:
            logger.warning(f"Block detected: {indicator}")
            return True
    
    return False


def wait_random(min_time=1, max_time=3):
    """Wait for a random amount of time."""
    time.sleep(random.uniform(min_time, max_time))


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


def generate_device_fingerprint():
    """Generate random device fingerprint to avoid detection."""
    import hashlib
    
    # Random screen resolutions
    resolutions = [
        (1920, 1080), (1366, 768), (1536, 864), (1440, 900),
        (1280, 720), (1600, 900), (1680, 1050), (2560, 1440)
    ]
    
    # Random user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    ]
    
    # Random timezone
    timezones = [
        "America/New_York", "America/Los_Angeles", "America/Chicago",
        "Europe/London", "Europe/Paris", "Europe/Berlin",
        "Asia/Tokyo", "Asia/Singapore", "Australia/Sydney"
    ]
    
    # Random language
    languages = ["en-US", "en-GB", "en-CA", "en-AU"]
    
    # Random platform
    platforms = ["Win32", "MacIntel", "Linux x86_64"]
    
    fingerprint = {
        'screen': random.choice(resolutions),
        'user_agent': random.choice(user_agents),
        'timezone': random.choice(timezones),
        'language': random.choice(languages),
        'platform': random.choice(platforms),
        'color_depth': random.choice([24, 32]),
        'device_memory': random.choice([4, 8, 16]),
        'hardware_concurrency': random.choice([4, 8, 12, 16]),
        'touch_support': random.choice([True, False]),
    }
    
    # Generate unique canvas fingerprint hash
    canvas_seed = f"{fingerprint['screen']}{fingerprint['platform']}{random.random()}"
    fingerprint['canvas_hash'] = hashlib.md5(canvas_seed.encode()).hexdigest()[:16]
    
    return fingerprint


def apply_fingerprint(driver, fingerprint):
    """Apply device fingerprint masking to the browser."""
    try:
        # Override navigator properties
        script = f"""
        Object.defineProperty(navigator, 'platform', {{
            get: () => '{fingerprint['platform']}'
        }});
        Object.defineProperty(navigator, 'language', {{
            get: () => '{fingerprint['language']}'
        }});
        Object.defineProperty(navigator, 'languages', {{
            get: () => ['{fingerprint['language']}']
        }});
        Object.defineProperty(navigator, 'deviceMemory', {{
            get: () => {fingerprint['device_memory']}
        }});
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            get: () => {fingerprint['hardware_concurrency']}
        }});
        Object.defineProperty(screen, 'width', {{
            get: () => {fingerprint['screen'][0]}
        }});
        Object.defineProperty(screen, 'height', {{
            get: () => {fingerprint['screen'][1]}
        }});
        Object.defineProperty(screen, 'colorDepth', {{
            get: () => {fingerprint['color_depth']}
        }});
        """
        driver.execute_script(script)
        logger.info("Applied device fingerprint masking")
        return True
    except Exception as e:
        logger.warning(f"Could not apply full fingerprint: {e}")
        return False


def setup_proxy(driver, proxy_data):
    """Configure proxy for the browser session."""
    try:
        if not proxy_data:
            return True
            
        host = proxy_data.get('host')
        port = proxy_data.get('port')
        username = proxy_data.get('username')
        password = proxy_data.get('password')
        
        # Proxy is set via ChromeOptions before browser creation
        # This function validates the proxy format
        logger.info(f"Using proxy: {host}:{port}")
        
        if username and password:
            logger.info("Proxy authentication configured")
            
        return True
    except Exception as e:
        logger.error(f"Error setting up proxy: {e}")
        return False


def wait_for_verification_code(email_provider, email, timeout=180):
    """
    Wait for and retrieve verification code from email.
    
    Args:
        email_provider: Email provider instance
        email: Email address to check
        timeout: Maximum wait time in seconds
    
    Returns:
        str: Verification code or None
    """
    import re
    
    logger.info(f"Waiting for verification email at {email}...")
    print(f"\n{'='*60}")
    print(f"Checking email: {email}")
    print(f"Timeout: {timeout} seconds")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    check_interval = 5
    
    while time.time() - start_time < timeout:
        try:
            messages = email_provider.get_inbox(email)
            
            if messages:
                for msg in messages:
                    subject = msg.get('subject', '').lower()
                    sender = msg.get('from', '').lower()
                    body = msg.get('body', '')
                    
                    # Check if it's from TikTok
                    if 'tiktok' in sender or 'tiktok' in subject or 'verification' in subject:
                        logger.info("Found TikTok verification email!")
                        
                        # Extract code using multiple patterns
                        patterns = [
                            r'\b(\d{4,6})\b',  # 4-6 digit code
                            r'code[:\s]*(\d{4,6})',
                            r'verification[:\s]*(\d{4,6})',
                            r'enter[:\s]*(\d{4,6})',
                        ]
                        
                        for pattern in patterns:
                            match = re.search(pattern, body, re.IGNORECASE)
                            if match:
                                code = match.group(1)
                                logger.info(f"Extracted verification code: {code}")
                                return code
                        
                        # If no pattern matched, show the email for manual extraction
                        print(f"\nEmail found but couldn't auto-extract code.")
                        print(f"Subject: {msg.get('subject')}")
                        print(f"Body preview: {body[:500]}")
                        
        except Exception as e:
            logger.debug(f"Error checking email: {e}")
        
        time.sleep(check_interval)
        elapsed = int(time.time() - start_time)
        print(f"\rWaiting for email... {elapsed}s/{timeout}s", end='', flush=True)
    
    print("\n")
    logger.warning("Timeout waiting for verification email")
    return None


def signup(driver, email, password, username=None, birth_date=None, email_provider=None, 
           proxy_data=None, fingerprint=None, use_enhanced_anti_bot=True):
    """
    Create a new TikTok account with anti-detection features.
    
    Args:
        driver: Selenium WebDriver instance
        email: Email address for the account
        password: Password for the account
        username: Optional username (will be generated if not provided)
        birth_date: Optional birth date dict with 'month', 'day', 'year' keys
        email_provider: Optional email provider instance for verification
        proxy_data: Optional proxy configuration
        fingerprint: Optional device fingerprint
        use_enhanced_anti_bot: Whether to use enhanced anti-bot measures
    
    Returns:
        dict: Account data if successful, None otherwise
    """
    bot = TikTokBot(driver)
    
    # Generate fingerprint if not provided
    if not fingerprint:
        fingerprint = generate_device_fingerprint()
    
    try:
        logger.info("Starting TikTok account signup process...")
        logger.info(f"Using fingerprint: platform={fingerprint['platform']}, screen={fingerprint['screen']}")
        
        # Apply fingerprint masking
        apply_fingerprint(driver, fingerprint)
        
        # Navigate to TikTok signup page with human-like behavior
        logger.info("Navigating to TikTok signup page...")
        driver.get("https://www.tiktok.com/signup")
        
        # Random wait to let page load naturally
        wait_random(3, 6)
        
        # Human-like scroll after page load
        if use_enhanced_anti_bot:
            human_like_scroll(driver, scrolls=1)
        
        # Check for blocks first
        if check_for_blocks(driver):
            logger.warning("TikTok is blocking requests. Try using a proxy or waiting.")
            return None
        
        # Check for CAPTCHA before anything else
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
        
        # Check if we need to accept cookies - with human-like click
        try:
            cookie_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept") or contains(text(), "Accept all")]'))
            )
            if use_enhanced_anti_bot:
                random_mouse_click(driver, cookie_btn)
            else:
                cookie_btn.click()
            logger.info("Accepted cookies")
            wait_random(1, 2)
        except:
            logger.info("No cookie popup found")
        
        # Check for CAPTCHA after cookie acceptance
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
        
        # Random mouse movement to appear more human
        if use_enhanced_anti_bot:
            random_jitter_mouse(driver)
            wait_random(0.5, 1.5)
        
        # Click on "Use phone or email" option - with human-like behavior
        try:
            phone_email_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Use phone or email") or contains(@data-e2e, "phone-email")]'))
            )
            if use_enhanced_anti_bot:
                random_mouse_click(driver, phone_email_btn)
            else:
                phone_email_btn.click()
            logger.info("Selected phone/email signup")
            wait_random(2, 4)
        except TimeoutException:
            # Try alternative selectors
            try:
                alt_btn = driver.find_element(By.XPATH, '//div[contains(@class, "channel-item") and contains(text(), "email")]')
                if use_enhanced_anti_bot:
                    random_mouse_click(driver, alt_btn)
                else:
                    alt_btn.click()
                logger.info("Selected email signup (alternative)")
                wait_random(2, 4)
            except:
                logger.error("Could not find email signup option")
                return None
        
        # Check for CAPTCHA after clicking signup option
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
        
        # Switch to email tab if needed
        try:
            email_tab_selectors = [
                (By.XPATH, '//div[contains(text(), "Email")]'),
                (By.XPATH, '//span[contains(text(), "Email")]'),
                (By.XPATH, '//div[@data-e2e="email-tab"]'),
                (By.CSS_SELECTOR, '[data-e2e="email-tab"]'),
                (By.XPATH, '//button[contains(@class, "email")]'),
            ]
            email_tab = bot.find_element_multiple_selectors(email_tab_selectors, timeout=3)
            if email_tab:
                if use_enhanced_anti_bot:
                    random_mouse_click(driver, email_tab)
                else:
                    email_tab.click()
                logger.info("Switched to email tab")
                wait_random(1, 2)
        except:
            logger.info("Email tab not needed or already selected")
        
        # Check for CAPTCHA after switching tabs
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
            # Add random mouse movement
            random_jitter_mouse(driver)

        # Fill in birth date if required
        if birth_date:
            try:
                # Try multiple selectors for month dropdown
                month_selectors = [
                    (By.CSS_SELECTOR, 'select[name="month"]'),
                    (By.XPATH, '//select[@name="month"]'),
                    (By.CSS_SELECTOR, '[data-e2e="month"] select'),
                    (By.XPATH, '//*[contains(@data-e2e, "month")]//select'),
                ]
                month_dropdown = bot.find_element_multiple_selectors(month_selectors, timeout=3)
                if month_dropdown:
                    month_dropdown.click()
                    time.sleep(0.3)
                    month_option = driver.find_element(By.XPATH, f'//option[@value="{birth_date["month"]}"]')
                    month_option.click()
                    time.sleep(0.3)

                # Day dropdown
                day_selectors = [
                    (By.CSS_SELECTOR, 'select[name="day"]'),
                    (By.XPATH, '//select[@name="day"]'),
                    (By.CSS_SELECTOR, '[data-e2e="day"] select'),
                    (By.XPATH, '//*[contains(@data-e2e, "day")]//select'),
                ]
                day_dropdown = bot.find_element_multiple_selectors(day_selectors, timeout=3)
                if day_dropdown:
                    day_dropdown.click()
                    time.sleep(0.3)
                    day_option = driver.find_element(By.XPATH, f'//option[@value="{birth_date["day"]}"]')
                    day_option.click()
                    time.sleep(0.3)

                # Year dropdown
                year_selectors = [
                    (By.CSS_SELECTOR, 'select[name="year"]'),
                    (By.XPATH, '//select[@name="year"]'),
                    (By.CSS_SELECTOR, '[data-e2e="year"] select'),
                    (By.XPATH, '//*[contains(@data-e2e, "year")]//select'),
                ]
                year_dropdown = bot.find_element_multiple_selectors(year_selectors, timeout=3)
                if year_dropdown:
                    year_dropdown.click()
                    time.sleep(0.3)
                    year_option = driver.find_element(By.XPATH, f'//option[@value="{birth_date["year"]}"]')
                    year_option.click()
                    time.sleep(0.3)

                logger.info("Entered birth date")

                # Click next/continue after birth date
                next_selectors = [
                    (By.XPATH, '//button[contains(text(), "Next")]'),
                    (By.XPATH, '//button[contains(text(), "Continue")]'),
                    (By.CSS_SELECTOR, 'button[type="submit"]'),
                    (By.XPATH, '//button[@type="submit"]'),
                ]
                next_btn = bot.find_element_multiple_selectors(next_selectors, timeout=3)
                if next_btn:
                    next_btn.click()
                    time.sleep(2)
            except Exception as e:
                logger.info(f"Birth date form not present or already passed: {e}")
                    
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
        
        # Check for CAPTCHA before entering email
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
            human_like_scroll(driver, scrolls=1)
        
        # Enter email - try multiple selectors for different TikTok page versions
        email_selectors = [
            (By.CSS_SELECTOR, 'input[type="email"]'),
            (By.XPATH, '//input[@type="email"]'),
            (By.CSS_SELECTOR, 'input[name="email"]'),
            (By.XPATH, '//input[@name="email"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="email"]'),
            (By.XPATH, '//input[contains(@placeholder, "email")]'),
            (By.CSS_SELECTOR, 'input[placeholder*="Email"]'),
            (By.XPATH, '//input[contains(@placeholder, "Email")]'),
            (By.XPATH, '//input[@type="text"]'),
            (By.XPATH, '//input[contains(@autocomplete, "email")]'),
        ]

        email_input = bot.find_element_multiple_selectors(email_selectors, timeout=10)
        if email_input:
            # Use human-like typing
            if use_enhanced_anti_bot:
                simulate_human_typing(email_input, email, fast=False)
            else:
                email_input.clear()
                for char in email:
                    email_input.send_keys(char)
                    time.sleep(random.uniform(0.02, 0.05))
            logger.info(f"Entered email: {email}")
        else:
            logger.error("Could not find email input field")
            # Try to find any input field
            try:
                all_inputs = driver.find_elements(By.TAG_NAME, 'input')
                logger.info(f"Found {len(all_inputs)} input fields on page")
                for i, inp in enumerate(all_inputs):
                    logger.info(f"  Input {i}: type={inp.get_attribute('type')}, name={inp.get_attribute('name')}, placeholder={inp.get_attribute('placeholder')}")
            except:
                pass
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
        
        wait_random(1, 3)
        
        # Check for CAPTCHA before entering password
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
        
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
            wait_random(2, 4)
        
        if password_input:
            # Use human-like typing for password
            if use_enhanced_anti_bot:
                simulate_human_typing(password_input, password, fast=True)
            else:
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
        
        wait_random(1, 2)
        
        # Check for CAPTCHA before entering username
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
        
        # Enter username - always generate if not provided
        if not username:
            # Generate a username if not provided
            import random
            adjectives = ['cool', 'awesome', 'happy', 'lucky', 'smart', 'brave', 'creative', 'wild', 'epic', 'fierce', 'swift']
            nouns = ['tiger', 'eagle', 'dolphin', 'wolf', 'bear', 'lion', 'fox', 'hawk', 'shark', 'panther', 'phoenix']
            username = f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(100, 9999)}"
            logger.info(f"Generated username: {username}")

        username_selectors = [
            (By.CSS_SELECTOR, 'input[name="username"]'),
            (By.XPATH, '//input[@name="username"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="username"]'),
            (By.XPATH, '//input[contains(@placeholder, "username")]'),
            (By.CSS_SELECTOR, 'input[placeholder*="Username"]'),
            (By.XPATH, '//input[contains(@placeholder, "Username")]'),
            (By.CSS_SELECTOR, 'input[placeholder*="@"]'),
            (By.XPATH, '//input[contains(@placeholder, "@")]'),
        ]

        username_input = bot.find_element_multiple_selectors(username_selectors, timeout=10)
        if username_input:
            # Use human-like typing for username
            if use_enhanced_anti_bot:
                simulate_human_typing(username_input, username, fast=False)
            else:
                username_input.clear()
                for char in username:
                    username_input.send_keys(char)
                    time.sleep(random.uniform(0.02, 0.05))
            logger.info(f"Entered username: {username}")
        else:
            logger.warning("Could not find username input field, may not be required yet")
        
        # Random delay before clicking signup
        if use_enhanced_anti_bot:
            wait_random(0.5, 1.5)
            random_jitter_mouse(driver)
        
        # Check for CAPTCHA before clicking signup
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
        
        # Click sign up button - with human-like click
        signup_selectors = [
            (By.XPATH, '//button[@type="submit"]'),
            (By.XPATH, '//button[contains(text(), "Sign up")]'),
            (By.XPATH, '//button[contains(text(), "Next")]'),
        ]
        
        # Click signup button with human-like behavior
        for selector in signup_selectors:
            try:
                signup_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(selector)
                )
                if use_enhanced_anti_bot:
                    random_mouse_click(driver, signup_btn)
                else:
                    signup_btn.click()
                logger.info("Clicked signup button")
                break
            except:
                continue
        
        wait_random(3, 6)
        
        # Check for CAPTCHA using enhanced detection
        if use_enhanced_anti_bot:
            check_and_solve_captcha(driver)
        
        # Also check for blocks
        if check_for_blocks(driver):
            logger.warning("TikTok is blocking after signup click. Try using a proxy.")
            return None
        
        # Random scroll to simulate human behavior
        if use_enhanced_anti_bot:
            human_like_scroll(driver, scrolls=1)
        
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
                        
                        # Use human-like typing for verification code
                        if use_enhanced_anti_bot:
                            simulate_human_typing(verification_code_input, code, fast=True)
                        else:
                            verification_code_input.clear()
                            for char in code:
                                verification_code_input.send_keys(char)
                                time.sleep(0.1)
                        
                        logger.info("Entered verification code")
                        wait_random(1, 2)
                    else:
                        print(f"\nEmail body: {body[:500]}")
                        code = input("Enter the verification code manually: ").strip()
                        if use_enhanced_anti_bot:
                            simulate_human_typing(verification_code_input, code, fast=True)
                        else:
                            verification_code_input.clear()
                            verification_code_input.send_keys(code)
                        time.sleep(2)
                else:
                    code = input("Enter the verification code manually: ").strip()
                    if use_enhanced_anti_bot:
                        simulate_human_typing(verification_code_input, code, fast=True)
                    else:
                        verification_code_input.clear()
                        verification_code_input.send_keys(code)
                    time.sleep(2)
            else:
                print("\n" + "="*60)
                print(f"Please check your email: {email}")
                print("Enter the verification code from TikTok's email.")
                print("="*60 + "\n")
                code = input("Enter the verification code: ").strip()
                if use_enhanced_anti_bot:
                    simulate_human_typing(verification_code_input, code, fast=True)
                else:
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
