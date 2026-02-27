# Email Generation Guide

Complete guide for email generation in TikTok Automation Bot.

## Overview

The bot supports multiple email generation strategies, including real temporary email services that can be scraped to get working email addresses for account creation.

## Email Strategies

### 1. Random Email Generation

**Strategy**: `random`

Generates random email addresses with various domains.

**Best For**: Testing purposes only - these emails won't actually work for account creation.

**How It Works**:
- Generates random usernames with numbers
- Uses configurable domains (Gmail, Yahoo, Outlook, etc.)
- Creates fake email addresses like `user123@gmail.com`

**Configuration**:
```python
EMAIL_GENERATION_STRATEGY = "random"
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com"]
```

**Limitations**:
- Emails are not real
- Cannot receive verification emails
- Only useful for testing bot functionality

### 2. Guerrilla Mail

**Strategy**: `guerrillamail`

Uses Guerrilla Mail API to generate real temporary email addresses.

**Best For**: Quick temporary email generation with working email addresses.

**How It Works**:
- Scrapes Guerrilla Mail API for new email
- Provides real working email address
- Can check inbox for verification emails
- Automatic email waiting functionality

**Configuration**:
```python
EMAIL_GENERATION_STRATEGY = "guerrillamail"
EMAIL_WAIT_TIMEOUT = 300  # 5 minutes
EMAIL_CHECK_INTERVAL = 5  # Check every 5 seconds
```

**Usage Example**:
```python
from email_generator import EmailGenerator

# Initialize
generator = EmailGenerator(strategy='guerrillamail')

# Generate email
email = generator.generate_email()
print(f"Generated email: {email}")

# Wait for verification email
message = generator.wait_for_email(email, timeout=300)
if message:
    print(f"Received email: {message['subject']}")
    print(f"Body: {message['body']}")
```

**Features**:
- ✅ Real working email addresses
- ✅ Inbox access
- ✅ Automatic email waiting
- ✅ Email verification code extraction
- ⚠️ Temporary (expires in 15-60 minutes)

### 3. 10 Minute Mail

**Strategy**: `10minutemail`

Uses 10minutemail.com service for temporary email addresses.

**Best For**: Short-lived temporary email needs.

**How It Works**:
- Scrapes 10minutemail.com for new email
- Provides real working email address
- Can check inbox for messages
- Email valid for 10 minutes

**Configuration**:
```python
EMAIL_GENERATION_STRATEGY = "10minutemail"
EMAIL_WAIT_TIMEOUT = 600  # 10 minutes (max)
```

**Features**:
- ✅ Real working email addresses
- ✅ 10-minute validity period
- ✅ Inbox access
- ⚠️ Web scraping (may be slower)
- ⚠️ Anti-bot protections may block requests

### 4. Temp Mail

**Strategy**: `tempmail`

Uses temp-mail.org service for temporary email addresses.

**Best For**: Multiple temporary email addresses quickly.

**How It Works**:
- Uses temp-mail.org API
- Generates random usernames with temp mail domains
- Provides real working email addresses
- API-based (faster than scraping)

**Configuration**:
```python
EMAIL_GENERATION_STRATEGY = "tempmail"
EMAIL_WAIT_TIMEOUT = 300
```

**Supported Domains**:
- temp-mail.org
- 1secmail.com
- 1secmail.net
- 1secmail.com

**Features**:
- ✅ Real working email addresses
- ✅ API-based (fast and reliable)
- ✅ Multiple domain options
- ✅ Inbox access
- ✅ Email waiting functionality

### 5. Custom Email List

**Strategy**: `custom`

Uses your own list of pre-existing email addresses.

**Best For**: Using verified email accounts or bulk email creation.

**How It Works**:
- Reads email addresses from a text file
- Uses emails one by one
- Tracks which emails have been used
- Can reset tracking to reuse emails

**Configuration**:
```python
EMAIL_GENERATION_STRATEGY = "custom"
CUSTOM_EMAILS_FILE = "emails.txt"
```

**Email File Format** (`emails.txt`):
```
# Lines starting with # are comments
email1@gmail.com
email2@yahoo.com
email3@outlook.com
another.email@domain.com
```

**Usage Example**:
```python
from email_generator import CustomEmailList

# Initialize
email_list = CustomEmailList("emails.txt")

# Get unused email
email = email_list.get_email()
print(f"Using email: {email}")

# Mark as used when done
email_list.mark_used(email)

# Reset tracking (to reuse emails)
email_list.reset_usage()
```

