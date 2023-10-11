"""Parse EVM bytecode and extract the key elements.

Follows the decomposition detailed in the article by OpenZeppelin:
https://blog.openzeppelin.com/deconstructing-a-solidity-contract-part-i-introduction-832efd2d7737
"""

import functools
import re

# GENERIC #####################################################################

@functools.lru_cache(maxsize=128)
def is_raw_hex(bytecode: str) -> bool:
    """Check whether the bytecode is a raw hexadecimal string or a sequence of opcodes."""
    return not (
        isinstance(bytecode, list)
        or isinstance(bytecoden, tuple)
        or (isinstance(bytecode, str) and ' ' in bytecode))

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

@functools.lru_cache(maxsize=128)
def metadata_regex() -> str:
    """Regex matching the metadata appended to the bytecode."""
    return r'(a264697066735822[0-9a-f]{68}64736f6c6343[0-9a-f]{6}0033)'

# METADATA ####################################################################

@functools.lru_cache(maxsize=128)
def split_metadata(bytecode: str) -> list:
    """Split the metadata from the bytecode, returning both."""
    return re.split(pattern=metadata_regex(), string=bytecode)

# NORMALIZE ###################################################################

@functools.lru_cache(maxsize=128)
def normalize(bytecode: str) -> str:
    """Format the hex bytecode in a known and consistent way.
    Remove both the prefix "0x" and the metadata suffix."""
    __split = split_metadata(bytecode=bytecode)
    return __split[0].lower().replace('0x', '')

# OPCODES #####################################################################

STOP = 0x00
COINBASE = 0x41
JUMPDEST = 0x5B
PUSH1 = 0x60
PUSH32 = 0x7F
RETURN = 0xF3
REVERT = 0xFD
INVALID = 0xFE
SELFDESTRUCT = 0xFF
CREATE2 = 0xF5
DELEGATECALL = 0xF4

HALTING = [STOP, RETURN, REVERT, INVALID, SELFDESTRUCT]

is_halting = lambda opcode: opcode in HALTING
is_push = lambda opcode: opcode >= PUSH1 and opcode <= PUSH32

@functools.lru_cache(maxsize=128)
def bytecode_has_specific_opcode(bytecode: str, opcode: int) -> bool:
    """Check if the runtime code contains a specific opcode."""
    __bytes = bytes.fromhex(normalize(bytecode))
    __halted = False
    __skip = 0

    for __oc in __bytes:
        if __skip > 0: # skip the data bytes
            __skip -= 1
            continue
        else:
            if __oc == opcode and not __halted:
                return True
            elif __oc == JUMPDEST:
                __halted = False
            elif is_halting(__oc):
                __halted = True
            elif is_push(__oc):
                __skip = __oc - PUSH1 + 1 # length of data

    return False

@functools.lru_cache(maxsize=128)
def bytecode_has_specific_opcodes(bytecode: str, opcodes: int, check: callable=any) -> bool:
    """Check if the runtime code contains any/all of the specified opcodes."""
    return check(bytecode_has_specific_opcode(bytecode=bytecode, opcode=__o) for __o in opcodes)

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
