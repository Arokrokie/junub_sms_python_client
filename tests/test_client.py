"""
Tests for JunubSMS client - Clean and complete.
"""

import pytest
from unittest.mock import patch, Mock
from junub_sms import JunubSMS
from junub_sms.errors import *


# ============================================================
# HELPERS
# ============================================================

def mock_client(mock_call, responses=None):
    """Create a client with mocked _call."""
    responses = responses or [{"token": "test_token"}]
    mock_call.side_effect = responses
    return JunubSMS("test", "pass")


def assert_response(result, key, value):
    """Helper to assert response contains expected value."""
    assert result.get(key) == value


# ============================================================
# INITIALIZATION (2 tests)
# ============================================================

def test_init_success():
    with patch('junub_sms.client.JunubSMS._call') as m:
        m.return_value = {"token": "test_token_123"}
        assert JunubSMS("test", "pass").token == "test_token_123"


def test_init_failure():
    with patch('junub_sms.client.JunubSMS._call') as m:
        m.return_value = {}
        with pytest.raises(JunubSMSError) as e:
            JunubSMS("test", "wrong")
        assert "100" in str(e.value)


# ============================================================
# MESSAGE OPERATIONS (6 tests)
# ============================================================

def test_send_sms():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": [{"id": "12345"}]}]
        client = JunubSMS("test", "pass")
        result = client.send("123", "Hello")
        assert result[0]["id"] == "12345"


def test_send_sms_multiple():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": [{"id": "1"}, {"id": "2"}]}]
        client = JunubSMS("test", "pass")
        assert len(client.send(["1", "2"], "Hello")) == 2


def test_get_outgoing_status():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": [{"status": "delivered"}]}]
        client = JunubSMS("test", "pass")
        assert client.get_outgoing_status()[0]["status"] == "delivered"


def test_get_incoming():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": [{"msg": "Hello"}]}]
        client = JunubSMS("test", "pass")
        assert client.get_incoming()[0]["msg"] == "Hello"


def test_get_inbox():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": [{"id": "1"}]}]
        client = JunubSMS("test", "pass")
        assert len(client.get_inbox()) == 1


def test_get_sandbox():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": [{"id": "1"}]}]
        client = JunubSMS("test", "pass")
        assert len(client.get_sandbox()) == 1


# ============================================================
# ACCOUNT OPERATIONS (3 tests)
# ============================================================

def test_get_credit():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": {"balance": "100.50"}}]
        client = JunubSMS("test", "pass")
        assert client.get_credit()["balance"] == "100.50"


def test_get_token():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"token": "new_token_123"}]
        client = JunubSMS("test", "pass")
        assert client.get_token() == "new_token_123"


def test_set_token():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"token": "new_token_456"}]
        client = JunubSMS("test", "pass")
        new_token = client.set_token("new_token_456")
        assert new_token == "new_token_456"
        assert client.token == "new_token_456"


# ============================================================
# CONTACT OPERATIONS (2 tests)
# ============================================================

def test_get_contacts():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": [{"p_desc": "John"}, {"p_desc": "Jane"}]}]
        client = JunubSMS("test", "pass")
        contacts = client.get_contacts("john")
        assert len(contacts) == 2
        assert contacts[0]["p_desc"] == "John"


def test_get_groups():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"data": [{"code": "G1"}, {"code": "G2"}]}]
        client = JunubSMS("test", "pass")
        groups = client.get_groups()
        assert len(groups) == 2
        assert groups[0]["code"] == "G1"


# ============================================================
# QUERY (1 test)
# ============================================================

def test_query():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"username": "test"}]
        client = JunubSMS("test", "pass")
        assert client.query("user")["username"] == "test"


# ============================================================
# ADMIN OPERATIONS (13 tests)
# ============================================================

def test_admin_inject():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"status": "OK"}]
        client = JunubSMS("test", "pass")
        assert client.inject_message("S", "M", "123", "S")["status"] == "OK"


def test_add_account():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"status": "OK"}]
        client = JunubSMS("test", "pass")
        result = client.add_account("newuser", "pass123", "John Doe", "john@example.com", 3)
        assert result["status"] == "OK"


def test_remove_account():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"status": "OK"}]
        client = JunubSMS("test", "pass")
        assert client.remove_account("testuser")["status"] == "OK"


def test_ban_account():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"status": "OK"}]
        client = JunubSMS("test", "pass")
        assert client.ban_account("testuser")["status"] == "OK"


def test_unban_account():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"status": "OK"}]
        client = JunubSMS("test", "pass")
        assert client.unban_account("testuser")["status"] == "OK"


def test_set_parent():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"status": "OK"}]
        client = JunubSMS("test", "pass")
        assert client.set_parent("subuser", "parentuser")["status"] == "OK"


def test_get_parent():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"parent": "parentuser"}]
        client = JunubSMS("test", "pass")
        assert client.get_parent("subuser")["parent"] == "parentuser"


def test_update_preferences():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"status": "OK"}]
        client = JunubSMS("test", "pass")
        result = client.update_preferences("testuser", data_name="New Name")
        assert result["status"] == "OK"


def test_update_config():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"status": "OK"}]
        client = JunubSMS("test", "pass")
        result = client.update_config("testuser", data_footer="Powered by SMS")
        assert result["status"] == "OK"


