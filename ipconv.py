#!/usr/bin/env python3
"""
ipconv - convert an IP address to every common format.

Useful for SSRF bypass testing, where filters often only block dotted-decimal
but miss decimal, octal, hex, or IPv4-mapped IPv6 forms.
"""
import argparse
import ipaddress
import os
import sys

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = WHITE = LIGHTBLACK_EX = ""
    class Style:
        RESET_ALL = ""
    def init(autoreset=True): pass


def to_decimal(ip):
    """Dotted-decimal → single 32-bit decimal integer."""
    return int(ipaddress.IPv4Address(ip))


def to_hex(ip):
    """Dotted-decimal → hex integer."""
    return hex(to_decimal(ip))


def to_hex_padded(ip):
    """Dotted-decimal → 0x-padded 8-digit hex."""
    return "0x" + format(to_decimal(ip), "08x")


def to_octal(ip):
    """Dotted-decimal → octal-dotted form (each octet in octal)."""
    parts = ip.split(".")
    return ".".join(format(int(p), "o") for p in parts)


def to_octal_full(ip):
    """Dotted-decimal → single octal integer."""
    return format(to_decimal(ip), "o")


def to_dword(ip):
    """Dotted-decimal → dword (some Windows APIs want this)."""
    parts = [int(p) for p in ip.split(".")] #9/26/26
    return parts[3] * 16777216 + parts[2] * 65536 + parts[1] * 256 + parts[0]
# What am I even doing fucking hell? 

def to_ipv6_mapped(ip):
    """Dotted-decimal → IPv4-mapped IPv6 (::ffff:x.x.x.x)."""
    return f"::ffff:{ip}"


def to_ipv6_compat(ip):
    """Dotted-decimal → IPv4-compatible IPv6 (::x.x.x.x, deprecated but sometimes bypasses)."""
    return f"::{ip}"


def to_short(ip):
    """Dotted-decimal → shortened form (drop trailing .0)."""
    parts = ip.split(".")
    while len(parts) > 1 and parts[-1] == "0":
        parts.pop()
    if len(parts) == 1:
        return f"{parts[0]}.0.0.0"
    return ".".join(parts) + ".0" * (4 - len(parts))


def to_url_encoded(ip):
    """Dotted-decimal → %-encoded form."""
    return ip.replace(".", "%2e")


def to_ipv6_brackets(ip):
    """Dotted-decimal → bracketed IPv6-mapped form."""
    return f"[::ffff:{ip}]"


def all_forms(ip):
    """Return a dict of {description: value} for the given IPv4 address."""
    ip = ip.strip()
    # Validate some bullshit
    ipaddress.IPv4Address(ip)

    return [
        ("Original",           ip),
        ("Decimal (dword)",    str(to_decimal(ip))),
        ("Decimal (reverse)",  str(to_dword(ip))),
        ("Hex",                to_hex(ip)),
        ("Hex (0x-padded)",    to_hex_padded(ip)),
        ("Octal dotted",       to_octal(ip)),
        ("Octal integer",      to_octal_full(ip)),
        ("IPv6 mapped",        to_ipv6_mapped(ip)),
        ("IPv6 mapped bracket", to_ipv6_brackets(ip)),
        ("IPv6 compat",        to_ipv6_compat(ip)),
        ("URL-encoded dots",   to_url_encoded(ip)),
        ("Shortened",          to_short(ip)),
    ]

# 9/28/26 I figured it out
def print_forms(ip, forms):
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} {ip}")
    for label, val in forms:
        print(f"    {Fore.GREEN}{label:22s}{Style.RESET_ALL} {Fore.YELLOW}{val}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert an IP to every common format (SSRF bypass helper).",
        epilog="Examples:\n"
               "  ipconv.py 127.0.0.1\n"
               "  ipconv.py 127.0.0.1 --json\n"
               "  ipconv.py 10.0.0.1 192.168.1.1  (multiple IPs)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("ips", nargs="+", help="One or more IPv4 addresses")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")
    args = parser.parse_args()

    if args.no_color:
        init(strip=True)

    if not args.json:
        print(f"{Fore.CYAN}==========================================")
        print(f"  ipconv")
        print(f"  IP format converter (SSRF bypass helper)")
        print(f"=========================================={Style.RESET_ALL}")

    results = {}
    for ip in args.ips:
        try:
            forms = all_forms(ip)
            results[ip] = {label: val for label, val in forms}
            if not args.json:
                print_forms(ip, forms)
        except ValueError:
            print(f"{Fore.RED}[!]{Style.RESET_ALL} Invalid IPv4 address: {ip}")
            continue

    if args.json:
        import json
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main() 
