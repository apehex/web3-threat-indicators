"""Parse EVM bytecode and extract the key elements.

Follows the decomposition detailed in the article by OpenZeppelin:
https://blog.openzeppelin.com/deconstructing-a-solidity-contract-part-i-introduction-832efd2d7737
"""

import functools
import re

# GENERIC #####################################################################

# REGEX #######################################################################

@functools.lru_cache(maxsize=128)
def selector_regex(raw: bool=False) -> str:
    """Regex matching a function selector, in the bytecode."""
    return (
        r'63([0-9a-f]{8})14' if raw
        else r'PUSH4\s+([0-9a-f]{8})')

@functools.lru_cache(maxsize=128)
def address_regex(raw: bool=False) -> str:
    """Regex matching an address, in the bytecode."""
    return (
        r'73([0-9a-f]{40})' if raw
        else r'PUSH20\s+([0-9a-f]{40})')

@functools.lru_cache(maxsize=128)
def storage_slot_regex(raw: bool=False) -> str:
    """Regex matching a storage slot, in the bytecode."""
    return (
        r'7f([0-9a-f]{64})' if raw
        else r'PUSH32\s+([0-9a-f]{64})')

# SELECTORS ###################################################################

@functools.lru_cache(maxsize=128)
def get_function_selectors(bytecode: str, raw: bool=False) -> tuple:
    """Get all the function selectors from the hub portion of the bytecode."""
    _r = re.compile(selector_regex(raw=raw), re.IGNORECASE)
    return tuple(set(_r.findall(bytecode)))

# STORAGE #####################################################################

#TODO SLOAD could use a computed address instead of a hardcoded one => fetching only the 32 bytes words is too naive

@functools.lru_cache(maxsize=128)
def get_storage_slots(bytecode: str, raw: bool=False) -> str:
    """Get all the storage slots used in the bytecode."""
    _r = re.compile(storage_slot_regex(raw=raw), re.IGNORECASE)
    return tuple(set(_r.findall(bytecode)))
