# Changelog

All notable changes to the TikTok Automation Bot project will be documented in this file.

## [2.1.1] - 2024-02-27

### Fixed - Email Generation 🎉

**Problem**: Previous email generation only created fake email addresses that couldn't receive verification emails, making real account creation impossible.

**Solution**: Integrated with real temporary email services that provide working email addresses and inbox access.

### New Email Providers

- **Guerrilla Mail** (`guerrillamail`)
  - Real working temporary email addresses
  - API-based email generation
  - Inbox access for verification emails
  - Automatic email waiting functionality
  - 15-60 minute email expiry

- **10 Minute Mail** (`10minutemail`)
  - Temporary emails valid for 10 minutes
  - Web scraping integration
  - Inbox access and message parsing
  - Ideal for short-term email needs

- **Temp Mail** (`tempmail`)
  - Uses temp-mail.org API
  - API-based (fast and reliable)
  - Multiple domain options
  - Real working email addresses
  - Automatic inbox checking

### Email Generation Features

- **Automatic Email Waiting**: Wait for verification emails with configurable timeout
- **Inbox Access**: Check inbox for messages
- **Verification Code Extraction**: Extract codes from email bodies
- **Multiple Strategies**: Choose between random, temp services, or custom lists
- **Error Handling**: Comprehensive error handling for email service failures
- **Web Scraping**: BeautifulSoup integration for scraping email pages
- **Rate Limiting**: Configurable check intervals to avoid blocking

### Updated Configuration

```python
# Email Generation Settings
EMAIL_GENERATION_STRATEGY = "guerrillamail"  # Now supports real services
CUSTOM_EMAILS_FILE = "emails.txt"
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com"]

# Email Service Settings (NEW)
EMAIL_WAIT_TIMEOUT = 300  # Seconds to wait for verification email
EMAIL_CHECK_INTERVAL = 5  # Seconds between inbox checks
```

### Updated Dependencies

- Added `beautifulsoup4>=4.12.0` for web scraping
- Added `lxml>=4.9.0` as HTML parser

### Documentation

- **EMAIL_GENERATION_GUIDE.md** (13,249 bytes) - Complete guide for email generation
  - All email strategies explained
  - Usage examples
  - Verification code extraction
  - Troubleshooting guide
  - Best practices

### Modified Files

- `email_generator.py` - Complete rewrite with real email service integrations
  - Added GuerrillaMailProvider class
  - Added TenMinuteMailProvider class
  - Added TempMailProvider class
  - Added wait_for_email() method to all providers
  - Improved error handling

- `config.py` - Added email service settings
- `requirements.txt` - Added beautifulsoup4 and lxml
- `main.py` - Updated account creation wizard with strategy selection
- `README.md` - Updated features and documentation links

### Breaking Changes

None - all changes are backward compatible.

### Notes

- **Guerrilla Mail** is recommended for most use cases (API-based, reliable)
- **Temp Mail** is fastest but has shorter expiry
- **10 Minute Mail** may be blocked by anti-bot protections
- **Random** strategy is now clearly marked as testing-only
- Email services may rate limit requests - use appropriate delays

## [2.1.0] - 2024-02-27

### Added - Multi-Account Support 🎉

- **Account Management System** (`account_manager.py`)
  - Create, read, update, delete accounts
  - Import/export accounts from JSON or CSV
  - Account status management (active/disabled)
  - Cookie storage per account
  - Account metadata (created_at, last_used)

- **Proxy Manager** (`proxy_manager.py`)
  - Add proxies manually or from file
  - Multiple proxy rotation strategies (round_robin, random, least_used)
  - Proxy validation/testing
  - Support for authenticated proxies
  - Proxy usage tracking (success/failure counts)
  - Import/export proxies from JSON or TXT

- **Email Generator** (`email_generator.py`)
  - Random email generation with multiple domains
  - Custom email list support
  - Temporary email service integration (framework)
  - Email validation utilities

- **Multi-Account Bot Manager** (`multi_account_bot.py`)
  - Execute tasks across multiple accounts simultaneously
  - Thread pool for parallel execution
  - Account-specific bot instances
  - Batch comment with multiple accounts
  - Batch follow with multiple accounts
  - Account rotation for repeated tasks
  - Configurable concurrent bot limit

