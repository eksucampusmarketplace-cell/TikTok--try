"""
Email Generator for TikTok Automation Bot

Generates temporary email addresses for account creation by scraping
real temporary email services.
Supports various email services and patterns.
"""
import random
import string
import logging
import time
import re
import requests
from typing import Optional, List, Dict
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class EmailProvider(ABC):
    """Abstract base class for email providers."""
    
    @abstractmethod
    def generate_email(self) -> str:
        """Generate a new email address."""
        pass
    
    @abstractmethod
    def get_inbox(self, email: str) -> List[dict]:
        """Get inbox messages for an email."""
        pass
    
    @abstractmethod
    def wait_for_email(self, email: str, timeout: int = 300) -> Optional[Dict]:
        """Wait for incoming email and return first message."""
        pass


class RandomEmailGenerator(EmailProvider):
    """Generates random email addresses with various patterns."""
    
    def __init__(self, domains: Optional[List[str]] = None):
        """
        Initialize the random email generator.
        
        Args:
            domains: List of email domains to use
        """
        self.domains = domains or [
            'gmail.com',
            'yahoo.com',
            'outlook.com',
            'hotmail.com',
            'protonmail.com',
            'mail.com',
        ]
        
        self.prefixes = [
            'user', 'player', 'gamer', 'tech', 'cool', 'awesome',
            'happy', 'lucky', 'smart', 'brave', 'creative', 'wild',
            'alex', 'john', 'mike', 'sarah', 'emma', 'david'
        ]
    
    def generate_email(self) -> str:
        """Generate a random email address."""
        # Random prefix
        prefix = random.choice(self.prefixes)
        
        # Add random number
        number = random.randint(100, 9999)
        
        # Optional random separator
        separator = random.choice(['', '.', '_'])
        
        # Random domain
        domain = random.choice(self.domains)
        
        email = f"{prefix}{separator}{number}@{domain}"
        logger.info(f"Generated email: {email}")
        return email
    
    def get_inbox(self, email: str) -> List[dict]:
        """Get inbox for random email (not supported)."""
        logger.warning("Inbox access not supported for random email generator")
        return []
    
    def wait_for_email(self, email: str, timeout: int = 300) -> Optional[Dict]:
        """Not implemented for random emails."""
        return None


