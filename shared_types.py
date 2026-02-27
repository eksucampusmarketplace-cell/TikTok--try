"""
Shared Types and Utilities for TikTok Automation Bot

Common data structures, type hints, and utility functions
used across multiple modules.
"""
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AccountStatus(str, Enum):
    """Account status enumeration."""
    ACTIVE = "active"
    DISABLED = "disabled"
    BANNED = "banned"
    SUSPENDED = "suspended"
    CREATED = "created"  # Awaiting verification


class ProxyStatus(str, Enum):
    """Proxy status enumeration."""
    ACTIVE = "active"
    DISABLED = "disabled"
    TESTING = "testing"
    FAILED = "failed"


class EmailStrategy(str, Enum):
    """Email generation strategy enumeration."""
    RANDOM = "random"
    GUERRILLA_MAIL = "guerrillamail"
    TEN_MINUTE_MAIL = "10minutemail"
    TEMP_MAIL = "tempmail"
    CUSTOM = "custom"


class ProxyRotationStrategy(str, Enum):
    """Proxy rotation strategy enumeration."""
    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    LEAST_USED = "least_used"


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Account:
    """Account data structure."""
    email: str
    password: str
    username: Optional[str] = None
    proxy: Optional[Dict] = None
    status: AccountStatus = AccountStatus.ACTIVE
    created_at: Optional[str] = None
    last_used: Optional[str] = None
    cookies: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'proxy': self.proxy,
            'status': self.status.value if isinstance(self.status, AccountStatus) else self.status,
            'created_at': self.created_at,
            'last_used': self.last_used,
            'cookies': self.cookies
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Account':
        """Create Account from dictionary."""
        status = data.get('status', 'active')
        # Convert string status to enum if possible
        if isinstance(status, str):
            status = AccountStatus(status)
        
        return cls(
            email=data.get('email'),
            password=data.get('password'),
            username=data.get('username'),
            proxy=data.get('proxy'),
            status=status,
            created_at=data.get('created_at'),
            last_used=data.get('last_used'),
            cookies=data.get('cookies', {})
        )


@dataclass
class Proxy:
    """Proxy data structure."""
    host: str
    port: int
    protocol: str = "http"
    username: Optional[str] = None
    password: Optional[str] = None
    status: ProxyStatus = ProxyStatus.ACTIVE
    added_at: Optional[str] = None
    last_checked: Optional[str] = None
    success_count: int = 0
    failure_count: int = 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = {
            'host': self.host,
            'port': self.port,
            'protocol': self.protocol,
            'status': self.status.value if isinstance(self.status, ProxyStatus) else self.status,
            'added_at': self.added_at,
            'last_checked': self.last_checked,
            'success_count': self.success_count,
            'failure_count': self.failure_count
        }
        
        if self.username:
            result['username'] = self.username
        if self.password:
            result['password'] = self.password
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Proxy':
        """Create Proxy from dictionary."""
        status = data.get('status', 'active')
        if isinstance(status, str):
            status = ProxyStatus(status)
        
        return cls(
            host=data.get('host'),
            port=int(data.get('port', 8080)),
            protocol=data.get('protocol', 'http'),
            username=data.get('username'),
            password=data.get('password'),
            status=status,
            added_at=data.get('added_at'),
            last_checked=data.get('last_checked'),
            success_count=data.get('success_count', 0),
            failure_count=data.get('failure_count', 0)
        )
    
    def to_selenium_proxy(self) -> str:
        """Convert to Selenium-compatible proxy string."""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"
    
    def to_url(self) -> str:
        """Convert to URL format."""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"


@dataclass
class EmailMessage:
    """Email message structure."""
    id: Optional[str] = None
    from_email: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    timestamp: Optional[str] = None
    
    def extract_verification_code(self) -> Optional[str]:
        """Extract 6-digit verification code from body."""
        import re
        match = re.search(r'(\d{6})', self.body or '')
        return match.group(0) if match else None


@dataclass
class Task:
    """Task data structure for queue system."""
    id: str
    type: str  # 'comment', 'follow', 'upload', etc.
    account_email: str
    status: TaskStatus = TaskStatus.PENDING
    data: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    result: Optional[Any] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'type': self.type,
            'account_email': self.account_email,
            'status': self.status.value if isinstance(self.status, TaskStatus) else self.status,
            'data': self.data,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'error': self.error,
            'result': self.result
        }


@dataclass
class BotConfig:
    """Bot configuration structure."""
    headless: bool = False
    browser_mode: str = "uc"
    max_retries: int = 3
    wait_time: int = 10
    max_concurrent_bots: int = 3
    use_proxies: bool = False
    proxy_rotation: ProxyRotationStrategy = ProxyRotationStrategy.ROUND_ROBIN
    email_strategy: EmailStrategy = EmailStrategy.GUERRILLA_MAIL
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'headless': self.headless,
            'browser_mode': self.browser_mode,
            'max_retries': self.max_retries,
            'wait_time': self.wait_time,
            'max_concurrent_bots': self.max_concurrent_bots,
            'use_proxies': self.use_proxies,
            'proxy_rotation': self.proxy_rotation.value if isinstance(self.proxy_rotation, ProxyRotationStrategy) else self.proxy_rotation,
            'email_strategy': self.email_strategy.value if isinstance(self.email_strategy, EmailStrategy) else self.email_strategy
        }


class Result:
    """Generic result wrapper."""
    def __init__(self, success: bool, data: Any = None, error: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error
    
    def __bool__(self) -> bool:
        """Allow use in boolean context."""
        return self.success
    
    def __repr__(self) -> str:
        """String representation."""
        if self.success:
            return f"Result(success={self.success}, data={self.data})"
        return f"Result(success={self.success}, error={self.error})"
