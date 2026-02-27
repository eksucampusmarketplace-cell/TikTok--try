"""
Social Media Automation Package

This package contains automation modules for various social media platforms.
"""

from .tiktok import (
    TikTokBot,
    tiktok_bot,
    save_cookies,
    load_cookies,
    login,
    comment_user_video,
    follow,
    upload,
    log_report,
)

__all__ = [
    'TikTokBot',
    'tiktok_bot',
    'save_cookies',
    'load_cookies',
    'login',
    'comment_user_video',
    'follow',
    'upload',
    'log_report',
]