class GuerrillaMailProvider(EmailProvider):
    """
    Guerrilla Mail temporary email provider.
    Scrapes guerrillamail.com for temporary email addresses.
    """
    
    def __init__(self):
        """Initialize Guerrilla Mail provider."""
        self.base_url = "https://www.guerrillamail.com"
        self.api_url = "https://api.guerrillamail.com/ajax.php"
        self.current_email = None
        self.sid_token = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def generate_email(self) -> str:
        """Generate a new Guerrilla Mail email address."""
        try:
            # Request new email
            params = {
                'f': 'get_email_address',
                'ip': '127.0.0.1',
                'agent': 'Firefox_Linux'
            }
            
            response = self.session.get(self.api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                # Parse JSON response
                import json
                data = json.loads(response.text)
                
                if data.get('email_addr'):
                    self.current_email = data['email_addr']
                    self.sid_token = data.get('sid_token')
                    logger.info(f"Generated Guerrilla Mail email: {self.current_email}")
                    return self.current_email
            
            logger.error("Failed to generate Guerrilla Mail email")
            return None
            
        except Exception as e:
            logger.error(f"Error generating Guerrilla Mail email: {e}")
            return None
    
    def get_inbox(self, email: str) -> List[dict]:
        """Get inbox messages for the email."""
        try:
            params = {
                'f': 'check_email',
                'seq': '0',
                'sid_token': self.sid_token,
                'ip': '127.0.0.1',
                'agent': 'Firefox_Linux'
            }
            
            response = self.session.get(self.api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                import json
                data = json.loads(response.text)
                
                if 'list' in data:
                    messages = []
                    for msg in data['list']:
                        messages.append({
                            'id': msg.get('mail_id'),
                            'from': msg.get('mail_from'),
                            'subject': msg.get('mail_subject'),
                            'body': msg.get('mail_body'),
                            'timestamp': msg.get('mail_timestamp')
                        })
                    return messages
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting Guerrilla Mail inbox: {e}")
            return []
    
    def wait_for_email(self, email: str, timeout: int = 300) -> Optional[Dict]:
        """Wait for incoming email and return first message."""
        start_time = time.time()
        check_interval = 5  # Check every 5 seconds
        
        logger.info(f"Waiting for email on {email} (timeout: {timeout}s)...")
        
        while time.time() - start_time < timeout:
            messages = self.get_inbox(email)
            
            if messages:
                logger.info(f"Received email on {email}")
                return messages[0]
            
            time.sleep(check_interval)
        
        logger.warning(f"Timeout waiting for email on {email}")
        return None


class TenMinuteMailProvider(EmailProvider):
    """
    10 Minute Mail temporary email provider.
    Scrapes 10minutemail.com for temporary email addresses.
    """
    
    def __init__(self):
        """Initialize 10 Minute Mail provider."""
        self.base_url = "https://10minutemail.com"
        self.current_email = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def generate_email(self) -> str:
        """Generate a new 10 Minute Mail email address."""
        try:
            response = self.session.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                # Parse email from page
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for email address on page
                email_elem = soup.find('input', {'id': 'mailAddress'})
                if email_elem:
                    self.current_email = email_elem.get('value')
                    logger.info(f"Generated 10 Minute Mail email: {self.current_email}")
                    return self.current_email
                
                # Alternative: look in page content
                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', response.text)
                if email_match:
                    self.current_email = email_match.group(0)
                    logger.info(f"Generated 10 Minute Mail email: {self.current_email}")
                    return self.current_email
            
            logger.error("Failed to generate 10 Minute Mail email")
            return None
            
        except Exception as e:
            logger.error(f"Error generating 10 Minute Mail email: {e}")
            return None
    
    def get_inbox(self, email: str) -> List[dict]:
        """Get inbox messages for the email."""
        try:
            # Try to access inbox
            response = self.session.get(f"{self.base_url}/inbox", timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                messages = []
                # Parse messages from page (structure may vary)
                email_items = soup.find_all('div', class_='email-item')
                
                for item in email_items:
                    messages.append({
                        'id': item.get('data-id'),
                        'from': item.find('span', class_='from').get_text().strip(),
                        'subject': item.find('span', class_='subject').get_text().strip(),
                        'body': item.find('div', class_='body').get_text().strip(),
                        'timestamp': item.find('span', class_='time').get_text().strip()
                    })
                
                return messages
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting 10 Minute Mail inbox: {e}")
            return []
    
    def wait_for_email(self, email: str, timeout: int = 600) -> Optional[Dict]:
        """Wait for incoming email (10 minute mail has 10 min timeout)."""
        start_time = time.time()
        check_interval = 5
        
        logger.info(f"Waiting for email on {email} (timeout: {timeout}s)...")
        
        while time.time() - start_time < timeout:
            messages = self.get_inbox(email)
            
            if messages:
                logger.info(f"Received email on {email}")
                return messages[0]
            
            time.sleep(check_interval)
        
        logger.warning(f"Timeout waiting for email on {email}")
        return None


class TempMailProvider(EmailProvider):
    """
    Temp Mail temporary email provider.
    Uses temp-mail.org service.
    """
    
    def __init__(self):
        """Initialize Temp Mail provider."""
        self.base_url = "https://temp-mail.org"
        self.api_url = "https://web1.temp-mail.org/api/v1"
        self.current_email = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def generate_email(self) -> str:
        """Generate a new Temp Mail email address."""
        try:
            # Generate random email data
            import random
            import string
            
            domains = ['temp-mail.org', '1secmail.com', '1secmail.net', '1secmail.com']
            chars = string.ascii_lowercase + string.digits
            username = ''.join(random.choice(chars) for _ in range(10))
            domain = random.choice(domains)
            
            self.current_email = f"{username}@{domain}"
            
            logger.info(f"Generated Temp Mail email: {self.current_email}")
            return self.current_email
            
        except Exception as e:
            logger.error(f"Error generating Temp Mail email: {e}")
            return None
    
    def get_inbox(self, email: str) -> List[dict]:
        """Get inbox messages for the email."""
        try:
            username, domain = email.split('@')
            
            # Use temp-mail.org API
            url = f"{self.api_url}/messages.php?login={username}&domain={domain}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                import json
                data = json.loads(response.text)
                
                messages = []
                for msg in data:
                    messages.append({
                        'id': msg.get('id'),
                        'from': msg.get('from'),
                        'subject': msg.get('subject'),
                        'body': msg.get('text'),
                        'timestamp': msg.get('created_at')
                    })
                
                return messages
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting Temp Mail inbox: {e}")
            return []
    
    def wait_for_email(self, email: str, timeout: int = 300) -> Optional[Dict]:
        """Wait for incoming email."""
        start_time = time.time()
        check_interval = 5
        
        logger.info(f"Waiting for email on {email} (timeout: {timeout}s)...")
        
        while time.time() - start_time < timeout:
            messages = self.get_inbox(email)
            
            if messages:
                logger.info(f"Received email on {email}")
                return messages[0]
            
            time.sleep(check_interval)
        
        logger.warning(f"Timeout waiting for email on {email}")
        return None


class CustomEmailList:
    """Manages a custom list of email addresses."""
    
    def __init__(self, emails_file: str = "emails.txt"):
        """
        Initialize custom email list.
        
        Args:
            emails_file: Path to file containing email addresses
        """
        self.emails_file = emails_file
        self.emails = self._load_emails()
        self.used_emails = set()
    
    def _load_emails(self) -> List[str]:
        """Load emails from file."""
        try:
            import os
            if os.path.exists(self.emails_file):
                with open(self.emails_file, 'r') as f:
                    return [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"Error loading emails: {e}")
        return []
    
    def get_email(self) -> Optional[str]:
        """Get an unused email from the list."""
        for email in self.emails:
            if email not in self.used_emails:
                self.used_emails.add(email)
                logger.info(f"Using email: {email}")
                return email
        
        logger.warning("No more unused emails available")
        return None
    
    def mark_used(self, email: str):
        """Mark an email as used."""
        self.used_emails.add(email)
    
    def reset_usage(self):
        """Reset all emails to unused."""
        self.used_emails = set()
        logger.info("Reset email usage tracking")


class EmailGenerator:
    """
    Main email generator that supports multiple strategies.
    """
    
    def __init__(self, strategy: str = 'random', **kwargs):
        """
        Initialize email generator.
        
        Args:
            strategy: Generation strategy ('random', 'guerrillamail', '10minutemail', 'tempmail', 'custom')
            **kwargs: Additional arguments for specific strategies
        """
        self.strategy = strategy
        
        if strategy == 'random':
            self.generator = RandomEmailGenerator(
                domains=kwargs.get('domains')
            )
        elif strategy == 'guerrillamail':
            self.generator = GuerrillaMailProvider()
        elif strategy == '10minutemail':
            self.generator = TenMinuteMailProvider()
        elif strategy == 'tempmail':
            self.generator = TempMailProvider()
        elif strategy == 'temp':
            # Legacy - default to guerrillamail
            self.generator = GuerrillaMailProvider()
        elif strategy == 'custom':
            self.generator = CustomEmailList(
                emails_file=kwargs.get('emails_file', 'emails.txt')
            )
        else:
            raise ValueError(f"Unknown email strategy: {strategy}")
        
        logger.info(f"Initialized email generator with strategy: {strategy}")
    
    def generate_email(self) -> str:
        """Generate a new email address."""
        try:
            if self.strategy == 'custom':
                email = self.generator.get_email()
                if not email:
                    raise Exception("No custom emails available")
                return email
            else:
                return self.generator.generate_email()
        except Exception as e:
            logger.error(f"Error generating email: {e}")
            raise
    
    def get_inbox(self, email: str) -> List[dict]:
        """Get inbox messages for an email."""
        try:
            return self.generator.get_inbox(email)
        except Exception as e:
            logger.error(f"Error getting inbox: {e}")
            return []
    
    def wait_for_email(self, email: str, timeout: int = 300) -> Optional[Dict]:
        """Wait for incoming email and return first message."""
        try:
            return self.generator.wait_for_email(email, timeout)
        except Exception as e:
            logger.error(f"Error waiting for email: {e}")
            return None
    
    def bulk_generate(self, count: int) -> List[str]:
        """
        Generate multiple email addresses.
        
        Args:
            count: Number of emails to generate
        
        Returns:
            List of generated email addresses
        """
        emails = []
        logger.info(f"Generating {count} email addresses...")
        
        for i in range(count):
            try:
                email = self.generate_email()
                if email:
                    emails.append(email)
                else:
                    logger.warning(f"Failed to generate email {i+1}/{count}")
            except Exception as e:
                logger.error(f"Error generating email {i+1}/{count}: {e}")
                continue
        
        logger.info(f"Generated {len(emails)}/{count} emails")
        return emails


class EmailValidator:
    """Validates email addresses."""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Check if an email address is valid.
        
        Args:
            email: Email address to validate
        
        Returns:
            bool: True if email is valid
        """
        import re
        
        # Basic email validation regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def extract_email_domain(email: str) -> Optional[str]:
        """Extract the domain from an email address."""
        try:
            return email.split('@')[1] if '@' in email else None
        except:
            return None
    
    @staticmethod
    def normalize_email(email: str) -> str:
        """
        Normalize an email address (lowercase, trim spaces).
        
        Args:
            email: Email address to normalize
        
        Returns:
            Normalized email address
        """
        return email.strip().lower()


def generate_emails(count: int, strategy: str = 'random', **kwargs) -> List[str]:
    """
    Convenience function to generate multiple emails.
    
    Args:
        count: Number of emails to generate
        strategy: Generation strategy
        **kwargs: Additional arguments for email generator
    
    Returns:
        List of generated email addresses
    """
    generator = EmailGenerator(strategy=strategy, **kwargs)
    return generator.bulk_generate(count)
