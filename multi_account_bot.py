"""
Multi-Account Bot Manager for TikTok Automation Bot

Manages simultaneous operations across multiple TikTok accounts.
Supports threading, proxy management, and task distribution.
"""
import logging
import threading
import time
from typing import List, Dict, Optional, Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from datetime import datetime

from seleniumbase import Driver
from account_manager import AccountManager
from proxy_manager import ProxyManager
from email_generator import EmailGenerator

logger = logging.getLogger(__name__)


class AccountBot:
    """Bot instance for a single TikTok account."""
    
    def __init__(self, account_data: Dict, proxy_manager: Optional[ProxyManager] = None):
        """
        Initialize account bot.
        
        Args:
            account_data: Account information dictionary
            proxy_manager: Optional proxy manager for this account
        """
        self.account_data = account_data
        self.proxy_manager = proxy_manager
        self.driver = None
        self.is_running = False
    
    def initialize_driver(self) -> bool:
        """
        Initialize Selenium WebDriver for this account.
        
        Returns:
            bool: True if driver initialized successfully
        """
        try:
            # Get proxy if available
            proxy_args = {}
            if self.proxy_manager and self.account_data.get('proxy'):
                proxy_data = self.account_data['proxy']
                proxy_string = self.proxy_manager.to_selenium_proxy(proxy_data)
                proxy_args['proxy_string'] = proxy_string
                logger.info(f"Using proxy for {self.account_data.get('email')}")
            
            # Initialize driver
            driver_args = {
                'uc': True,
                'headless': False,
                **proxy_args
            }
            
            self.driver = Driver(**driver_args)
            self.driver.maximize_window()
            
            logger.info(f"Driver initialized for {self.account_data.get('email')}")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing driver: {e}")
            return False
    
    def login(self) -> bool:
        """
        Login to TikTok with this account.
        
        Returns:
            bool: True if login successful
        """
        if not self.driver:
            logger.error("Driver not initialized")
            return False
        
        try:
            from social_media import tiktok
            
            email = self.account_data.get('email')
            password = self.account_data.get('password')
            cookies = self.account_data.get('cookies', {})
            
            # Try cookie login first
            if cookies:
                logger.info(f"Attempting cookie login for {email}")
                success = tiktok.login(self.driver, email, password, cookies)
                if success:
                    return True
            
            # Fallback to credential login
            logger.info(f"Attempting credential login for {email}")
            success = tiktok.login(self.driver, email, password, None)
            
            if success:
                # Save new cookies
                new_cookies = self.driver.get_cookies()
                self.account_data['cookies'] = new_cookies
                logger.info(f"Login successful for {email}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False
    
    def execute_task(self, task_name: str, task_func: Callable, **kwargs) -> Any:
        """
        Execute a task for this account.
        
        Args:
            task_name: Name of the task
            task_func: Function to execute
            **kwargs: Arguments to pass to task function
        
        Returns:
            Task result
        """
        try:
            logger.info(f"Executing task '{task_name}' for {self.account_data.get('email')}")
            
            # Execute task
            result = task_func(self.driver, **kwargs)
            
            logger.info(f"Task '{task_name}' completed for {self.account_data.get('email')}")
            return result
            
        except Exception as e:
            logger.error(f"Error executing task '{task_name}': {e}")
            raise
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info(f"Driver closed for {self.account_data.get('email')}")
            except Exception as e:
                logger.error(f"Error closing driver: {e}")


class MultiAccountBotManager:
    """Manages multiple TikTok bot instances simultaneously."""
    
    def __init__(self, account_manager: AccountManager, 
                 proxy_manager: Optional[ProxyManager] = None,
                 max_workers: int = 3):
        """
        Initialize multi-account manager.
        
        Args:
            account_manager: Account manager instance
            proxy_manager: Optional proxy manager
            max_workers: Maximum number of concurrent bots
        """
        self.account_manager = account_manager
        self.proxy_manager = proxy_manager
        self.max_workers = max_workers
        self.active_bots: Dict[str, AccountBot] = {}
        self.results: Queue = Queue()
    
    def create_bot(self, account_data: Dict) -> AccountBot:
        """Create a new bot instance for an account."""
        bot = AccountBot(account_data, self.proxy_manager)
        
        # Assign proxy if available and account doesn't have one
        if self.proxy_manager and not account_data.get('proxy'):
            proxy = self.proxy_manager.get_proxy(strategy='round_robin')
            if proxy:
                account_data['proxy'] = proxy
                logger.info(f"Assigned proxy to {account_data.get('email')}")
        
        return bot
    
    def execute_task_single_account(self, account_email: str, 
                                    task_name: str, 
                                    task_func: Callable,
                                    **kwargs) -> Any:
        """
        Execute a task on a single account.
        
        Args:
            account_email: Email of the account to use
            task_name: Name of the task
            task_func: Function to execute
            **kwargs: Arguments for the task function
        
        Returns:
            Task result
        """
        # Get account
        account = self.account_manager.get_account(account_email)
        if not account:
            logger.error(f"Account not found: {account_email}")
            return None
        
        # Create bot
        bot = self.create_bot(account)
        
        try:
            # Initialize driver
            if not bot.initialize_driver():
                return None
            
            # Login
            if not bot.login():
                return None
            
            # Execute task
            result = bot.execute_task(task_name, task_func, **kwargs)
            
            # Update account metadata
            self.account_manager.update_last_used(account_email)
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing task on {account_email}: {e}")
            return None
        finally:
            bot.cleanup()
    
    def execute_task_all_accounts(self, task_name: str,
                                   task_func: Callable,
                                   account_filter: Optional[Callable] = None,
                                   **kwargs) -> Dict[str, Any]:
        """
        Execute a task on all accounts.
        
        Args:
            task_name: Name of the task
            task_func: Function to execute
            account_filter: Optional function to filter accounts
            **kwargs: Arguments for the task function
        
        Returns:
            Dictionary of results by account email
        """
        # Get accounts
        accounts = self.account_manager.get_all_accounts(status='active')
        
        if account_filter:
            accounts = [a for a in accounts if account_filter(a)]
        
        if not accounts:
            logger.warning("No accounts available for task")
            return {}
        
        logger.info(f"Executing task '{task_name}' on {len(accounts)} accounts")
        
        results = {}
        
        # Execute on each account (sequentially for now)
        for account in accounts:
            email = account.get('email')
            result = self.execute_task_single_account(
                email, task_name, task_func, **kwargs
            )
            results[email] = result
            
            # Delay between accounts
            time.sleep(random.uniform(2, 5))
        
        successful = sum(1 for r in results.values() if r)
        logger.info(f"Task '{task_name}' completed: {successful}/{len(accounts)} successful")
        
        return results
    
    def execute_task_parallel(self, task_name: str,
                              task_func: Callable,
                              account_emails: List[str],
                              **kwargs) -> Dict[str, Any]:
        """
        Execute a task in parallel across multiple accounts.
        
        Args:
            task_name: Name of the task
            task_func: Function to execute
            account_emails: List of account emails to use
            **kwargs: Arguments for the task function
        
        Returns:
            Dictionary of results by account email
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks
            future_to_email = {
                executor.submit(
                    self.execute_task_single_account,
                    email, task_name, task_func, **kwargs
                ): email
                for email in account_emails
            }
            
            # Collect results
            for future in as_completed(future_to_email):
                email = future_to_email[future]
                try:
                    results[email] = future.result()
                except Exception as e:
                    logger.error(f"Task failed for {email}: {e}")
                    results[email] = None
        
        successful = sum(1 for r in results.values() if r)
        logger.info(f"Parallel task '{task_name}' completed: {successful}/{len(account_emails)} successful")
        
        return results
    
    def batch_comment(self, target_user: str, comments: List[str], 
                     comment_count: int = 1) -> Dict[str, Any]:
        """
        Batch comment across multiple accounts.
        
        Args:
            target_user: Target TikTok user to comment on
            comments: List of comments to choose from
            comment_count: Number of comments per account
        
        Returns:
            Dictionary of results by account email
        """
        from social_media import tiktok
        
        def comment_task(driver, **kwargs):
            return tiktok.comment_user_video(
                driver,
                kwargs['target_user'],
                kwargs['comments'],
                kwargs['comment_count']
            )
        
        accounts = self.account_manager.get_all_accounts(status='active')
        account_emails = [a.get('email') for a in accounts[:self.max_workers]]
        
        return self.execute_task_parallel(
            f"comment_{target_user}",
            comment_task,
            account_emails,
            target_user=target_user,
            comments=comments,
            comment_count=comment_count
        )
    
    def batch_follow(self, target_users: List[str]) -> Dict[str, Dict[str, bool]]:
        """
        Batch follow users across multiple accounts.
        
        Args:
            target_users: List of users to follow
        
        Returns:
            Dictionary mapping account emails to results
        """
        from social_media import tiktok
        
        results = {}
        
        for target_user in target_users:
            def follow_task(driver, **kwargs):
                return tiktok.follow(driver, kwargs['target_user'])
            
            accounts = self.account_manager.get_all_accounts(status='active')
            account_emails = [a.get('email') for a in accounts[:self.max_workers]]
            
            task_results = self.execute_task_parallel(
                f"follow_{target_user}",
                follow_task,
                account_emails,
                target_user=target_user
            )
            
            # Aggregate results
            for email, result in task_results.items():
                if email not in results:
                    results[email] = {}
                results[email][target_user] = result
            
            # Delay between users
            time.sleep(random.uniform(3, 6))
        
        return results
    
    def rotate_accounts_task(self, task_name: str,
                             task_func: Callable,
                             iterations: int,
                             **kwargs) -> List[Dict[str, Any]]:
        """
        Execute a task multiple times, rotating through accounts.
        
        Args:
            task_name: Name of the task
            task_func: Function to execute
            iterations: Number of iterations
            **kwargs: Arguments for the task function
        
        Returns:
            List of results per iteration
        """
        accounts = self.account_manager.get_all_accounts(status='active')
        if not accounts:
            logger.warning("No accounts available")
            return []
        
        results = []
        
        for i in range(iterations):
            # Rotate through accounts
            account = accounts[i % len(accounts)]
            email = account.get('email')
            
            result = self.execute_task_single_account(
                email, f"{task_name}_{i}", task_func, **kwargs
            )
            
            results.append({
                'iteration': i + 1,
                'account': email,
                'result': result
            })
            
            # Delay between iterations
            time.sleep(random.uniform(5, 10))
        
        return results
    
    def get_status(self) -> Dict:
        """Get status of all accounts."""
        return {
            'total_accounts': self.account_manager.get_account_count(),
            'active_accounts': self.account_manager.get_account_count(status='active'),
            'total_proxies': self.proxy_manager.get_proxy_count() if self.proxy_manager else 0,
            'active_proxies': self.proxy_manager.get_proxy_count(status='active') if self.proxy_manager else 0,
            'max_workers': self.max_workers
        }


def create_driver_with_proxy(proxy_data: Dict) -> Driver:
    """
    Create a Selenium driver with proxy configuration.
    
    Args:
        proxy_data: Proxy data dictionary
    
    Returns:
        Configured Driver instance
    """
    proxy_string = f"{proxy_data.get('protocol', 'http')}://{proxy_data.get('host')}:{proxy_data.get('port')}"
    
    if proxy_data.get('username') and proxy_data.get('password'):
        proxy_string = f"{proxy_data.get('protocol', 'http')}://{proxy_data.get('username')}:{proxy_data.get('password')}@{proxy_data.get('host')}:{proxy_data.get('port')}"
    
    return Driver(uc=True, proxy_string=proxy_string)
