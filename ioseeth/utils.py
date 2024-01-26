"""Various utility functions."""

import os.path
import collections.abc
import typing

import eth_utils.crypto

import toolblocks.parsing.common

# DATA ########################################################################

def get_data_dir_path() -> str:
    """Returns the path to the directory containing the data files."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/')

# COVERAGE ####################################################################

def coverage(left: collections.abc.Iterable, right: collections.abc.Iterable) -> float:
    """Calculate the ratio of the right iterable covered by the left one."""
    __left = set(left)
    __right = set(right)
    return (
        1. if not __right
        else sum(__e in __right for __e in __left) / len(__right))

# CRYPTO ######################################################################

def keccak(primitive: typing.Union[bytes, int, bool]=None, hexstr: str=None, text: str=None) -> str:
    """Compute the Keccak 256 hash of any data, encoded as a HEX string."""
    return toolblocks.parsing.common.to_hexstr(eth_utils.crypto.keccak(primitive=primitive, hexstr=hexstr, text=text), prefix=False) # lowercase, without prefix
