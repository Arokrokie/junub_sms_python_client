"""
Tests for JunubSMS client - Ultra minimal.
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
    if responses is None:
        responses = [{"token": "test_token"}]
    mock_call.side_effect = responses
    return JunubSMS("test", "pass")


# ============================================================
# TESTS
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


def test_send_sms():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": [{"id": "12345"}]}
        ]
        client = JunubSMS("test", "pass")
        result = client.send("123", "Hello")
        assert result[0]["id"] == "12345"


def test_send_sms_multiple():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": [{"id": "1"}, {"id": "2"}]}
        ]
        client = JunubSMS("test", "pass")
        assert len(client.send(["1", "2"], "Hello")) == 2


def test_get_credit():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": {"balance": "100.50"}}
        ]
        client = JunubSMS("test", "pass")
        assert client.get_credit()["balance"] == "100.50"


def test_get_incoming():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": [{"msg": "Hello"}]}
        ]
        client = JunubSMS("test", "pass")
        assert client.get_incoming()[0]["msg"] == "Hello"


def test_get_outgoing_status():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": [{"status": "delivered"}]}
        ]
        client = JunubSMS("test", "pass")
        assert client.get_outgoing_status()[0]["status"] == "delivered"


def test_get_inbox():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": [{"id": "1"}]}
        ]
        client = JunubSMS("test", "pass")
        assert len(client.get_inbox()) == 1


def test_get_sandbox():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": [{"id": "1"}]}
        ]
        client = JunubSMS("test", "pass")
        assert len(client.get_sandbox()) == 1


def test_get_contacts():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": [{"p_desc": "John"}, {"p_desc": "Jane"}]}
        ]
        client = JunubSMS("test", "pass")
        contacts = client.get_contacts("john")
        assert len(contacts) == 2 and contacts[0]["p_desc"] == "John"


def test_get_groups():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"data": [{"code": "G1"}, {"code": "G2"}]}
        ]
        client = JunubSMS("test", "pass")
        groups = client.get_groups()
        assert len(groups) == 2 and groups[0]["code"] == "G1"


def test_admin_inject():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"status": "OK"}
        ]
        client = JunubSMS("test", "pass")
        assert client.inject_message("S", "M", "123", "S")["status"] == "OK"


def test_query():
    with patch('junub_sms.client.JunubSMS._call') as mock:
        mock.side_effect = [
            {"token": "test_token"},
            {"username": "test"}
        ]
        client = JunubSMS("test", "pass")
        assert client.query("user")["username"] == "test"


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
# ERROR TESTS - All in One!
# ============================================================

@pytest.mark.parametrize("code,msg,expected", [
    ("200", "Send failed", MessageError),
    ("103", "No credit", CreditError),
    ("100", "Auth failed", AuthError),
    ("600", "Admin denied", AdminError),
    ("501", "Not found", NotFoundError),
    ("999", "Unknown", JunubSMSError),
])
def test_errors(code, msg, expected):
    with pytest.raises(expected) as e:
        handle_error(code, msg)
    assert code in str(e.value)


# ============================================================
# HTTP ERROR TESTS - All in One!
# ============================================================

@pytest.mark.parametrize("code,msg,expected", [
    ("200", "Send failed", MessageError),
    ("103", "No credit", CreditError),
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
        r.json = Mock(return_value={"ERR": "200", "DESC": "Send failed"})
        mock.return_value = r
        with patch('junub_sms.client.JunubSMS._authenticate'):
            c = JunubSMS("test", "pass")
            c.token = "test_token"
            with pytest.raises(MessageError) as e:
                c._call({"op": "pv", "to": "123", "msg": "test"})
            assert "200" in str(e.value)