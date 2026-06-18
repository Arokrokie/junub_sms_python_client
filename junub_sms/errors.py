"""
Error codes for JunubSMS API - Super clean.
"""

class JunubSMSError(Exception):
    def __init__(self, code: str, message: str):
        self.code, self.message = code, message
        super().__init__(f"[{code}] {message}")

# Short exception classes
class AuthError(JunubSMSError): pass
class CreditError(JunubSMSError): pass
class MessageError(JunubSMSError): pass
class NotFoundError(JunubSMSError): pass
class AdminError(JunubSMSError): pass

# One dictionary with all errors
ERRORS = {
    "100": (AuthError, "Authentication failed"),
    "101": (AuthError, "Invalid operation"),
    "102": (AuthError, "Missing fields"),
    "103": (CreditError, "Insufficient credit"),
    "104": (AuthError, "Token missing"),
    "105": (AuthError, "Token disabled"),
    "106": (AuthError, "IP blocked"),
    "200": (MessageError, "Send failed"),
    "201": (MessageError, "Empty recipient/message"),
    "400": (NotFoundError, "No delivery status"),
    "401": (NotFoundError, "SMS in queue"),
    "402": (NotFoundError, "SMS processed"),
    "501": (NotFoundError, "No data"),
    "600": (AdminError, "Admin auth failed"),
    "601": (AdminError, "Inject failed"),
    "602": (AdminError, "Empty sender/message"),
    "603": (AdminError, "Missing account data"),
    "604": (AdminError, "Account add failed"),
    "605": (AdminError, "User not found"),
    "606": (AdminError, "Remove failed"),
    "607": (AdminError, "Parent not found"),
    "608": (AdminError, "Set parent failed"),
    "611": (AdminError, "Ban failed - user not found"),
    "612": (AdminError, "Ban failed"),
    "613": (AdminError, "Unban failed - user not found"),
    "614": (AdminError, "Unban failed"),
    "615": (AdminError, "Missing preferences"),
    "616": (AdminError, "Pref update failed"),
    "617": (AdminError, "Missing config"),
    "618": (AdminError, "Config update failed"),
    "619": (AdminError, "Missing credit view data"),
    "620": (AdminError, "Credit view failed"),
    "621": (AdminError, "Missing amount"),
    "622": (AdminError, "Credit add failed"),
    "623": (AdminError, "Missing amount to deduct"),
    "624": (AdminError, "Credit deduct failed"),
    "625": (AdminError, "Missing login key data"),
    "626": (AdminError, "Login key set failed"),
}

def handle_error(code: str, msg: str = None):
    """Raise the right error for any code."""
    if code in ERRORS:
        err_class, default = ERRORS[code]
        raise err_class(code, msg or default)
    raise JunubSMSError(code, msg or f"Unknown: {code}")