<div align="center">

# 📱 JunubSMS Python Client

**The easiest way to integrate JunubSMS Bulk SMS into your Python projects.**

</div>

---

## ⚡ 3-Step Quick Start

### 1. Install the Library
```bash
pip install junub-sms
```

### 2. Create Your Script (`send_sms.py`)
Replace `your_username` and `your_password` with your actual JunubSMS credentials.

```python
from junub_sms import JunubSMS

# 1. Connect to JunubSMS (Recommended: use "with" so it closes automatically)
with JunubSMS(username="your_username", password="your_password") as sms:
    
    # 2. Send an SMS
    response = sms.send(
        to="256700000000",          # Recipient phone number (with country code)
        msg="Hello from JunubSMS!",  # Message content
        sender="MyCompany"          # Optional: your approved Sender ID
    )
    print(f"✓ Message Sent! ID: {response[0]['id']}")
    
    # 3. Check your remaining balance
    balance_info = sms.get_credit()
    print(f"✓ Remaining Balance: {balance_info.get('balance')} credits")
```

### 3. Run It!
```bash
python send_sms.py
```

---

## 📖 Common Examples

### Send to Multiple People at Once
Pass a list of phone numbers instead of a single string:

```python
with JunubSMS(username="your_username", password="your_password") as sms:
    sms.send(
        to=["256700000000", "256700000001", "256700000002"],
        msg="Hello everyone!"
    )
```

### Check Detailed Account Credit
Find out your credit limit, how much you have used, and your current balance:

```python
with JunubSMS(username="your_username", password="your_password") as sms:
    credit = sms.get_credit()
    print(f"Total Limit: {credit.get('limit')}")
    print(f"Used So Far: {credit.get('used')}")
    print(f"Current Balance: {credit.get('balance')}")
```

### Checking Sent Messages & Inbox
Retrieve logs of sent messages, delivery reports, or incoming replies:

```python
with JunubSMS(username="your_username", password="your_password") as sms:
    # See sent messages status
    sent_messages = sms.get_outgoing_status(limit=10)
    
    # See incoming messages (replies)
    replies = sms.get_incoming()
```

---

## 🛡️ Error Handling
If something goes wrong (e.g., wrong password or no credits left), the library will raise a specific error:

```python
from junub_sms import JunubSMS
from junub_sms.errors import AuthError, CreditError, JunubSMSError

try:
    with JunubSMS(username="wrong_user", password="password") as sms:
        sms.send(to="256700000000", msg="Hello")
except AuthError:
    print("Oops! Username or password was incorrect.")
except CreditError:
    print("Oops! You do not have enough credits to send this message.")
except JunubSMSError as e:
    print(f"An API error occurred: {e}")
```

---

## ⚙️ Advanced Features

For advanced requirements (such as managing contacts, user groups, or admin operations like creating user accounts and adding/deducting credits), see the method documentation in [client.py](file:///d:/Target%20Media%20Group/Junub%20SMS%20Python%20Client/junub_sms_python_client/junub_sms/client.py).

### 🧪 Running Tests
If you are developing this library and want to run tests:
```bash
pip install pytest
pytest
```