**Features**:
- ✅ Use your own verified emails
- ✅ Track usage
- ✅ No dependency on external services
- ✅ Can reuse emails
- ⚠️ Requires manual email list management

## Comparison of Strategies

| Strategy | Real Email | Inbox Access | Waiting | Best For | Notes |
|-----------|-------------|---------------|----------|-----------|---------|
| Random | ❌ | ❌ | ❌ | Testing | Won't work for real accounts |
| Guerrilla Mail | ✅ | ✅ | ✅ | Quick temp accounts | 15-60 min expiry |
| 10 Minute Mail | ✅ | ✅ | ✅ | Short-term needs | 10 min expiry, scraping |
| Temp Mail | ✅ | ✅ | ✅ | Fast temp accounts | API-based, fast |
| Custom List | ✅ | ❌ | ❌ | Verified accounts | Manual management |

## Usage Examples

### Basic Email Generation

```python
from email_generator import EmailGenerator

# Initialize with strategy
generator = EmailGenerator(strategy='guerrillamail')

# Generate email
email = generator.generate_email()
print(f"Email: {email}")
```

### Waiting for Verification Email

```python
# Generate email
generator = EmailGenerator(strategy='guerrillamail')
email = generator.generate_email()

# Use email for registration (e.g., with TikTok)
# ... registration code ...

# Wait for verification email
message = generator.wait_for_email(email, timeout=300)

if message:
    print(f"From: {message['from']}")
    print(f"Subject: {message['subject']}")
    print(f"Body: {message['body']}")
    
    # Extract verification code
    import re
    code_match = re.search(r'\d{6}', message['body'])
    if code_match:
        code = code_match.group(0)
        print(f"Verification code: {code}")
else:
    print("Timeout waiting for verification email")
```

### Checking Inbox

```python
# Generate email
generator = EmailGenerator(strategy='tempmail')
email = generator.generate_email()

# Later, check inbox
messages = generator.get_inbox(email)

for msg in messages:
    print(f"ID: {msg['id']}")
    print(f"From: {msg['from']}")
    print(f"Subject: {msg['subject']}")
    print(f"Timestamp: {msg['timestamp']}")
    print(f"Body: {msg['body'][:100]}...")
    print("-" * 40)
```

### Bulk Email Generation

```python
# Generate multiple emails
generator = EmailGenerator(strategy='tempmail')
emails = generator.bulk_generate(count=10)

for i, email in enumerate(emails, 1):
    print(f"{i}. {email}")
```

### Account Creation with Email Verification

```python
from email_generator import EmailGenerator
from seleniumbase import Driver

# Initialize
generator = EmailGenerator(strategy='guerrillamail')
driver = Driver(uc=True)

# Generate email
email = generator.generate_email()
password = "SecurePass123!"

# Navigate to TikTok signup
driver.get("https://www.tiktok.com/signup")

# Fill in registration form
# ... use Selenium to fill form with email and password ...

# Submit registration
# ... click submit button ...

# Wait for verification email
message = generator.wait_for_email(email, timeout=300)

if message:
    # Extract verification code from email
    import re
    code = re.search(r'(\d{6})', message['body'])
    
    if code:
        verification_code = code.group(0)
        print(f"Verification code: {verification_code}")
        
        # Enter code on TikTok
        # ... use Selenium to enter code ...

driver.quit()
```

## Configuration Options

### Global Settings (config.py)

```python
# Email Generation Settings
EMAIL_GENERATION_STRATEGY = "guerrillamail"  # Strategy to use
CUSTOM_EMAILS_FILE = "emails.txt"  # For custom strategy
EMAIL_DOMAINS = ["gmail.com", "yahoo.com"]  # For random strategy

# Email Service Settings
EMAIL_WAIT_TIMEOUT = 300  # Max wait time (seconds)
EMAIL_CHECK_INTERVAL = 5  # Inbox check interval (seconds)
```

### Proxy Settings

Some email services may block requests from certain IPs. Use proxies if needed:

```python
# Use proxies for email generation requests
import requests

session = requests.Session()
session.proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}
```

## Troubleshooting

### Issue: Failed to generate email

**Guerrilla Mail**:
- Check internet connection
- Verify API is accessible: https://api.guerrillamail.com/ajax.php
- Try different strategy (tempmail, 10minutemail)

**10 Minute Mail**:
- May be blocked by anti-bot protections
- Try using proxies
- Try Guerrilla Mail or Temp Mail instead