- **Account Creation Wizard**
  - Automated account data structure creation
  - Email and password generation
  - Proxy assignment
  - Interactive wizard in menu
  - Bulk account creation support

- **Interactive Multi-Account Menu**
  - View all accounts with status
  - Add/delete/import accounts
  - Enable/disable accounts
  - Execute tasks on all accounts
  - Batch comment operations
  - Batch follow operations
  - Account creation wizard
  - Proxy management sub-menu

- **Enhanced Configuration** (`config.py`)
  - Multi-account settings
  - Account creation settings
  - Proxy settings with rotation strategies
  - Email generation configuration
  - Concurrent bot limits

### New Files

- `account_manager.py` - Account management system (12,400 bytes)
- `proxy_manager.py` - Proxy management system (12,274 bytes)
- `email_generator.py` - Email generation utilities (8,822 bytes)
- `multi_account_bot.py` - Multi-account execution engine (15,952 bytes)
- `MULTI_ACCOUNT_GUIDE.md` - Comprehensive multi-account documentation (14,980 bytes)
- `accounts.example.json` - Example accounts file (724 bytes)
- `proxies.example.json` - Example proxies file (817 bytes)
- `emails.example.txt` - Example email list (322 bytes)

### Modified Files

- `main.py` - Added multi-account menu, imports, and functionality
- `config.py` - Added multi-account, proxy, and email settings
- `requirements.txt` - Added requests>=2.31.0
- `.gitignore` - Added accounts.json, proxies.json, emails.txt
- `README.md` - Updated features and documentation links

### Documentation

- **MULTI_ACCOUNT_GUIDE.md** - Complete guide for multi-account features
  - Account management
  - Proxy management
  - Email generation
  - Account creation
  - Multi-account operations
  - Configuration
  - Best practices
  - Troubleshooting
  - API reference

### Breaking Changes

None - all changes are additions and backward compatible.

### Notes

- Account creation generates data structures but requires manual verification (email/phone, captcha)
- Proxy support requires quality proxies for best results
- Start with small numbers of accounts and increase gradually
- Monitor account health and disable flagged accounts

## [2.0.0] - 2024-02-27

### Added

- **Configuration Management**: New `config.py` file for centralized settings
- **Environment Variables Support**: Can now set credentials via environment variables
- **Interactive Mode**: New `--interactive` flag for choosing tasks manually
- **Comprehensive Logging**: Added logging to both file (`bot.log`) and console
- **Setup Validation**: `test_setup.py` script to verify installation
- **Multiple Selector Strategies**: Each function now tries multiple DOM selectors for better reliability
- **Human-like Typing**: Added randomized typing delays to appear more natural
- **Error Handling**: Improved error handling with detailed logging
- **Report File**: `report.txt` now records all completed tasks with timestamps
- **Documentation**:
  - Updated README with comprehensive documentation
  - New USAGE_EXAMPLES.md with detailed examples
  - New .env.example for environment variable setup
  - New CHANGELOG.md to track changes

### Changed

- **Refactored Code**: Completely rewrote `social_media/tiktok.py` with better structure
- **Class Renaming**: Main class is now `TikTokBot` (with `tiktok_bot` alias for backward compatibility)
- **Updated Dependencies**: Added version pinning in requirements.txt
- **Improved Selectors**: All selectors now have fallback strategies for TikTok DOM changes
- **Better Main Script**: `main.py` now supports both automated and interactive modes

### Fixed

- **Cookie Handling**: Improved cookie loading/saving with better error handling
- **Login Flow**: Enhanced login process with multiple strategies
- **Comment Posting**: Better comment submission with retry logic
- **Follow Function**: Improved follow detection (checks if already following)
- **Video Upload**: More robust upload process with better error messages
- **Import Issues**: Added `__init__.py` to social_media package for proper imports

### Security

- **Added .gitignore**: Prevents committing sensitive files (cookies, logs, videos)
- **Environment Variables**: Recommended method for storing credentials
- **.env.example**: Template for environment variable setup

### Removed

- Hardcoded credentials in main.py (moved to config.py)

## [1.0.0] - Initial Release

- Basic TikTok automation functionality
- Cookie-based login
- Comment on user videos
- Follow users
- Video upload
- Simple configuration via main.py
