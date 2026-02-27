"""
Configuration file for TikTok Automation Bot
"""
import os

# TikTok Credentials (set as environment variables or fill in directly)
TIKTOK_EMAIL = os.getenv("TIKTOK_EMAIL", "youremail@example.com")
TIKTOK_PASSWORD = os.getenv("TIKTOK_PASSWORD", "yourpassword")

# Cookie file path
COOKIE_FILE = "tiktok_cookies.txt"

# Bot Settings
HEADLESS = False  # Run in headless mode
BROWSER_MODE = "uc"  # Options: "uc" (undetected), "normal"
MAX_RETRIES = 3
WAIT_TIME = 10

# Comment Settings
COMMENTS = [
    "Great video! Engaging and informative.",
    "Amazing content! Well-presented and insightful.",
    "Fantastic job! Your creativity shines through.",
    "Impressive video! Captivating from start to finish.",
    "Wonderful production! Keep up the excellent work.",
    "Bravo! Your storytelling is truly compelling.",
    "Exceptional video! It's both entertaining and educational.",
    "Outstanding work! Your talent is evident in every frame.",
    "Well done! Your video is a delight to watch.",
    "Kudos on a superb video! Your efforts are commendable.",
]

# Default Actions
DEFAULT_COMMENT_USER = "taylor"
DEFAULT_COMMENT_COUNT = 3
DEFAULT_FOLLOW_USER = "amazon"

# Upload Settings
VIDEO_FILE_PATH = os.path.join(os.path.dirname(__file__), "my_video.mp4")
DEFAULT_VIDEO_CAPTION = "Check out this cool video! #tiktok #viral"

# Logging
LOG_FILE = "bot.log"
REPORT_FILE = "report.txt"

# TikTok URLs
TIKTOK_BASE_URL = "https://www.tiktok.com"
TIKTOK_LOGIN_URL = f"{TIKTOK_BASE_URL}/login/phone-or-email/email"
TIKTOK_UPLOAD_URL = f"{TIKTOK_BASE_URL}/creator-center/upload"

# Selectors (updated for current TikTok structure)
SELECTORS = {
    "login": {
        "email_input": '//input[@type="text"]',
        "password_input": '//input[@type="password"]',
        "submit_button": '//button[@type="submit"]',
    },
    "profile": {
        "user_post_item": '//div[@data-e2e="user-post-item"]',
        "video_card": '//div[contains(@class, "video-card")]',
        "follow_button": '//button[contains(@data-e2e, "follow")]',
    },
    "video": {
        "comment_input": '//div[@role="textbox"]',
        "comment_textarea": '//textarea[@placeholder="Add comment..."]',
        "send_button": '//button[@data-e2e="browse-send"]',
        "arrow_right": '//button[@data-e2e="arrow-right"]',
        "video_container": '//div[contains(@class, "video-feed")]',
    },
    "upload": {
        "file_input": 'input[type="file"]',
        "caption_input": '//div[@role="combobox"] or //div[contains(@class, "caption-input")]',
        "post_button": '//button[contains(text(), "Post") or contains(@class, "post-button")]',
    },
}