**Temp Mail**:
- Check API availability: https://web1.temp-mail.org/api/v1
- Verify domains are accessible

### Issue: Not receiving verification emails

**Solutions**:
1. Increase timeout:
   ```python
   message = generator.wait_for_email(email, timeout=600)  # 10 minutes
   ```

2. Check spam folder (manual check)

3. Verify email address is correct

4. Try different email service:
   ```python
   generator = EmailGenerator(strategy='guerrillamail')  # Try this
   # or
   generator = EmailGenerator(strategy='tempmail')
   ```

### Issue: Email expired

**Guerrilla Mail**: Emails expire in 15-60 minutes
**10 Minute Mail**: Emails expire in 10 minutes
**Temp Mail**: Varies by domain

**Solution**: Complete verification quickly after receiving email

### Issue: Too many requests

Email services may rate limit requests.

**Solutions**:
1. Add delays between email generations
2. Use proxies
3. Rotate between different email services
4. Use custom email list

## Best Practices

### 1. Choose the Right Strategy

- **Testing**: Use `random` for quick tests
- **Quick temp accounts**: Use `guerrillamail` or `tempmail`
- **10-minute needs**: Use `10minutemail`
- **Verified accounts**: Use `custom` with your own emails

### 2. Handle Timeouts

Always set reasonable timeouts:
```python
# TikTok emails usually arrive within 1-5 minutes
message = generator.wait_for_email(email, timeout=300)
```

### 3. Extract Verification Codes

Most verification codes are 6-digit numbers:
```python
import re

code_match = re.search(r'(\d{6})', message['body'])
if code_match:
    code = code_match.group(0)
```

### 4. Error Handling

Always handle email generation failures:
```python
try:
    email = generator.generate_email()
    if not email:
        raise Exception("Failed to generate email")
    
    # Use email for registration...
    
except Exception as e:
    print(f"Error: {e}")
    # Try different strategy or retry
```

### 5. Log Everything

Track email generation and verification:
```python
import logging

logger = logging.getLogger(__name__)

email = generator.generate_email()
logger.info(f"Generated email: {email}")

message = generator.wait_for_email(email)
if message:
    logger.info(f"Received verification email from {message['from']}")
else:
    logger.warning(f"Timeout waiting for email: {email}")
```

## API Reference

### EmailGenerator

```python
class EmailGenerator:
    def __init__(self, strategy: str, **kwargs)
    def generate_email(self) -> str
    def get_inbox(self, email: str) -> List[dict]
    def wait_for_email(self, email: str, timeout: int = 300) -> Optional[Dict]
    def bulk_generate(self, count: int) -> List[str]
```

### EmailProvider (Base Class)

```python
class EmailProvider:
    def generate_email(self) -> str
    def get_inbox(self, email: str) -> List[dict]
    def wait_for_email(self, email: str, timeout: int = 300) -> Optional[Dict]
```

## Dependencies

Required packages:
- `requests` - For HTTP requests to email services
- `beautifulsoup4` - For scraping email pages
- `lxml` - HTML parser for BeautifulSoup

Install:
```bash
pip install requests beautifulsoup4 lxml
```

## Security Notes

### 1. Don't Store Passwords with Emails

Generated emails are temporary. Don't associate them with sensitive accounts.

### 2. Use Unique Emails

Generate a new email for each account. Don't reuse.

### 3. Monitor Usage

Some email services have usage limits. Monitor your usage.

### 4. Respect Terms of Service

Email services may have usage terms. Read and comply.

## Legal Disclaimer

Using temporary email services for account creation may violate the terms of service of:
- The email service provider
- The platform where you're creating accounts (TikTok)

Use this feature responsibly and at your own risk. The developers are not responsible for any consequences.

## Support

For issues or questions:
- Check `bot.log` for detailed error messages
- Review [MULTI_ACCOUNT_GUIDE.md](MULTI_ACCOUNT_GUIDE.md)
- Contact: [mysteredev](https://t.me/mysteredev) on Telegram

## Changelog

### v2.1.1 - Email Generation Update

**Added**:
- Real temporary email service integrations
- Guerrilla Mail provider
- 10 Minute Mail provider
- Temp Mail provider (API-based)
- Email waiting functionality
- Inbox access for verification emails
- BeautifulSoup for web scraping
- Email verification code extraction

**Improved**:
- Better error handling
- Timeout configuration
- Multiple email strategies
- Web scraping with proper headers

**Fixed**:
- Random email generation (now marked as testing only)
- Email service integration issues