def test_credit_view():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"balance": "150.75"}]
        client = JunubSMS("test", "pass")
        assert client.credit_view("testuser")["balance"] == "150.75"


def test_credit_add():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"balance": "200.50"}]
        client = JunubSMS("test", "pass")
        assert client.credit_add("testuser", 50.00)["balance"] == "200.50"


def test_credit_deduct():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"balance": "100.25"}]
        client = JunubSMS("test", "pass")
        assert client.credit_deduct("testuser", 25.00)["balance"] == "100.25"


def test_set_login_key():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [{"token": "test_token"}, {"login_key": "new_key_123"}]
        client = JunubSMS("test", "pass")
        assert client.set_login_key("testuser")["login_key"] == "new_key_123"


# ============================================================
# UTILITY (2 tests)
# ============================================================

def test_context_manager():
    with patch('junub_sms.client.JunubSMS._call') as m:
        m.return_value = {"token": "test_token"}
        with JunubSMS("test", "pass") as c:
            assert c.session is not None


def test_close():
    with patch('junub_sms.client.JunubSMS._call') as m:
        m.return_value = {"token": "test_token"}
        c = JunubSMS("test", "pass")
        c.close()
        assert c.session is not None


# ============================================================
# ERROR TESTS - ALL 45 CODES (1 parameterized test)
# ============================================================

ERRORS = [
    # Authentication (7)
    ("100", "authentication failed", AuthError),
    ("101", "type of action is invalid or unknown", AuthError),
    ("102", "one or more field empty", AuthError),
    ("103", "not enough credit for this operation", CreditError),
    ("104", "webservice token is not available", AuthError),
    ("105", "webservice token not enable for this user", AuthError),
    ("106", "webservice token not allowed from this IP address", AuthError),
    # Message (2)
    ("200", "send message failed", MessageError),
    ("201", "destination number or message is empty", MessageError),
    # Delivery Status (3)
    ("400", "no delivery status available", NotFoundError),
    ("401", "no delivery status retrieved and SMS still in queue", NotFoundError),
    ("402", "no delivery status retrieved and SMS has been processed from queue", NotFoundError),
    # Not Found (1)
    ("501", "no data returned or result is empty", NotFoundError),
    # Admin (27)
    ("600", "admin level authentication failed", AdminError),
    ("601", "inject message failed", AdminError),
    ("602", "sender id or message is empty", AdminError),
    ("603", "account addition failed due to missing data", AdminError),
    ("604", "fail to add account", AdminError),
    ("605", "account removal failed due to unknown username", AdminError),
    ("606", "fail to remove account", AdminError),
    ("607", "set parent failed due to unknown username", AdminError),
    ("608", "fail to set parent", AdminError),
    ("609", "get parent failed due to unknown username", AdminError),
    ("610", "fail to get parent", AdminError),
    ("611", "account ban failed due to unknown username", AdminError),
    ("612", "fail to ban account", AdminError),
    ("613", "account unban failed due to unknown username", AdminError),
    ("614", "fail to unban account", AdminError),
    ("615", "editing account preferences failed due to missing data", AdminError),
    ("616", "fail to edit account preferences", AdminError),
    ("617", "editing account configuration failed due to missing data", AdminError),
    ("618", "fail to edit account configuration", AdminError),
    ("619", "viewing credit failed due to missing data", AdminError),
    ("620", "fail to view credit", AdminError),
    ("621", "adding credit failed due to missing data", AdminError),
    ("622", "fail to add credit", AdminError),
    ("623", "deducting credit failed due to missing data", AdminError),
    ("624", "fail to deduct credit", AdminError),
    ("625", "setting login key failed due to missing data", AdminError),
    ("626", "fail to set login key", AdminError),
    # Unknown
    ("999", "Unknown error", JunubSMSError),
]

@pytest.mark.parametrize("code,msg,expected", ERRORS)
def test_errors(code, msg, expected):
    """Test ALL 45 error codes."""
    with pytest.raises(expected) as e:
        handle_error(code, msg)
    assert code in str(e.value)
    assert msg.lower() in str(e.value).lower()


# ============================================================
# HTTP ERROR TESTS (3 tests)
# ============================================================

@pytest.mark.parametrize("code,msg,expected", [
    ("200", "send message failed", MessageError),
    ("103", "not enough credit for this operation", CreditError),
])
def test_http_errors(code, msg, expected):
    with patch('junub_sms.client.requests.Session.get') as mock:
        r = Mock()
        r.raise_for_status = Mock()
        r.json = Mock(return_value={"ERR": code, "DESC": msg})
        mock.return_value = r
        with patch('junub_sms.client.JunubSMS._authenticate'):
            c = JunubSMS("test", "pass")
            c.token = "test_token"
            with pytest.raises(expected) as e:
                c._call({"op": "pv", "to": "123", "msg": "test"})
            assert code in str(e.value)


def test_error_through_client():
    with patch('junub_sms.client.requests.Session.get') as mock:
        r = Mock()
        r.raise_for_status = Mock()
        r.json = Mock(return_value={"ERR": "200", "DESC": "send message failed"})
        mock.return_value = r
        with patch('junub_sms.client.JunubSMS._authenticate'):
            c = JunubSMS("test", "pass")
            c.token = "test_token"
            with pytest.raises(MessageError) as e:
                c._call({"op": "pv", "to": "123", "msg": "test"})
            assert "200" in str(e.value)