import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ipconv import (
    to_decimal, to_hex, to_hex_padded, to_octal, to_octal_full,
    to_ipv6_mapped, to_url_encoded, all_forms
)


def test_localhost_decimal():
    assert to_decimal("127.0.0.1") == 2130706433


def test_localhost_hex():
    assert to_hex("127.0.0.1") == "0x7f000001"


def test_localhost_hex_padded():
    assert to_hex_padded("127.0.0.1") == "0x7f000001"


def test_octal_dotted():
    assert to_octal("127.0.0.1") == "177.0.0.1"


def test_octal_integer():
    assert to_octal_full("127.0.0.1") == "17700000001"


def test_ipv6_mapped():
    assert to_ipv6_mapped("127.0.0.1") == "::ffff:127.0.0.1"


def test_url_encoded():
    assert to_url_encoded("127.0.0.1") == "127%2e0%2e0%2e1"


def test_all_forms_returns_list():
    forms = all_forms("10.0.0.1")
    assert isinstance(forms, list)
    assert len(forms) >= 10


def test_invalid_ip_raises():
    import pytest
    with pytest.raises(ValueError):
        all_forms("999.999.999.999")
