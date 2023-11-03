"""Various utility functions."""

import os.path

import eth_utils.crypto

# DATA ########################################################################

def get_data_dir_path() -> str:
    """Returns the path to the directory containing the data files."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/')

# COVERAGE ####################################################################

def coverage(left: iter, right: iter) -> float:
    """Calculate the ratio of the right iterable covered by the left one."""
    __left = set(left)
    __right = set(right)
    return (sum(__e in __right for __e in __left) / len(__right))

# CRYPTO ######################################################################

def keccak(primitive: bytes=None, hexstr: str=None, text: str=None) -> str:
    """Compute the Keccak 256 hash of any data, encoded as a HEX string."""
    return eth_utils.crypto.keccak(primitive=primitive, hexstr=hexstr, text=text).hex().lower() # lowercase, without prefix
