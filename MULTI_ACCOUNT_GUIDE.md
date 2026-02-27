# Multi-Account Guide

Complete guide for using multi-account functionality with the TikTok Automation Bot.

## Table of Contents

1. [Overview](#overview)
2. [Setup](#setup)
3. [Account Management](#account-management)
4. [Proxy Management](#proxy-management)
5. [Email Generation](#email-generation)
6. [Account Creation](#account-creation)
7. [Multi-Account Operations](#multi-account-operations)
8. [Configuration](#configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Overview

The multi-account system allows you to:
- Manage multiple TikTok accounts simultaneously
- Use different proxy addresses for each account
- Automatically generate email addresses for new accounts
- Execute tasks across multiple accounts in parallel
- Batch comment and follow with multiple accounts

## Setup

### 1. Enable Multi-Account Mode

Edit `config.py`:

```python
# Enable multi-account features
MULTI_ACCOUNT_ENABLED = True

# Account storage
ACCOUNTS_FILE = "accounts.json"

# Maximum concurrent bots (threads)
MAX_CONCURRENT_BOTS = 3
```

### 2. Install Additional Dependencies

```bash
pip install -r requirements.txt
```

The new `requests` library is required for proxy checking.

## Account Management

### Interactive Account Management

Run the bot in interactive mode and select "Multi-Account Management":

```bash
python main.py --interactive
```

Then select option "5. Multi-Account Management".

### Adding Accounts Manually

From the multi-account menu, select "2. Add new account":

```
Enter your credentials:
Email: myaccount@gmail.com
Password: mypassword123
Username (optional): myusername
Use proxy? (y/n): y
Proxy host: proxy.example.com
Proxy port: 8080
Proxy protocol (http/https): http
```

### Importing Accounts from File

You can import accounts from JSON or CSV files.

#### JSON Format

Create `my_accounts.json`:

```json
[
  {
    "email": "account1@gmail.com",
    "password": "password1",
    "username": "user1",
    "proxy": {
      "host": "proxy1.example.com",
      "port": 8080,
      "protocol": "http"
    }
  },
  {
    "email": "account2@yahoo.com",
    "password": "password2",
    "username": "user2"
  }
]
```

Import from menu:
```
3. Import accounts from file
Enter file path (JSON or TXT): my_accounts.json
```

#### CSV Format

Create `my_accounts.csv`:

```csv
email,password,username
account1@gmail.com,password1,user1
account2@yahoo.com,password2,user2
```

### Viewing Accounts

Select "1. View all accounts" to see all stored accounts with their status and proxy information.

### Managing Account Status

Enable or disable accounts:
```
5. Enable/Disable account
Enter account email: account1@gmail.com
Enable or disable? (e/d): e
```

### Deleting Accounts

```
4. Delete account
Enter account email to delete: account1@gmail.com
```

## Proxy Management

### What are Proxies?

Proxies allow each account to appear as if it's coming from a different IP address, which helps avoid TikTok's anti-bot detection.

### Supported Proxy Formats

1. **Simple**: `host:port`
   ```
   192.168.1.1:8080
   ```

2. **With Protocol**: `protocol://host:port`
   ```
   http://192.168.1.1:8080
   https://192.168.1.1:8443
   ```

3. **With Authentication**: `protocol://username:password@host:port`
   ```
   http://user:pass@192.168.1.1:8080
   ```

### Adding Proxies

From the multi-account menu, select "10. Proxy management", then "2. Add proxy":

```
Proxy host: 192.168.1.1
Proxy port: 8080
Protocol (http/https): http
Username (optional): myuser
Password (optional): mypass
```

### Importing Proxies from File

#### TXT Format (one proxy per line)

Create `proxies.txt`:

```
192.168.1.1:8080
192.168.1.2:8080
http://user:pass@192.168.1.3:8080
```

#### JSON Format

Create `my_proxies.json`:

```json
[
  {
    "host": "192.168.1.1",
    "port": 8080,
    "protocol": "http"
  },
  {
    "host": "192.168.1.2",
    "port": 8080,
    "protocol": "http",
    "username": "user",
    "password": "pass"
  }
]
```

Import from menu:
```
3. Import proxies from file
Enter file path: proxies.txt
```

### Checking Proxies

```
5. Check proxy
Enter proxy (host:port): 192.168.1.1:8080
```

This will test if the proxy is working by making a request to httpbin.org.

### Proxy Rotation Strategies

Configure in `config.py`:

```python
# Round-robin: Cycle through proxies in order
PROXY_ROTATION_STRATEGY = "round_robin"

# Random: Select proxy randomly each time
PROXY_ROTATION_STRATEGY = "random"

# Least-used: Select proxy with lowest usage count
PROXY_ROTATION_STRATEGY = "least_used"
```

## Email Generation

The bot supports three strategies for generating email addresses for new accounts.

### Strategy 1: Random Email Generation

Generates random email addresses with various domains.

```python
# In config.py
EMAIL_GENERATION_STRATEGY = "random"
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com"]
```

Example generated emails:
- `user123@gmail.com`
- `cool456@yahoo.com`
- `awesome789@outlook.com`

### Strategy 2: Temporary Email Services

Uses temporary email services (requires API integration).

```python
EMAIL_GENERATION_STRATEGY = "temp"
```

Note: This requires integration with specific temp email APIs.

### Strategy 3: Custom Email List

Use your own list of email addresses.

```python
EMAIL_GENERATION_STRATEGY = "custom"
CUSTOM_EMAILS_FILE = "emails.txt"
```

Create `emails.txt`:
```
email1@gmail.com
email2@yahoo.com
email3@outlook.com
```

## Account Creation

### Account Creation Wizard

From the multi-account menu, select "9. Account creation wizard":

```
Account creation will:
- Generate new email addresses
- Generate secure passwords
- Assign proxies (if enabled)
- Create TikTok accounts

⚠️ Note: Actual TikTok account creation requires manual verification
   (email/phone verification, captcha, etc.)
   This will create the account data structure for you.

Proceed? (y/n): y
How many accounts to create? (default: 5): 3
```

### What Gets Created

For each account, the wizard generates:
- **Email**: Based on your configured strategy
- **Password**: Random secure password (12+ characters)
- **Username**: Random username
- **Proxy**: Assigned from your proxy pool (if enabled)

### Manual Verification Required

The bot creates the account data structure, but TikTok requires:
1. Email/phone verification
2. CAPTCHA solving
3. Additional security checks

You'll need to complete these steps manually for each account.

### Exporting Created Accounts

After creation, accounts are saved to `accounts.json`. You can export them:

```python
from account_manager import AccountManager

am = AccountManager("accounts.json")
am.export_accounts("my_accounts_backup.json")
```

## Multi-Account Operations

### Batch Commenting

Have multiple accounts comment on the same video:

From multi-account menu:
```
7. Batch comment with multiple accounts
Enter username to comment on: targetuser
Comments per account: 2

Executing batch comment with 5 accounts...
✓ Completed: 4/5 accounts
```

This will use all active accounts to post comments simultaneously.

### Batch Following

Have multiple accounts follow the same users:

From multi-account menu:
```
8. Batch follow with multiple accounts
Enter usernames (comma-separated): user1,user2,user3

Executing batch follow with 5 accounts...
✓ Batch follow completed
```

### Execute Task on All Accounts

Choose any task and execute on all accounts:

From multi-account menu:
```
6. Execute task on all accounts
Available tasks:
1. Comment on user videos
2. Follow user

Select task (1-2): 1
Enter username to comment on: targetuser
Comments per account: 3
```

### Parallel Execution

The bot uses threading to execute tasks in parallel:

```python
from account_manager import AccountManager
from proxy_manager import ProxyManager
from multi_account_bot import MultiAccountBotManager

# Initialize managers
account_manager = AccountManager("accounts.json")
proxy_manager = ProxyManager("proxies.json")

# Create multi-account manager (max 3 concurrent bots)
multi_bot = MultiAccountBotManager(
    account_manager,
    proxy_manager,
    max_workers=3
)

# Execute task on multiple accounts
results = multi_bot.batch_comment(
    target_user="someuser",
    comments=["Great!", "Awesome!"],
    comment_count=2
)

print(results)
```

## Configuration

### Multi-Account Settings in config.py

```python
# Enable multi-account features
MULTI_ACCOUNT_ENABLED = True

# Account storage file
ACCOUNTS_FILE = "accounts.json"

# Maximum concurrent bots (threads)
MAX_CONCURRENT_BOTS = 3

# Account creation settings
AUTO_CREATE_ACCOUNTS = False
ACCOUNTS_TO_CREATE = 5

# Proxy settings
USE_PROXIES = False
PROXIES_FILE = "proxies.json"
PROXY_ROTATION_STRATEGY = "round_robin"  # Options: "round_robin", "random", "least_used"

# Email generation settings
EMAIL_GENERATION_STRATEGY = "random"  # Options: "random", "temp", "custom"
CUSTOM_EMAILS_FILE = "emails.txt"
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com"]
```

### Example Account Configuration

```json
{
  "email": "myaccount@gmail.com",
  "password": "secure_password",
  "username": "myusername",
  "proxy": {
    "host": "192.168.1.1",
    "port": 8080,
    "protocol": "http"
  },
  "status": "active",
  "created_at": "2024-02-27T10:00:00",
  "last_used": "2024-02-27T12:00:00",
  "cookies": {}
}
```

## Best Practices

### 1. Start Small

- Test with 2-3 accounts first
- Use `MAX_CONCURRENT_BOTS = 1` initially
- Gradually increase as you verify everything works

### 2. Use Quality Proxies

- Use residential or mobile proxies if possible
- Test proxies before using them
- Rotate proxies to avoid detection

### 3. Space Out Operations

- Don't execute too many operations simultaneously
- Use delays between account creations
- Follow rate limits

### 4. Monitor Account Health

- Regularly check account status
- Disable accounts that get flagged
- Keep backup of account credentials

### 5. Secure Your Data

- Keep `accounts.json` secure
- Don't commit it to version control
- Use strong, unique passwords

### 6. Use Different Email Providers

- Mix up email domains (Gmail, Yahoo, Outlook, etc.)
- Don't use the same domain for all accounts

### 7. Human-like Behavior

- Use random delays between actions
- Vary comment texts
- Don't post the same content from all accounts

## Troubleshooting

### Issue: "No accounts available"

**Solution**: Make sure you have added accounts and they are set to "active" status.

```python
from account_manager import AccountManager
am = AccountManager("accounts.json")
print(am.get_account_count(status='active'))
```

### Issue: "No proxies available"

**Solution**: Add proxies to your proxy pool:

```python
from proxy_manager import ProxyManager
pm = ProxyManager("proxies.json")
pm.add_proxy_from_string("192.168.1.1:8080")
```

### Issue: Proxy connection failed

**Solution**: Check if the proxy is working:

```python
from proxy_manager import ProxyManager
pm = ProxyManager("proxies.json")
proxy = pm.get_proxy()
if pm.check_proxy(proxy):
    print("Proxy is working")
else:
    print("Proxy is not working")
```

### Issue: Account login failed

**Solution**: 
1. Check if credentials are correct
2. Try logging in manually first
3. Check if account is not disabled
4. Verify proxy is working if using one

### Issue: Too many concurrent connections

**Solution**: Reduce `MAX_CONCURRENT_BOTS` in config.py:

```python
MAX_CONCURRENT_BOTS = 1  # Start with 1, increase gradually
```

### Issue: Cookies expired

**Solution**: The bot will attempt to re-login. If that fails, login manually and cookies will be saved.

## Advanced Usage

### Custom Task Execution

```python
from multi_account_bot import MultiAccountBotManager

# Initialize
multi_bot = MultiAccountBotManager(account_manager, proxy_manager, max_workers=3)

# Execute custom task
def custom_task(driver, **kwargs):
    # Your custom logic here
    return True

results = multi_bot.execute_task_parallel(
    "custom_task",
    custom_task,
    ["account1@gmail.com", "account2@gmail.com"]
)
```

### Account Rotation

Execute a task multiple times, rotating through accounts:

```python
results = multi_bot.rotate_accounts_task(
    "follow_users",
    follow_task,
    iterations=10,
    users=["user1", "user2", "user3"]
)
```

### Filtering Accounts

Execute task only on specific accounts:

```python
def filter_new_accounts(account):
    # Only use accounts created in the last 7 days
    from datetime import datetime, timedelta
    created = datetime.fromisoformat(account.get('created_at'))
    return datetime.now() - created < timedelta(days=7)

results = multi_bot.execute_task_all_accounts(
    "comment_task",
    comment_task,
    account_filter=filter_new_accounts,
    target_user="someuser",
    comments=["Nice!", "Great!"],
    comment_count=1
)
```

## API Reference

### AccountManager

```python
from account_manager import AccountManager

am = AccountManager("accounts.json")

# Add account
am.add_account({'email': 'test@gmail.com', 'password': 'pass'})

# Get account
account = am.get_account('test@gmail.com')

# Get all accounts
accounts = am.get_all_accounts(status='active')

# Update account
am.update_account('test@gmail.com', {'status': 'disabled'})

# Delete account
am.delete_account('test@gmail.com')

# Import accounts
count = am.import_accounts('accounts.json')

# Export accounts
count = am.export_accounts('backup.json')
```

### ProxyManager

```python
from proxy_manager import ProxyManager

pm = ProxyManager("proxies.json")

# Add proxy
pm.add_proxy({'host': '192.168.1.1', 'port': 8080, 'protocol': 'http'})

# Add from string
pm.add_proxy_from_string("192.168.1.1:8080")

# Get proxy
proxy = pm.get_proxy(strategy='round_robin')

# Check proxy
is_working = pm.check_proxy(proxy)

# Import proxies
count = pm.import_proxies('proxies.txt')

# Export proxies
count = pm.export_proxies('backup.json')
```

### MultiAccountBotManager

```python
from multi_account_bot import MultiAccountBotManager

multi_bot = MultiAccountBotManager(account_manager, proxy_manager, max_workers=3)

# Batch comment
results = multi_bot.batch_comment(target_user, comments, comment_count)

# Batch follow
results = multi_bot.batch_follow(target_users)

# Execute task on all accounts
results = multi_bot.execute_task_all_accounts(task_name, task_func, **kwargs)

# Execute task in parallel
results = multi_bot.execute_task_parallel(task_name, task_func, account_emails, **kwargs)

# Rotate accounts
results = multi_bot.rotate_accounts_task(task_name, task_func, iterations, **kwargs)
```

## Support

For issues or questions:
- Check `bot.log` for detailed error messages
- Review [README.md](README.md) for general documentation
- Contact: [mysteredev](https://t.me/mysteredev) on Telegram

## Disclaimer

Multi-account automation may violate TikTok's Terms of Service. Use responsibly and at your own risk. The developers are not responsible for any consequences of using this feature.
