"""
Account Manager for TikTok Automation Bot

Handles creation, storage, and management of multiple TikTok accounts
with support for proxies and email generation.
"""
import json
import os
import random
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class AccountManager:
    """Manages multiple TikTok accounts with proxy and email support."""
    
    def __init__(self, accounts_file="accounts.json"):
        self.accounts_file = accounts_file
        self.accounts = self._load_accounts()
    
    def _load_accounts(self) -> List[Dict]:
        """Load accounts from JSON file."""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading accounts: {e}")
        return []
    
    def _save_accounts(self):
        """Save accounts to JSON file."""
        try:
            with open(self.accounts_file, 'w') as f:
                json.dump(self.accounts, f, indent=2)
            logger.info(f"Saved {len(self.accounts)} accounts to {self.accounts_file}")
        except Exception as e:
            logger.error(f"Error saving accounts: {e}")
    
    def add_account(self, account_data: Dict) -> bool:
        """
        Add a new account to the manager.
        
        Args:
            account_data: Dictionary containing account information
                Required keys: email, password, username (optional)
                Optional keys: proxy, cookies, status, created_at, last_used
        
        Returns:
            bool: True if added successfully
        """
        try:
            # Add metadata
            account_data.setdefault('status', 'active')
            account_data.setdefault('created_at', datetime.now().isoformat())
            account_data.setdefault('last_used', None)
            account_data.setdefault('cookies', {})
            
            self.accounts.append(account_data)
            self._save_accounts()
            logger.info(f"Added account: {account_data.get('email')}")
            return True
        except Exception as e:
            logger.error(f"Error adding account: {e}")
            return False
    
    def get_account(self, account_id: Optional[str] = None) -> Optional[Dict]:
        """
        Get a specific account by ID or random account.
        
        Args:
            account_id: Optional account ID (email or index)
        
        Returns:
            Account data dictionary or None
        """
        try:
            if not self.accounts:
                return None
            
            if account_id:
                # Search by email
                for account in self.accounts:
                    if account.get('email') == account_id:
                        return account
                # Try as index
                try:
                    idx = int(account_id)
                    if 0 <= idx < len(self.accounts):
                        return self.accounts[idx]
                except ValueError:
                    pass
                return None
            
            # Return random active account
            active_accounts = [a for a in self.accounts if a.get('status') == 'active']
            if active_accounts:
                return random.choice(active_accounts)
            return None
        except Exception as e:
            logger.error(f"Error getting account: {e}")
            return None
    
    def get_all_accounts(self, status: Optional[str] = None) -> List[Dict]:
        """
        Get all accounts, optionally filtered by status.
        
        Args:
            status: Filter by status (active, disabled, etc.)
        
        Returns:
            List of account dictionaries
        """
        if status:
            return [a for a in self.accounts if a.get('status') == status]
        return self.accounts.copy()
    
    def update_account(self, email: str, updates: Dict) -> bool:
        """
        Update account information.
        
        Args:
            email: Account email to update
            updates: Dictionary of fields to update
        
        Returns:
            bool: True if updated successfully
        """
        try:
            for account in self.accounts:
                if account.get('email') == email:
                    account.update(updates)
                    self._save_accounts()
                    logger.info(f"Updated account: {email}")
                    return True
            logger.warning(f"Account not found: {email}")
            return False
        except Exception as e:
            logger.error(f"Error updating account: {e}")
            return False
    
    def update_last_used(self, email: str):
        """Update the last used timestamp for an account."""
        self.update_account(email, {'last_used': datetime.now().isoformat()})
    
    def disable_account(self, email: str) -> bool:
        """Disable an account."""
        return self.update_account(email, {'status': 'disabled'})
    
    def enable_account(self, email: str) -> bool:
        """Enable an account."""
        return self.update_account(email, {'status': 'active'})
    
    def delete_account(self, email: str) -> bool:
        """Delete an account."""
        try:
            self.accounts = [a for a in self.accounts if a.get('email') != email]
            self._save_accounts()
            logger.info(f"Deleted account: {email}")
            return True
        except Exception as e:
            logger.error(f"Error deleting account: {e}")
            return False
    
    def get_account_count(self, status: Optional[str] = None) -> int:
        """Get count of accounts, optionally filtered by status."""
        return len(self.get_all_accounts(status))
    
    def import_accounts(self, filepath: str) -> int:
        """
        Import accounts from a JSON or CSV file.
        
        Args:
            filepath: Path to import file
        
        Returns:
            Number of accounts imported
        """
        imported = 0
        try:
            with open(filepath, 'r') as f:
                if filepath.endswith('.json'):
                    accounts = json.load(f)
                    for account in accounts:
                        if self.add_account(account):
                            imported += 1
                elif filepath.endswith('.csv'):
                    # Simple CSV import (assuming header row)
                    import csv
                    reader = csv.DictReader(f)
                    for row in reader:
                        if self.add_account(dict(row)):
                            imported += 1
            logger.info(f"Imported {imported} accounts from {filepath}")
        except Exception as e:
            logger.error(f"Error importing accounts: {e}")
        return imported
    
    def export_accounts(self, filepath: str, status: Optional[str] = None) -> int:
        """
        Export accounts to a JSON file.
        
        Args:
            filepath: Path to export file
            status: Filter by status (optional)
        
        Returns:
            Number of accounts exported
        """
        try:
            accounts = self.get_all_accounts(status)
            with open(filepath, 'w') as f:
                json.dump(accounts, f, indent=2)
            logger.info(f"Exported {len(accounts)} accounts to {filepath}")
            return len(accounts)
        except Exception as e:
            logger.error(f"Error exporting accounts: {e}")
            return 0


