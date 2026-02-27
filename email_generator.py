"""
Email Generator for TikTok Automation Bot

Generates temporary email addresses for account creation.
Supports various email services and patterns.
"""
import random
import string
import logging
from typing import Optional, List
from abc import ABC, abstractmethod

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


class TempEmailProvider(EmailProvider):
    """
    Wrapper for temporary email services.
    Note: This would require integration with specific temp email APIs.
    """
    
    def __init__(self, service: str = 'guerrillamail'):
        """
        Initialize temp email provider.
        
        Args:
            service: Temp email service name
        """
        self.service = service
        self.current_email = None
    
    def generate_email(self) -> str:
        """Generate a temporary email address."""
        # This would integrate with actual temp email APIs
        # For now, returning a placeholder
        import time
        timestamp = int(time.time())
        self.current_email = f"temp{timestamp}@tempmail.com"
        logger.info(f"Generated temp email: {self.current_email}")
        return self.current_email
    
    def get_inbox(self, email: str) -> List[dict]:
        """Get inbox messages for temporary email."""
        # This would integrate with actual temp email APIs
        logger.info(f"Checking inbox for: {email}")
        return []


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
            strategy: Generation strategy ('random', 'temp', 'custom')
            **kwargs: Additional arguments for specific strategies
        """
        self.strategy = strategy
        
        if strategy == 'random':
            self.generator = RandomEmailGenerator(
                domains=kwargs.get('domains')
            )
        elif strategy == 'temp':
            self.generator = TempEmailProvider(
                service=kwargs.get('service', 'guerrillamail')
            )
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
                emails.append(email)
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
