# Usage Examples

This document provides detailed examples of how to use the TikTok Automation Bot.

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Running the Bot](#running-the-bot)
3. [Customizing Comments](#customizing-comments)
4. [Single Task Execution](#single-task-execution)
5. [Error Handling](#error-handling)
6. [Advanced Usage](#advanced-usage)

## Basic Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Credentials

Edit `config.py`:

```python
TIKTOK_EMAIL = "your.email@example.com"
TIKTOK_PASSWORD = "yourpassword"
```

Or use environment variables:

```bash
export TIKTOK_EMAIL="your.email@example.com"
export TIKTOK_PASSWORD="yourpassword"
```

### Step 3: Prepare for Video Upload (Optional)

If you plan to upload videos, place your video file as `my_video.mp4` in the project root, or update the path in `config.py`:

```python
VIDEO_FILE_PATH = "/path/to/your/video.mp4"
```

## Running the Bot

### Default Automated Mode

Run all default tasks:

```bash
python main.py
```

This will:
1. Login to TikTok
2. Post 3 comments on @taylor's videos
3. Follow @amazon
4. Upload a video (if file exists)

### Interactive Mode

Choose tasks interactively:

```bash
python main.py --interactive
```

Example session:

```
Available tasks:
1. Comment on user videos
2. Follow a user
3. Upload a video
4. Run all default tasks
5. Exit

Select a task (1-5): 1
Enter username to comment on: someuser
Enter number of comments: 5

Posted 5/5 comments
```

## Customizing Comments

### Edit in config.py

```python
COMMENTS = [
    "Love this content! 🔥",
    "This is amazing! Keep it up!",
    "Great job on this video!",
    "Absolutely fantastic! 👏",
    "Can't wait for the next one!",
    "This deserves more views!",
    "Quality content right here!",
    "Subscribed and liked! ❤️",
]
```

### Use Different Comments for Different Users

Create a custom script:

```python
from seleniumbase import Driver
from social_media import tiktok

driver = Driver(uc=True)
driver.maximize_window()

# Login
cookies = tiktok.load_cookies('tiktok_cookies.txt')
tiktok.login(driver, "email@example.com", "password", cookies)

# Custom comments for specific user
tech_comments = [
    "Great tech tutorial!",
    "Very informative coding content!",
    "Love the explanation!",
    "Helpful as always!",
]

tiktok.comment_user_video(driver, "techchannel", tech_comments, 5)
```

## Single Task Execution

### Only Comment

```python
from seleniumbase import Driver
from social_media import tiktok

driver = Driver(uc=True)
driver.maximize_window()

# Login
tiktok.login(driver, "email@example.com", "password", None)

# Comment only
comments = ["Great video!", "Amazing content!"]
tiktok.comment_user_video(driver, "username", comments, 2)
```

### Only Follow

```python
from seleniumbase import Driver
from social_media import tiktok

driver = Driver(uc=True)
driver.maximize_window()

# Login
tiktok.login(driver, "email@example.com", "password", None)

# Follow only
tiktok.follow(driver, "username")
```

### Only Upload

```python
from seleniumbase import Driver
from social_media import tiktok

driver = Driver(uc=True)
driver.maximize_window()

# Login
tiktok.login(driver, "email@example.com", "password", None)

# Upload only
tiktok.upload(driver, "my_video.mp4", "Check out my new video! #viral")
```

## Error Handling

### Using Try-Except

```python
from seleniumbase import Driver
from social_media import tiktok
import time

driver = Driver(uc=True)
driver.maximize_window()

try:
    # Login
    login_success = tiktok.login(driver, "email", "password", None)
    
    if login_success:
        # Comment
        result = tiktok.comment_user_video(driver, "user", ["Nice!"], 1)
        print(f"Comments posted: {result}")
    else:
        print("Login failed")
        
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    driver.quit()
```

### Retry Logic

```python
from seleniumbase import Driver
from social_media import tiktok
import time

def retry_follow(driver, username, max_retries=3):
    for attempt in range(max_retries):
        try:
            success = tiktok.follow(driver, username)
            if success:
                return True
            print(f"Attempt {attempt + 1} failed, retrying...")
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
    return False

driver = Driver(uc=True)
tiktok.login(driver, "email", "password", None)
retry_follow(driver, "username")
driver.quit()
```

## Advanced Usage

### Batch Follow Multiple Users

```python
from seleniumbase import Driver
from social_media import tiktok
import time

users_to_follow = ["user1", "user2", "user3", "user4", "user5"]

driver = Driver(uc=True)
driver.maximize_window()

# Login
tiktok.login(driver, "email", "password", None)

# Follow each user
for i, user in enumerate(users_to_follow):
    print(f"Following {user} ({i+1}/{len(users_to_follow)})")
    tiktok.follow(driver, user)
    
    # Random delay between follows
    time.sleep(time.uniform(3, 7))

driver.quit()
```

### Custom Comment Schedule

```python
from seleniumbase import Driver
from social_media import tiktok
import time

driver = Driver(uc=True)
driver.maximize_window()

# Login
tiktok.login(driver, "email", "password", None)

# Comment on multiple users
users_and_comments = [
    ("user1", ["Great!", "Amazing!"], 2),
    ("user2", ["Love it!", "Awesome!"], 2),
    ("user3", ["Fantastic!", "Bravo!"], 2),
]

for user, comments, count in users_and_comments:
    print(f"Commenting on {user}")
    tiktok.comment_user_video(driver, user, comments, count)
    time.sleep(10)  # Delay between users

driver.quit()
```

### Upload Multiple Videos

```python
from seleniumbase import Driver
from social_media import tiktok
import os
import glob

driver = Driver(uc=True)
driver.maximize_window()

# Login
tiktok.login(driver, "email", "password", None)

# Get all video files
video_files = glob.glob("videos/*.mp4")

for video_path in video_files:
    filename = os.path.basename(video_path)
    caption = f"Check out {filename}! #video #share"
    
    print(f"Uploading {filename}")
    tiktok.upload(driver, video_path, caption)
    
    # Wait between uploads
    time.sleep(30)

driver.quit()
```

### Headless Mode for Production

```python
# Set in config.py:
HEADLESS = True

# Or programmatically:
from seleniumbase import Driver
from social_media import tiktok

driver = Driver(headless=True, uc=True)
# ... rest of your code
```

### Using Different Browsers

```python
# Chrome (default)
driver = Driver(uc=True)

# Firefox
driver = Driver(browser="firefox", uc=True)

# Edge
driver = Driver(browser="edge", uc=True)
```

## Tips and Best Practices

1. **Start Small**: Test with 1-2 comments first
2. **Add Delays**: Always add delays between actions
3. **Monitor Logs**: Check `bot.log` for issues
4. **Use Cookies**: After first manual login, cookies are saved automatically
5. **Be Respectful**: Don't spam or over-automate
6. **Stay Updated**: TikTok changes frequently, keep the bot updated

## Common Issues and Solutions

### Issue: "Could not find element"

**Solution**: TikTok may have updated their DOM. Check the logs and consider updating selectors in `config.py`.

### Issue: "Login failed"

**Solution**: Complete the login manually when prompted. Cookies will be saved for future use.

### Issue: "Captcha required"

**Solution**: The bot will pause. Complete the CAPTCHA manually in the browser.

### Issue: "Video upload failed"

**Solution**: Ensure video file exists and meets TikTok's requirements. Check logs for specific errors.

## Need More Help?

For custom automation projects or questions, contact: **[mysteredev](https://t.me/mysteredev)**
