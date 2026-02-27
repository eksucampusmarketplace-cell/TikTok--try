# Changelog

All notable changes to the TikTok Automation Bot project will be documented in this file.

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
