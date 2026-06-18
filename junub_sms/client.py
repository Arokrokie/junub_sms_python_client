"""
JunubSMS API Client - Clean and minimal.
"""

import requests
from typing import Dict, Any, Union, List, Optional
from .errors import handle_error, JunubSMSError


class JunubSMS:
    """JunubSMS API Client."""
    
    BASE_URL = "https://sms.junubsms.com/index.php"
    
    def __init__(self, username: str, password: str):
        self.username, self.password = username, password
        self.token = None
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "junub-sms-python/1.0.0"})
        self._authenticate()
    
    def _authenticate(self):
        """Get webservices token."""
        resp = self._call({"op": "get_token", "u": self.username, "p": self.password})
        if "token" in resp:
            self.token = resp["token"]
        else:
            raise JunubSMSError("100", "Failed to get authentication token")
    
    def _call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API call with error handling."""
        if self.token and params.get("op") not in ["get_token", "set_token"]:
            params["h"] = self.token
        params.setdefault("format", "json")
        
        try:
            resp = self.session.get(self.BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            if isinstance(data, dict):
                if "ERR" in data:
                    handle_error(data["ERR"], data.get("DESC", f"Error {data['ERR']}"))
                return data.get("data", data) if data.get("status") == "OK" or data.get("error") == "0" else data
            return data
        except requests.exceptions.RequestException as e:
            raise JunubSMSError("999", f"Request failed: {e}")
    
    def _build_params(self, op: str, **kwargs) -> Dict:
        """Build parameters for API calls."""
        return {"op": op, **{k: v for k, v in kwargs.items() if v is not None}}
    
    def _get(self, op: str, **kwargs):
        """Generic GET operation."""
        return self._call(self._build_params(op, **kwargs))
    
    def _get_data(self, op: str, **kwargs):
        """GET operation returning data list."""
        return self._get(op, **kwargs).get("data", [])
    
    # ============================================================
    # MESSAGES
    # ============================================================
    
    def send(self, to: Union[str, List[str]], msg: str, sender: str = None,
             msg_type: str = "0", unicode: bool = False, schedule: str = None):
        """Send SMS message(s)."""
        params = {"op": "pv", "to": to if isinstance(to, str) else ",".join(to), "msg": msg, "type": msg_type}
        if sender: params["from"] = sender
        if unicode: params["unicode"] = "1"
        if schedule: params["schedule"] = schedule
        
        resp = self._call(params)
        return resp.get("data", [{"id": resp.get("id"), "to": to}]) if "data" in resp else [resp] if "id" in resp else [resp]
    
    def get_outgoing_status(self, **kwargs):
        """Get outgoing SMS and delivery status."""
        return self._get_data("ds", **kwargs)
    
    def get_incoming(self, **kwargs):
        """Get incoming SMS."""
        return self._get_data("in", **kwargs)
    
    def get_inbox(self, **kwargs):
        """Get inbox messages."""
        return self._get_data("ix", **kwargs)
    
    def get_sandbox(self, **kwargs):
        """Get sandbox messages."""
        return self._get_data("sx", **kwargs)
    
    # ============================================================
    # ACCOUNT
    # ============================================================
    
    def get_credit(self):
        """Get user credit information."""
        return self._get("cr").get("data", {})
    
    def get_token(self):
        """Get webservices token."""
        return self._get("get_token", u=self.username, p=self.password).get("token", "")
    
    def set_token(self, new_token: str):
        """Set webservices token."""
        self.token = new_token
        return self._get("set_token", u=self.username, h=new_token).get("token", new_token)
    
    def query(self, info_type: str = "user"):
        """Query server for information."""
        return self._get("query", type=info_type)
    
    # ============================================================
    # CONTACTS
    # ============================================================
    
    def get_contacts(self, keyword: str, limit: int = 100):
        """Get contact list by keyword."""
        return self._get_data("get_contact", kwd=keyword, c=limit)
    
    def get_groups(self, keyword: str = "", limit: int = 100):
        """Get group contact list by name or code."""
        return self._get_data("get_contact_group", kwd=keyword, c=limit)
    
    # ============================================================
    # ADMIN
    # ============================================================
    
    def inject_message(self, sender: str, msg: str, recipient: str, smsc: str):
        """Inject message into system (admin)."""
        return self._get("inject", from_=sender, msg=msg, recvnum=recipient, smsc=smsc)
    
    def add_account(self, username: str, password: str, name: str, email: str,
                   status: int = 3, parent: str = None, mobile: str = None):
        """Add account (admin)."""
        return self._get("accountadd", data_username=username, data_password=password,
                        data_name=name, data_email=email, data_status=status,
                        data_parent=parent, data_mobile=mobile)
    
    def remove_account(self, username: str):
        return self._get("accountremove", data_username=username)
    
    def ban_account(self, username: str):
        return self._get("accountban", data_username=username)
    
    def unban_account(self, username: str):
        return self._get("accountunban", data_username=username)
    
    def credit_view(self, username: str):
        return self._get("creditview", data_username=username)
    
    def credit_add(self, username: str, amount: float):
        return self._get("creditadd", data_username=username, data_amount=amount)
    
    def credit_deduct(self, username: str, amount: float):
        return self._get("creditdeduct", data_username=username, data_amount=amount)
    
    def set_parent(self, username: str, parent: str):
        return self._get("parentset", data_username=username, data_parent=parent)
    
    def get_parent(self, username: str):
        return self._get("parentget", data_username=username)
    
    def set_login_key(self, username: str):
        return self._get("loginkeyset", data_username=username)
    
    def update_preferences(self, username: str, **kwargs):
        return self._get("accountpref", data_username=username, **kwargs)
    
    def update_config(self, username: str, **kwargs):
        return self._get("accountconf", data_username=username, **kwargs)
    
    # ============================================================
    # UTILITY
    # ============================================================
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()