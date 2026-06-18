"""
Error codes for JunubSMS API - Matching official documentation exactly.
"""

class JunubSMSError(Exception):
    def __init__(self, code: str, message: str):
        self.code, self.message = code, message
        super().__init__(f"[{code}] {message}")

# Specific exception classes
class AuthError(JunubSMSError): pass
class CreditError(JunubSMSError): pass
class MessageError(JunubSMSError): pass
class NotFoundError(JunubSMSError): pass
class AdminError(JunubSMSError): pass

# ALL error codes with EXACT messages from documentation
ERRORS = {
    # Authentication Errors (100-106)
    "100": (AuthError, "authentication failed"),
    "101": (AuthError, "type of action is invalid or unknown"),
    "102": (AuthError, "one or more field empty"),
    "103": (CreditError, "not enough credit for this operation"),
    "104": (AuthError, "webservice token is not available"),
    "105": (AuthError, "webservice token not enable for this user"),
    "106": (AuthError, "webservice token not allowed from this IP address"),
    
    # Message Errors (200-201)
    "200": (MessageError, "send message failed"),
    "201": (MessageError, "destination number or message is empty"),
    
    # Delivery Status Errors (400-402)
    "400": (NotFoundError, "no delivery status available"),
    "401": (NotFoundError, "no delivery status retrieved and SMS still in queue"),
    "402": (NotFoundError, "no delivery status retrieved and SMS has been processed from queue"),
    
    # Not Found
    "501": (NotFoundError, "no data returned or result is empty"),
    
    # Admin Errors (600-626)
    "600": (AdminError, "admin level authentication failed"),
    "601": (AdminError, "inject message failed"),
    "602": (AdminError, "sender id or message is empty"),
    "603": (AdminError, "account addition failed due to missing data"),
    "604": (AdminError, "fail to add account"),
    "605": (AdminError, "account removal failed due to unknown username"),
    "606": (AdminError, "fail to remove account"),
    "607": (AdminError, "set parent failed due to unknown username"),
    "608": (AdminError, "fail to set parent"),
    "609": (AdminError, "get parent failed due to unknown username"),
    "610": (AdminError, "fail to get parent"),
    "611": (AdminError, "account ban failed due to unknown username"),
    "612": (AdminError, "fail to ban account"),
    "613": (AdminError, "account unban failed due to unknown username"),
    "614": (AdminError, "fail to unban account"),
    "615": (AdminError, "editing account preferences failed due to missing data"),
    "616": (AdminError, "fail to edit account preferences"),
    "617": (AdminError, "editing account configuration failed due to missing data"),
    "618": (AdminError, "fail to edit account configuration"),
    "619": (AdminError, "viewing credit failed due to missing data"),
    "620": (AdminError, "fail to view credit"),
    "621": (AdminError, "adding credit failed due to missing data"),
    "622": (AdminError, "fail to add credit"),
    "623": (AdminError, "deducting credit failed due to missing data"),
    "624": (AdminError, "fail to deduct credit"),
    "625": (AdminError, "setting login key failed due to missing data"),
    "626": (AdminError, "fail to set login key"),
}

def handle_error(code: str, msg: str = None):
    """Raise the right error for any code."""
    if code in ERRORS:
        err_class, default = ERRORS[code]
        raise err_class(code, msg or default)
    # Fallback for unknown errors - matches test expectation
    raise JunubSMSError(code, msg or f"Unknown error: {code}")