"""Indicators on anti-debugging techniques."""

import re

import ioseeth.parsing.bytecode

# REGEX #######################################################################

def cast_to_address_regex() -> str:
    """Regex matching a cast to the address type."""
    return r'73ffffffffffffffffffffffffffffffffffffffff16'

def null_value_regex() -> str:
    """Regex matching a null value: PUSH 0 then optionally DUP."""
    return r'(?:6000|5f)(?:8[01234])?'

def null_address_regex() -> str:
    """Regex matching a null address, in the bytecode."""
    return null_value_regex() + cast_to_address_regex()

def coinbase_address_regex() -> str:
    """Regex matching a coinbase cast to address, in the bytecode."""
    return r'41' + cast_to_address_regex()

def equality_test_regex() -> str:
    """Regex matching an equality test: SUB / EQ."""
    return r'(?:03|1415)'

def jumpi_regex() -> str:
    """Regex matching a conditional jump: PUSH the destination then JUMPI."""
    return r'6[012][0-9a-f]{2,6}57'

def coinbase_test_regex() -> str:
    """Regex matching a test on block.coinbase, in the bytecode."""
    __coinbase = '41'
    __null = null_value_regex()
    __cast = cast_to_address_regex()
    __eq = equality_test_regex()
    __jump = jumpi_regex()
    return '(?:{null})?(?:{cast})?{coinbase}(?:{cast})?(?:{null})?(?:{cast})?(?:{test})?{jump}'.format(null=__null, cast=__cast, coinbase=__coinbase, test=__eq, jump=__jump)

def difficulty_test_regex() -> str:
    """Regex matching a test on block.difficulty / prevrandao (0x44), in the bytecode."""
    __null = null_value_regex()
    __eq = equality_test_regex()
    __jump = jumpi_regex()
    return '(?:{null})?44(?:{test})?{jump}'.format(null=__null, test=__eq, jump=__jump)

# RED-PILL TESTS ##############################################################

def bytecode_has_coinbase_test(bytecode: str) -> bool:
    """Check whether the contract tries to detect a simulation env by looking for default values in block.coinbase."""
    __match = False
    # make sure data is not interpreted as the COINBASE opcode (HEX in PUSH instruction or HEX after the end of the contract)
    if ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode=bytecode, opcode=ioseeth.parsing.bytecode.COINBASE):
        __match = bool(re.findall(pattern=coinbase_test_regex(), string=bytecode))
    return __match

def bytecode_has_difficulty_test(bytecode: str) -> bool:
    """Check whether the contract tries to detect a simulation env by looking for default values in block.difficulty."""
    __match = False
    # make sure data is not interpreted as the PREVRANDAO / DIFFICULTY opcode (HEX in PUSH instruction or HEX after the end of the contract)
    if ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode=bytecode, opcode=ioseeth.parsing.bytecode.PREVRANDAO):
        __match = bool(re.findall(pattern=difficulty_test_regex(), string=bytecode))
    return __match
