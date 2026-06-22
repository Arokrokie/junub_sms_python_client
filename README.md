<div align="center">

# 📱 JunubSMS Python Client

**A lightweight, type-safe Python client for the JunubSMS Bulk SMS API**

</div>

---

## 📖 Overview

JunubSMS Python Client is a **simple, intuitive, and reliable** library for interacting with the JunubSMS Bulk SMS API. Built with developer experience in mind, it provides a clean interface for sending SMS messages, managing contacts, checking credit, and performing administrative tasks.

### 🎯 Why Use This Library?

| Feature               | Benefit                                 |
| --------------------- | --------------------------------------- |
| **🚀 Simple API**     | Send SMS in one line of code            |
| **📝 Type Hints**     | Full IDE autocomplete support           |
| **🔒 Error Handling** | Specific exceptions for each error type |
| **🧪 Tested**         | Comprehensive test coverage             |
| **⚡ Lightweight**    | Only `requests` dependency              |
| **📚 Complete**       | All API operations supported            |

---

## 🚀 Quick Start

### Installation

```bash
# Install via pip
pip install junub-sms

# Or install from source
git clone https://github.com/Arokrokie/junub_sms_python_client.git
cd junub-sms-python-client
pip install -e .
```

### Basic Usage

#### Sending SMS

```python
from junub_sms import JunubSMS

# Initialize the client (automatically authenticates and retrieves session token)
sms = JunubSMS(username="your_username", password="your_password")

try:
    # Send a single SMS
    result = sms.send(
        to="256700000000",
        msg="Hello from JunubSMS!",
        sender="MySender"  # Optional: registered sender ID
    )
    print(f"Message sent! ID: {result[0]['id']}")

    # Send to multiple recipients
    results = sms.send(
        to=["256700000000", "256700000001"],
        msg="Hello to multiple recipients!",
        sender="MySender"
    )
    for res in results:
        print(f"Sent to {res['to']} - ID: {res['id']}")

finally:
    # Always close the session when done
    sms.close()
```

#### Using the Context Manager (Recommended)

To avoid manually calling `.close()`, you can use the client as a context manager:

```python
from junub_sms import JunubSMS

with JunubSMS(username="your_username", password="your_password") as sms:
    result = sms.send(to="256700000000", msg="Hello via Context Manager!")
    print(result)
```

---

## 🛠️ Advanced Features

### Checking Balance & Credits

```python
with JunubSMS(username="your_username", password="your_password") as sms:
    credit = sms.get_credit()
    print(f"Credit Limit: {credit.get('limit')}")
    print(f"Credit Used: {credit.get('used')}")
    print(f"Remaining Credit: {credit.get('balance')}")
```

### Checking Delivery Reports & Inbox

```python
with JunubSMS(username="your_username", password="your_password") as sms:
    # Get status of outgoing messages (delivery status)
    outgoing = sms.get_outgoing_status(limit=50) # default: 100
    
    # Get incoming messages (received)
    incoming = sms.get_incoming()
    
    # Get inbox messages
    inbox = sms.get_inbox()
    
    # Get sandbox messages
    sandbox = sms.get_sandbox()
```

### Managing Contacts & Groups

```python
with JunubSMS(username="your_username", password="your_password") as sms:
    # Search contacts by keyword
    contacts = sms.get_contacts(keyword="John")
    
    # Search groups by keyword/name
    groups = sms.get_groups(keyword="Customers")
```

### Administrative Operations (Admin Level Only)

If your account has administrative privileges, you can perform administrative tasks:

```python
with JunubSMS(username="admin_user", password="admin_password") as sms:
    # Add a new user account
    sms.add_account(
        username="new_user", 
        password="secure_password", 
        name="John Doe", 
        email="john@example.com"
    )
    
    # Add credits to an account
    sms.credit_add(username="new_user", amount=500.0)
    
    # Deduct credits from an account
    sms.credit_deduct(username="new_user", amount=50.0)
    
    # View account credit
    credit_info = sms.credit_view(username="new_user")
    
    # Ban/Unban account
    sms.ban_account(username="new_user")
    sms.unban_account(username="new_user")
    
    # Inject a message directly into the SMS gateway
    sms.inject_message(
        sender="System", 
        msg="System Alert", 
        recipient="256700000000", 
        smsc="gateway_route"
    )
    
    # Remove account
    sms.remove_account(username="new_user")
```

---

## ⚠️ Error Handling

The client maps API error codes to specific, descriptive Python exceptions so you can handle different failure scenarios gracefully.

```python
from junub_sms import JunubSMS
from junub_sms.errors import AuthError, CreditError, MessageError, NotFoundError, JunubSMSError

try:
    with JunubSMS(username="user", password="wrong_password") as sms:
        sms.send(to="256700000000", msg="Hello!")
except AuthError as e:
    print(f"Authentication failed: {e.message} (Code: {e.code})")
except CreditError as e:
    print(f"Insufficient credits: {e.message} (Code: {e.code})")
except MessageError as e:
    print(f"Message failed to send: {e.message} (Code: {e.code})")
except NotFoundError as e:
    print(f"Resource not found: {e.message} (Code: {e.code})")
except JunubSMSError as e:
    print(f"API Error: {e.message} (Code: {e.code})")
```

---

## 🧪 Running Tests

To run the unit tests, install development dependencies and run `pytest`:

```bash
pip install -r requirements.txt pytest
pytest
```
