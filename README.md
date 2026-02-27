# TikTok Automation Bot

A powerful **TikTok Automation Bot** that automates various tasks such as logging in, posting comments, following users, and uploading videos. It's designed to help streamline interaction with TikTok using Python and Selenium.

> **📚 Documentation**: 
> - [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
> - [Usage Examples](USAGE_EXAMPLES.md) - Detailed code examples
> - [Upgrade Notes](UPGRADE_NOTES.md) - Migrating from v1.0.0

> **⚠️ Important Notice:** TikTok frequently updates their website structure, which may break automation scripts. This project uses multiple selector strategies and error handling to improve reliability, but some features may require adjustments over time.

## Features

- **Automatic Login**: Uses cookies for faster login or manual login if cookies are unavailable
- **Commenting**: Automatically posts comments on user's TikTok videos with human-like delays
- **Following Users**: Follows specified TikTok users automatically
- **Video Uploading**: Automates the upload of videos from local storage to TikTok
- **Interactive Mode**: Choose which tasks to run interactively
- **Logging**: Comprehensive logging to track bot activities and debug issues
- **Error Handling**: Robust error handling with multiple selector strategies
- **Configuration**: Centralized configuration file for easy customization

**📝 For recent changes and version history, see [CHANGELOG.md](CHANGELOG.md)**

## Technologies Used

- **Python 3.7+**: For the main logic and automation scripts
- **Selenium 4.15+**: For web automation
- **SeleniumBase 4.0+**: For enhanced Selenium capabilities with undetected-chromedriver

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mysterecode/tiktok-automation-bot.git
   cd tiktok-automation-bot
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot:**
   Edit `config.py` to set your preferences:
   - Add your TikTok email and password (or set as environment variables)
   - Customize comments list
   - Configure bot settings (headless mode, wait times, etc.)

## Usage

### Automated Mode (Default)

Run the bot with default tasks configured in `config.py`:

```bash
python main.py
```

The bot will:
1. Login to TikTok (using cookies or credentials)
2. Post comments on a user's videos
3. Follow a specified user
4. Upload a video (if file exists)

### Interactive Mode

Run the bot in interactive mode to choose tasks:

```bash
python main.py --interactive
```

You'll be prompted to select tasks:
1. Comment on user videos
2. Follow a user
3. Upload a video
4. Run all default tasks
5. Exit

### Using as a Module

You can also use the bot functions in your own scripts:

```python
from seleniumbase import Driver
from social_media import tiktok
import config

# Initialize driver
driver = Driver(uc=True)
driver.maximize_window()

# Login
cookies = tiktok.load_cookies(config.COOKIE_FILE)
tiktok.login(driver, "your@email.com", "yourpassword", cookies)

# Comment on videos
tiktok.comment_user_video(driver, "username", config.COMMENTS, 3)

# Follow a user
tiktok.follow(driver, "username")

# Upload a video
tiktok.upload(driver, "path/to/video.mp4", "Your caption here")
```

## Configuration

Edit `config.py` to customize the bot:

```python
# Credentials
TIKTOK_EMAIL = "your@email.com"
TIKTOK_PASSWORD = "yourpassword"

# Bot Settings
HEADLESS = False  # Run browser in headless mode
BROWSER_MODE = "uc"  # "uc" for undetected mode, "normal" for standard

# Comments to post
COMMENTS = [
    "Great video!",
    "Amazing content!",
    # Add more comments...
]

# Default Actions
DEFAULT_COMMENT_USER = "taylor"
DEFAULT_COMMENT_COUNT = 3
DEFAULT_FOLLOW_USER = "amazon"

# Upload Settings
VIDEO_FILE_PATH = "my_video.mp4"
DEFAULT_VIDEO_CAPTION = "Check out this cool video! #tiktok #viral"
```

### Environment Variables

For better security, use environment variables instead of hardcoding credentials:

```bash
# On Mac/Linux
export TIKTOK_EMAIL="your@email.com"
export TIKTOK_PASSWORD="yourpassword"

# On Windows (PowerShell)
$env:TIKTOK_EMAIL="your@email.com"
$env:TIKTOK_PASSWORD="yourpassword"

# On Windows (CMD)
set TIKTOK_EMAIL=your@email.com
set TIKTOK_PASSWORD=yourpassword
```

## Project Structure

```
tiktok-automation-bot/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── social_media/
│   └── tiktok.py       # Core TikTok automation functions
├── bot.log             # Bot activity logs (generated)
└── report.txt          # Task reports (generated)
```

## Logging

The bot creates two log files:

- **bot.log**: Detailed logs of all bot activities and errors
- **report.txt**: Summary of completed tasks

## Troubleshooting

### Login Issues

If automatic login fails:
1. The bot will prompt you to login manually
2. Complete any CAPTCHA or 2FA challenges
3. Type 'ok' to continue
4. Cookies will be saved for future use

### Selector Issues

TikTok frequently updates their website structure. If you encounter issues:

1. Check `bot.log` for specific errors
2. The bot uses multiple selector strategies for better reliability
3. Some features may require updating selectors in `config.py`

### Video Upload Issues

Video upload is complex and may fail if:
1. The video file doesn't exist at the specified path
2. TikTok has changed the upload flow
3. Additional verification is required

Check the logs for specific error messages.

### Captcha and 2FA

TikTok may present:
- CAPTCHAs during login
- 2FA verification via SMS/email
- Security challenges

The bot will pause and prompt you to complete these steps manually.

## Best Practices

1. **Use Cookie-Based Login**: Once logged in manually, cookies are saved for faster future logins
2. **Add Random Delays**: The bot includes human-like typing delays and random wait times
3. **Don't Overdo It**: Excessive automation may trigger TikTok's anti-bot measures
4. **Monitor Logs**: Regularly check `bot.log` for errors and issues
5. **Keep Updated**: TikTok changes frequently; update the bot when features break
6. **Use Interactive Mode**: For testing new features, use interactive mode first

## Limitations

- **TikTok Updates**: Website structure changes may break functionality
- **Anti-Bot Measures**: TikTok has sophisticated bot detection
- **Captcha/2FA**: Manual intervention may be required
- **Rate Limits**: Excessive actions may be flagged
- **Video Upload**: Complex process with multiple verification steps

## Security Notes

⚠️ **Important Security Practices:**

1. Never commit `tiktok_cookies.txt` or `bot.log` to version control
2. Use environment variables for credentials instead of hardcoding
3. Don't share your credentials or cookie files
4. The `.gitignore` file is configured to exclude sensitive files

## Future Enhancements

- Add support for more social media platforms (Instagram, YouTube)
- Multi-account support
- Scheduling features for timed automation
- Sentiment analysis of comments
- Advanced error recovery
- GUI interface for easier use
- Docker containerization

## Contributing

Contributions are welcome! If you find issues or have improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Disclaimer

This project is for educational purposes only. Using automation tools on social media platforms may violate their Terms of Service. Use responsibly and at your own risk. The developers are not responsible for any consequences of using this bot.

## License

This project is open source and available for educational purposes.

## Contact

For custom automation or scraping projects, reach out via Telegram: **[mysteredev](https://t.me/mysteredev)**

---

**Note**: This bot is continuously improved to adapt to TikTok's changes. If you encounter issues, please check the logs and consider contributing fixes.