class AccountCreator:
    """Automated TikTok account creation with proxy and email support."""
    
    def __init__(self, account_manager: AccountManager, proxy_manager=None, email_generator=None):
        self.account_manager = account_manager
        self.proxy_manager = proxy_manager
        self.email_generator = email_generator
    
    def create_account(self, driver, use_proxy: bool = True, 
                       email: Optional[str] = None, password: Optional[str] = None) -> Optional[Dict]:
        """
        Create a new TikTok account.
        
        Args:
            driver: Selenium WebDriver instance
            use_proxy: Whether to use a proxy for this account
            email: Custom email (or None to generate)
            password: Custom password (or None to generate)
        
        Returns:
            Account data dictionary or None
        """
        try:
            logger.info("Starting TikTok account creation...")
            
            # Get or generate email
            if not email and self.email_generator:
                email = self.email_generator.generate_email()
            elif not email:
                logger.error("No email provided and no email generator available")
                return None
            
            # Generate password if not provided
            if not password:
                password = self._generate_password()
            
            # Get proxy if requested
            proxy = None
            if use_proxy and self.proxy_manager:
                proxy = self.proxy_manager.get_proxy()
            
            # Create account (this would need actual TikTok signup automation)
            # Note: TikTok signup requires email/phone verification, captcha, etc.
            # This is a placeholder for the actual implementation
            account_data = {
                'email': email,
                'password': password,
                'proxy': proxy,
                'username': self._generate_username(),
                'status': 'created',  # Needs verification
                'created_at': datetime.now().isoformat(),
                'cookies': {}
            }
            
            # Save account
            if self.account_manager.add_account(account_data):
                logger.info(f"Account created successfully: {email}")
                return account_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            return None
    
    def _generate_password(self, length: int = 12) -> str:
        """Generate a random secure password."""
        import string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def _generate_username(self) -> str:
        """Generate a random username."""
        adjectives = ['cool', 'awesome', 'happy', 'lucky', 'smart', 'brave', 'creative', 'wild']
        nouns = ['tiger', 'eagle', 'dolphin', 'wolf', 'bear', 'lion', 'fox', 'hawk']
        return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(100, 999)}"
    
    def bulk_create_accounts(self, count: int, driver_func) -> List[Dict]:
        """
        Create multiple accounts.
        
        Args:
            count: Number of accounts to create
            driver_func: Function to create new drivers (for proxy support)
        
        Returns:
            List of created account data
        """
        created_accounts = []
        logger.info(f"Starting bulk account creation: {count} accounts")
        
        for i in range(count):
            try:
                # Create new driver for each account
                driver = driver_func()
                
                # Create account
                account = self.create_account(driver, use_proxy=True)
                if account:
                    created_accounts.append(account)
                
                # Close driver
                try:
                    driver.quit()
                except:
                    pass
                
                # Delay between account creations
                import time
                delay = random.uniform(5, 15)
                logger.info(f"Waiting {delay:.1f}s before next account creation...")
                time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error creating account {i+1}/{count}: {e}")
                continue
        
        logger.info(f"Created {len(created_accounts)}/{count} accounts")
        return created_accounts
