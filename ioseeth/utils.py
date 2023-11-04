"""Various utility functions."""

import os.path

import eth_utils.crypto

# DATA ########################################################################

def get_data_dir_path() -> str:
    """Returns the path to the directory containing the data files."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/')

# CONVERSIONS #################################################################

def is_raw_hex(data: str) -> bool:
    """Check whether the data is a raw hexadecimal string."""
    try:
        int(data, 16)
        return True
    except Exception:
        return False

def normalize_hexstr(data: str) -> str:
    """Format the hex data in a known and consistent way."""
    return (
        ((len(data) % 2) * '0') # pad so that the length is pair => full bytes
        + data.lower().replace('0x', ''))

def to_hexstr(data: any) -> str:
    """Format any data as a HEX string."""
    __data = ''
    if isinstance(data, str):
        __data = data if is_raw_hex(data=data) else data.encode('utf-8').hex()
    if isinstance(data, bytes):
        __data = data.hex()
    if isinstance(data, int):
        __data = hex(data)
    return normalize_hexstr(__data)

def to_bytes(data: any) -> bytes:
    """Format any data as a bytes array."""
    return bytes.fromhex(to_hexstr(data))

# COVERAGE ####################################################################

def coverage(left: iter, right: iter) -> float:
    """Calculate the ratio of the right iterable covered by the left one."""
    __left = set(left)
    __right = set(right)
    return (sum(__e in __right for __e in __left) / len(__right))

# CRYPTO ######################################################################

def keccak(primitive: bytes=None, hexstr: str=None, text: str=None) -> str:
    """Compute the Keccak 256 hash of any data, encoded as a HEX string."""
    return to_hexstr(eth_utils.crypto.keccak(primitive=primitive, hexstr=hexstr, text=text)) # lowercase, without prefix
