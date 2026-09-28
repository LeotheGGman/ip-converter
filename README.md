# ipconv

Convert an IPv4 address to every common alternate representation. Built for SSRF bypass testing, where filters often block only dotted-decimal.

## Why

An SSRF filter that blocks `127.0.0.1` will happily accept `2130706433`, `0x7f000001`, `0177.0.0.1`, or `::ffff:127.0.0.1`. This tool spits out all of them for any IPv4 address.

## Install

    git clone https://github.com/LeotheGGman/ip-converter.git
    cd ip-converter
    pip install -r requirements.txt

## Usage

    # Single IP
    python3 ipconv.py 127.0.0.1

    # Multiple IPs
    python3 ipconv.py 127.0.0.1 10.0.0.1 169.254.169.254

    # JSON output (for piping)
    python3 ipconv.py 127.0.0.1 --json

## Example output

    [*] 127.0.0.1
        Original               127.0.0.1
        Decimal (dword)        2130706433
        Hex                    0x7f000001
        Octal dotted           177.0.0.1
        Octal integer          17700000001
        IPv6 mapped            ::ffff:127.0.0.1
        IPv6 compat            ::127.0.0.1
        URL-encoded dots       127%2e0%2e0%2e1
        Shortened              127.0.0.1

## Supported formats

- Dotted-decimal (original)
- Decimal / dword (single integer)
- Reverse dword
- Hex (`0x...`)
- Hex padded (`0x00000000`)
- Octal dotted (`0177.0.0.1`)
- Octal integer
- IPv4-mapped IPv6 (`::ffff:x.x.x.x`)
- IPv4-compatible IPv6 (`::x.x.x.x`)
- Bracketed IPv6
- URL-encoded dots (`%2e`)
- Shortened (dropped trailing `.0`)

## Tests

    pytest tests/ -v

## Disclaimer

For authorized security testing only.

## License

MIT
