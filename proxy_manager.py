"""
Proxy Manager for TikTok Automation Bot

Manages proxy servers for multi-account automation.
Supports HTTP, HTTPS, and SOCKS proxies.
"""
import json
import os
import random
import logging
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ProxyManager:
    """Manages proxy servers for multi-account automation."""
    
    def __init__(self, proxies_file="proxies.json"):
        self.proxies_file = proxies_file
        self.proxies = self._load_proxies()
        self.current_index = 0
    
    def _load_proxies(self) -> List[Dict]:
        """Load proxies from JSON file."""
        try:
            if os.path.exists(self.proxies_file):
                with open(self.proxies_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading proxies: {e}")
        return []
    
    def _save_proxies(self):
        """Save proxies to JSON file."""
        try:
            with open(self.proxies_file, 'w') as f:
                json.dump(self.proxies, f, indent=2)
            logger.info(f"Saved {len(self.proxies)} proxies to {self.proxies_file}")
        except Exception as e:
            logger.error(f"Error saving proxies: {e}")
    
    def add_proxy(self, proxy_data: Dict) -> bool:
        """
        Add a new proxy.
        
        Args:
            proxy_data: Dictionary containing proxy information
                Required: host, port
                Optional: protocol, username, password, status
        
        Returns:
            bool: True if added successfully
        """
        try:
            # Normalize proxy data
            proxy_data.setdefault('protocol', 'http')
            proxy_data.setdefault('status', 'active')
            proxy_data.setdefault('added_at', datetime.now().isoformat())
            proxy_data.setdefault('last_checked', None)
            proxy_data.setdefault('success_count', 0)
            proxy_data.setdefault('failure_count', 0)
            
            # Validate required fields
            if not proxy_data.get('host') or not proxy_data.get('port'):
                logger.error("Proxy must have host and port")
                return False
            
            self.proxies.append(proxy_data)
            self._save_proxies()
            logger.info(f"Added proxy: {proxy_data['host']}:{proxy_data['port']}")
            return True
        except Exception as e:
            logger.error(f"Error adding proxy: {e}")
            return False
    
    def add_proxy_from_string(self, proxy_string: str) -> bool:
        """
        Add a proxy from a string.
        
        Supported formats:
        - host:port
        - protocol://host:port
        - protocol://username:password@host:port
        
        Args:
            proxy_string: Proxy string in one of the supported formats
        
        Returns:
            bool: True if added successfully
        """
        try:
            # Parse the proxy string
            if '://' in proxy_string:
                # Full URL format
                parsed = urlparse(proxy_string)
                proxy_data = {
                    'host': parsed.hostname,
                    'port': parsed.port,
                    'protocol': parsed.scheme,
                    'username': parsed.username,
                    'password': parsed.password
                }
            else:
                # Simple host:port format
                parts = proxy_string.split(':')
                if len(parts) >= 2:
                    proxy_data = {
                        'host': parts[0],
                        'port': int(parts[1]),
                        'protocol': 'http'
                    }
                else:
                    logger.error(f"Invalid proxy string format: {proxy_string}")
                    return False
            
            return self.add_proxy(proxy_data)
        except Exception as e:
            logger.error(f"Error parsing proxy string: {e}")
            return False
    
    def get_proxy(self, strategy: str = 'round_robin') -> Optional[Dict]:
        """
        Get a proxy based on the specified strategy.
        
        Args:
            strategy: Selection strategy ('round_robin', 'random', 'least_used')
        
        Returns:
            Proxy data dictionary or None
        """
        try:
            active_proxies = [p for p in self.proxies if p.get('status') == 'active']
            
            if not active_proxies:
                logger.warning("No active proxies available")
                return None
            
            if strategy == 'random':
                return random.choice(active_proxies)
            elif strategy == 'least_used':
                return min(active_proxies, key=lambda p: p.get('use_count', 0))
            else:  # round_robin (default)
                proxy = active_proxies[self.current_index % len(active_proxies)]
                self.current_index += 1
                return proxy
        except Exception as e:
            logger.error(f"Error getting proxy: {e}")
            return None
    
    def get_all_proxies(self, status: Optional[str] = None) -> List[Dict]:
        """
        Get all proxies, optionally filtered by status.
        
        Args:
            status: Filter by status (active, disabled, etc.)
        
        Returns:
            List of proxy dictionaries
        """
        if status:
            return [p for p in self.proxies if p.get('status') == status]
        return self.proxies.copy()
    
    def update_proxy(self, proxy_id: str, updates: Dict) -> bool:
        """
        Update proxy information.
        
        Args:
            proxy_id: Proxy identifier (host:port string or index)
            updates: Dictionary of fields to update
        
        Returns:
            bool: True if updated successfully
        """
        try:
            # Try to find proxy by host:port
            for proxy in self.proxies:
                proxy_str = f"{proxy.get('host')}:{proxy.get('port')}"
                if proxy_str == proxy_id:
                    proxy.update(updates)
                    self._save_proxies()
                    logger.info(f"Updated proxy: {proxy_id}")
                    return True
            
            logger.warning(f"Proxy not found: {proxy_id}")
            return False
        except Exception as e:
            logger.error(f"Error updating proxy: {e}")
            return False
    
    def record_proxy_success(self, proxy_id: str):
        """Record a successful proxy usage."""
        self.update_proxy(proxy_id, {
            'success_count': lambda x: x + 1,
            'last_used': datetime.now().isoformat()
        })
    
    def record_proxy_failure(self, proxy_id: str):
        """Record a failed proxy usage."""
        self.update_proxy(proxy_id, {
            'failure_count': lambda x: x + 1,
            'last_used': datetime.now().isoformat()
        })
    
    def disable_proxy(self, proxy_id: str) -> bool:
        """Disable a proxy."""
        return self.update_proxy(proxy_id, {'status': 'disabled'})
    
    def enable_proxy(self, proxy_id: str) -> bool:
        """Enable a proxy."""
        return self.update_proxy(proxy_id, {'status': 'active'})
    
    def delete_proxy(self, proxy_id: str) -> bool:
        """Delete a proxy."""
        try:
            proxy_str = f"{proxy_id.split('@')[-1]}"  # Handle auth format
            self.proxies = [p for p in self.proxies 
                          if f"{p.get('host')}:{p.get('port')}" != proxy_str]
            self._save_proxies()
            logger.info(f"Deleted proxy: {proxy_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting proxy: {e}")
            return False
    
    def import_proxies(self, filepath: str) -> int:
        """
        Import proxies from a file.
        
        Supported formats:
        - JSON: Array of proxy objects
        - TXT: One proxy per line (host:port or full URL)
        
        Args:
            filepath: Path to proxy file
        
        Returns:
            Number of proxies imported
        """
        imported = 0
        try:
            with open(filepath, 'r') as f:
                if filepath.endswith('.json'):
                    proxies = json.load(f)
                    for proxy in proxies:
                        if isinstance(proxy, dict):
                            if self.add_proxy(proxy):
                                imported += 1
                        elif isinstance(proxy, str):
                            if self.add_proxy_from_string(proxy):
                                imported += 1
                else:
                    # Text file - one proxy per line
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if self.add_proxy_from_string(line):
                                imported += 1
            logger.info(f"Imported {imported} proxies from {filepath}")
        except Exception as e:
            logger.error(f"Error importing proxies: {e}")
        return imported
    
    def export_proxies(self, filepath: str, status: Optional[str] = None) -> int:
        """
        Export proxies to a JSON file.
        
        Args:
            filepath: Path to export file
            status: Filter by status (optional)
        
        Returns:
            Number of proxies exported
        """
        try:
            proxies = self.get_all_proxies(status)
            with open(filepath, 'w') as f:
                json.dump(proxies, f, indent=2)
            logger.info(f"Exported {len(proxies)} proxies to {filepath}")
            return len(proxies)
        except Exception as e:
            logger.error(f"Error exporting proxies: {e}")
            return 0
    
    def check_proxy(self, proxy_data: Dict, timeout: int = 10) -> bool:
        """
        Check if a proxy is working.
        
        Args:
            proxy_data: Proxy data dictionary
            timeout: Request timeout in seconds
        
        Returns:
            bool: True if proxy is working
        """
        try:
            import requests
            
            # Construct proxy URL
            protocol = proxy_data.get('protocol', 'http')
            host = proxy_data.get('host')
            port = proxy_data.get('port')
            username = proxy_data.get('username')
            password = proxy_data.get('password')
            
            if username and password:
                proxy_url = f"{protocol}://{username}:{password}@{host}:{port}"
            else:
                proxy_url = f"{protocol}://{host}:{port}"
            
            # Test proxy
            response = requests.get(
                'http://httpbin.org/ip',
                proxies={'http': proxy_url, 'https': proxy_url},
                timeout=timeout
            )
            
            if response.status_code == 200:
                logger.info(f"Proxy {host}:{port} is working")
                return True
            return False
        except Exception as e:
            logger.error(f"Proxy check failed: {e}")
            return False
    
    def to_selenium_proxy(self, proxy_data: Dict) -> str:
        """
        Convert proxy data to Selenium proxy string format.
        
        Args:
            proxy_data: Proxy data dictionary
        
        Returns:
            Selenium-compatible proxy string
        """
        protocol = proxy_data.get('protocol', 'http')
        host = proxy_data.get('host')
        port = proxy_data.get('port')
        username = proxy_data.get('username')
        password = proxy_data.get('password')
        
        if username and password:
            return f"{protocol}://{username}:{password}@{host}:{port}"
        else:
            return f"{protocol}://{host}:{port}"
    
    def get_proxy_count(self, status: Optional[str] = None) -> int:
        """Get count of proxies, optionally filtered by status."""
        return len(self.get_all_proxies(status))
    
    def fetch_free_proxies(self, timeout: int = 10) -> int:
        """
        Fetch free proxies from public sources.
        
        Returns:
            Number of proxies fetched
        """
        import requests
        
        fetched = 0
        sources = [
            # Free proxy list sources
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
        ]
        
        logger.info("Fetching free proxies from public sources...")
        
        for source in sources:
            try:
                response = requests.get(source, timeout=timeout)
                if response.status_code == 200:
                    lines = response.text.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if ':' in line and not line.startswith('#'):
                            if self.add_proxy_from_string(line):
                                fetched += 1
                    logger.info(f"Fetched {fetched} proxies from {source}")
            except Exception as e:
                logger.warning(f"Failed to fetch from {source}: {e}")
        
        logger.info(f"Total free proxies fetched: {fetched}")
        return fetched
    
    def get_working_proxies(self, max_check: int = 10, timeout: int = 5) -> List[Dict]:
        """
        Get list of working proxies by testing them.
        
        Args:
            max_check: Maximum number of proxies to check
            timeout: Timeout for each proxy check
        
        Returns:
            List of working proxy dictionaries
        """
        import requests
        import concurrent.futures
        
        working = []
        proxies_to_check = self.get_all_proxies('active')[:max_check]
        
        def test_proxy(proxy_data):
            try:
                protocol = proxy_data.get('protocol', 'http')
                host = proxy_data.get('host')
                port = proxy_data.get('port')
                username = proxy_data.get('username')
                password = proxy_data.get('password')
                
                if username and password:
                    proxy_url = f"{protocol}://{username}:{password}@{host}:{port}"
                else:
                    proxy_url = f"{protocol}://{host}:{port}"
                
                response = requests.get(
                    'http://httpbin.org/ip',
                    proxies={'http': proxy_url, 'https': proxy_url},
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    return proxy_data
            except:
                pass
            return None
        
        logger.info(f"Testing {len(proxies_to_check)} proxies...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(test_proxy, proxies_to_check)
            
            for result in results:
                if result:
                    working.append(result)
        
        logger.info(f"Found {len(working)} working proxies")
        return working
