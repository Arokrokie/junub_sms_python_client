"""
Error codes for JunubSMS API.
All errors defined in one place for easy management.
"""

class JunubSMSError(Exception):
    """Base exception for all JunubSMS errors."""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

# Specific exception types
class AuthError(JunubSMSError):
    """Authentication errors (100-106)"""
    pass

class CreditError(JunubSMSError):
    """Credit errors (103)"""
    pass

class MessageError(JunubSMSError):
    """Message errors (200-206)"""
    pass

class NotFoundError(JunubSMSError):
    """Not found errors (400-402, 501)"""
    pass

class AdminError(JunubSMSError):
    """Admin errors (600-626)"""
    pass

# Error code mapping - all errors in one dictionary
ERRORS = {
    # Authentication errors
    "100": {"class": AuthError, "msg": "Authentication failed - check username/password"},
    "101": {"class": AuthError, "msg": "Invalid operation type"},
    "102": {"class": AuthError, "msg": "One or more fields are empty"},
    "104": {"class": AuthError, "msg": "Webservice token not available"},
    "105": {"class": AuthError, "msg": "Webservice token not enabled for this user"},
    "106": {"class": AuthError, "msg": "Webservice token not allowed from this IP"},
    
    # Credit error
    "103": {"class": CreditError, "msg": "Not enough credit for this operation"},
    
    # Message errors
    "200": {"class": MessageError, "msg": "Send message failed"},
    "201": {"class": MessageError, "msg": "Destination number or message is empty"},
    
    # Not found errors
    "400": {"class": NotFoundError, "msg": "No delivery status available"},
    "401": {"class": NotFoundError, "msg": "No delivery status - SMS still in queue"},
    "402": {"class": NotFoundError, "msg": "No delivery status - SMS processed from queue"},
    "501": {"class": NotFoundError, "msg": "No data returned or result is empty"},
    
    # Admin errors
    "600": {"class": AdminError, "msg": "Admin level authentication failed"},
    "601": {"class": AdminError, "msg": "Inject message failed"},
    "602": {"class": AdminError, "msg": "Sender ID or message is empty"},
    "603": {"class": AdminError, "msg": "Account addition failed - missing data"},
    "604": {"class": AdminError, "msg": "Failed to add account"},
    "605": {"class": AdminError, "msg": "Account removal failed - unknown username"},
    "606": {"class": AdminError, "msg": "Failed to remove account"},
    "607": {"class": AdminError, "msg": "Set parent failed - unknown username"},
    "608": {"class": AdminError, "msg": "Failed to set parent"},
    "611": {"class": AdminError, "msg": "Account ban failed - unknown username"},
    "612": {"class": AdminError, "msg": "Failed to ban account"},
    "613": {"class": AdminError, "msg": "Account unban failed - unknown username"},
    "614": {"class": AdminError, "msg": "Failed to unban account"},
    "615": {"class": AdminError, "msg": "Editing preferences failed - missing data"},
    "616": {"class": AdminError, "msg": "Failed to edit account preferences"},
    "617": {"class": AdminError, "msg": "Editing configuration failed - missing data"},
    "618": {"class": AdminError, "msg": "Failed to edit account configuration"},
    "619": {"class": AdminError, "msg": "Viewing credit failed - missing data"},
    "620": {"class": AdminError, "msg": "Failed to view credit"},
    "621": {"class": AdminError, "msg": "Adding credit failed - missing data"},
    "622": {"class": AdminError, "msg": "Failed to add credit"},
    "623": {"class": AdminError, "msg": "Deducting credit failed - missing data"},
    "624": {"class": AdminError, "msg": "Failed to deduct credit"},
    "625": {"class": AdminError, "msg": "Setting login key failed - missing data"},
    "626": {"class": AdminError, "msg": "Failed to set login key"},
}

def handle_error(code: str, message: str = None):
    """
    Handle API error by raising appropriate exception.
    
    Args:
        code: Error code (e.g., "100")
        message: Optional custom error message
    
    Raises:
        Appropriate exception based on error code
    """
    if code in ERRORS:
        error_info = ERRORS[code]
        error_msg = message or error_info["msg"]
        raise error_info["class"](code, error_msg)
    else:
        # Unknown error - raise base exception
        raise JunubSMSError(code, message or f"Unknown error: {code}")