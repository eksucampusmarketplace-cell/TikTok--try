# Quick Start Guide

Get the TikTok Automation Bot running in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- TikTok account

## Installation

```bash
# 1. Navigate to project directory
cd tiktok-automation-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
python test_setup.py
```

## Setup

### Option 1: Edit config.py (Quick)

1. Open `config.py`
2. Replace email and password:
   ```python
   TIKTOK_EMAIL = "your.email@example.com"
   TIKTOK_PASSWORD = "yourpassword"
   ```

### Option 2: Use Environment Variables (Secure)

```bash
# On Mac/Linux
export TIKTOK_EMAIL="your.email@example.com"
export TIKTOK_PASSWORD="yourpassword"

# On Windows PowerShell
$env:TIKTOK_EMAIL="your.email@example.com"
$env:TIKTOK_PASSWORD="yourpassword"
```

## Usage

### Automated Mode

Run all default tasks:
```bash
python main.py
```

The bot will:
1. Login to TikTok
2. Comment on 3 videos
3. Follow a user
4. Upload a video (if file exists)

### Interactive Mode

Choose tasks manually:
```bash
python main.py --interactive
```

You'll see:
```
Available tasks:
1. Comment on user videos
2. Follow a user
3. Upload a video
4. Run all default tasks
5. Exit

Select a task (1-5): 
```

## Common Tasks

### Only Comment

```python
from seleniumbase import Driver
from social_media import tiktok

driver = Driver(uc=True)
tiktok.login(driver, "email@example.com", "password", None)
tiktok.comment_user_video(driver, "username", ["Great video!"], 1)
```

### Only Follow

```python
from seleniumbase import Driver
from social_media import tiktok

driver = Driver(uc=True)
tiktok.login(driver, "email@example.com", "password", None)
tiktok.follow(driver, "username")
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Login fails
- The bot will prompt for manual login
- Complete any CAPTCHA
- Type 'ok' to continue
- Cookies will be saved for next time

### "Could not find element"
- TikTok may have updated their website
- Check `bot.log` for details
- The bot tries multiple selectors automatically

## Files Created During Runtime

- `tiktok_cookies.txt` - Saved login cookies
- `bot.log` - Activity log
- `report.txt` - Task completion report

These files are in `.gitignore` and won't be committed.

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for advanced examples
- Customize comments in `config.py`

## Need Help?

- Check `bot.log` for errors
- Review [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
- Contact: [mysteredev](https://t.me/mysteredev) on Telegram
