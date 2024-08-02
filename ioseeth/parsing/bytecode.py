"""Parse EVM bytecode and extract the key elements.

Follows the decomposition detailed in the article by OpenZeppelin:
https://blog.openzeppelin.com/deconstructing-a-solidity-contract-part-i-introduction-832efd2d7737
"""

import re

import toolblocks.parsing.common

# OPCODES #####################################################################

STOP = 0x00
EQ = 0x14
EXTCODECOPY = 0x3C
BLOCKHASH = 0x40
COINBASE = 0x41
PREVRANDAO = 0x44
JUMPDEST = 0x5B
PUSH0 = 0x5F
PUSH32 = 0x7F
CREATE = 0xF0
CALLCODE = 0xF2
RETURN = 0xF3
DELEGATECALL = 0xF4
CREATE2 = 0xF5
REVERT = 0xFD
INVALID = 0xFE
SELFDESTRUCT = 0xFF

HALTING = [STOP, RETURN, REVERT, INVALID, SELFDESTRUCT]

is_halting = lambda opcode: opcode in HALTING
is_push = lambda opcode: opcode >= PUSH0 and opcode <= PUSH32

# REGEX #######################################################################

def selector_regex(raw: bool=False) -> str:
    """Regex matching a function selector, in the bytecode."""
    return (
        r'63([0-9a-f]{8})14' if raw
        else r'PUSH4\s+([0-9a-f]{8})')

def address_regex(raw: bool=False) -> str:
    """Regex matching an address, in the bytecode."""
    return (
        r'73([0-9a-f]{40})' if raw
        else r'PUSH20\s+([0-9a-f]{40})')

def storage_slot_regex(raw: bool=False) -> str:
    """Regex matching a storage slot, in the bytecode."""
    return (
        r'7f([0-9a-f]{64})' if raw
        else r'PUSH32\s+([0-9a-f]{64})')

def creation_regex() -> str:
    """Regex matching the end of the creation bytecode, when it returns the runtime bytecode."""
    return r'(f3(?:00|fe)?)(6080)'

def metadata_regex() -> str:
    """Regex matching the metadata appended to the bytecode."""
    return r'(a264697066735822[0-9a-f]{68}64736f6c6343[0-9a-f]{6}0033)'

# CREATION ####################################################################

def split_creation(bytecode: str) -> list:
    """Split the creation and runtime code from the creation data."""
    __parts = re.split(pattern=creation_regex(), string=bytecode, flags=re.IGNORECASE)
    return (''.join(__parts[:2]), ''.join(__parts[2:]))

# METADATA ####################################################################

def split_metadata(bytecode: str) -> list:
    """Split the metadata from the bytecode, returning both."""
    return re.split(pattern=metadata_regex(), string=bytecode, flags=re.IGNORECASE)

# PARSE CREATION DATA #########################################################

#TODO recursive parsing in case several contracts are deployed
# 0xb61e1747cb5b2b9ff4a5dd18e625c1b5547a655d4d5136505e7cabd5e5299e93

def parse_creation_data(data: str) -> tuple:
    """Split the creation data into 4 parts: creation bytecode + runtime bytecode + metadata + creation args."""
    __creation = __runtime = __metadata = __args = ''
    __rest = data
    # extract the creation code
    __parts = split_creation(bytecode=data)
    if len(__parts) > 1 and __parts[1]:
        __creation = __parts[0]
        __rest = __parts[1]
    # parse the runtime, metadata and args from the rest of the creation data
    __parts = split_metadata(bytecode=__rest)
    if __parts:
        __runtime = __parts[0]
    if len(__parts) > 1:
        __metadata = __parts[1]
    if len(__parts) > 2:
        __args = __parts[2]
    return (
        toolblocks.parsing.common.to_hexstr(__creation),
        toolblocks.parsing.common.to_hexstr(__runtime),
        toolblocks.parsing.common.to_hexstr(__metadata),
        toolblocks.parsing.common.to_hexstr(__args))

# INSTRUCTIONS ################################################################

def instruction_length(opcode: int) -> int:
    return 1 + is_push(opcode) * (opcode - PUSH0) # 1 byte for the opcode + n bytes of data

def iterate_over_instructions(bytecode: str) -> iter:
    """Split the bytecode into raw instructions and returns an iterator."""
    __bytes = toolblocks.parsing.common.to_bytes(bytecode)
    __i = 0
    while __i < len(__bytes):
        __len = instruction_length(opcode=__bytes[__i])
        yield __bytes[__i:__i+__len]
        __i = __i + __len

def bytecode_has_specific_opcode(bytecode: str, opcode: int) -> bool:
    """Check if the runtime code contains a specific opcode."""
    __instructions = iterate_over_instructions(bytecode=bytecode)
    __halted = False

    for __i in __instructions:
        __oc = __i[0] # the opcode at the start of the instruction
        if __oc == opcode and not __halted:
            return True
        elif __oc == JUMPDEST:
            __halted = False
        elif is_halting(__oc):
            __halted = True

    return False

def bytecode_has_specific_opcodes(bytecode: str, opcodes: tuple, check: callable=any) -> bool:
    """Check if the runtime code contains any/all of the specified opcodes."""
    return check(bytecode_has_specific_opcode(bytecode=bytecode, opcode=__o) for __o in opcodes)

# SELECTORS ###################################################################

def get_function_selectors(bytecode: str, raw: bool=True) -> tuple:
    """Get all the function selectors from the hub portion of the bytecode."""
    _r = re.compile(selector_regex(raw=raw), flags=re.IGNORECASE)
    return tuple(set(_r.findall(bytecode)))

# STORAGE #####################################################################

#TODO SLOAD could use a computed address instead of a hardcoded one => fetching only the 32 bytes words is too naive

def get_storage_slots(bytecode: str, raw: bool=True) -> str:
    """Get all the storage slots used in the bytecode."""
    _r = re.compile(storage_slot_regex(raw=raw), flags=re.IGNORECASE)
    return tuple(set(_r.findall(bytecode)))
