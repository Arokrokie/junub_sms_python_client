"""
Example: Send SMS with JunubSMS
"""

from junub_sms import JunubSMS

# Your credentials
USERNAME = "your_username"
PASSWORD = "your_password"

# Create client
sms = JunubSMS(USERNAME, PASSWORD)

try:
    # Send SMS
    result = sms.send(
        to="256700000000",
        message="Hello from JunubSMS!",
        sender="MySender"  # Must be registered
    )
    
    print(f"✓ Message sent! ID: {result[0]['id']}")
    
    # Check credit
    credit = sms.get_credit()
    print(f"✓ Balance: {credit.get('balance', 0)}")
    
except Exception as e:
    print(f"✗ Error: {e}")
finally:
    sms.close()