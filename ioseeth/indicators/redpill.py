"""Indicators on anti-debugging techniques."""

import re

# REGEX #######################################################################

def cast_to_address_regex() -> str:
    """Regex matching a cast to the address type."""
    return r'73ffffffffffffffffffffffffffffffffffffffff16'

def null_value_regex() -> str:
    """Regex matching a null value: PUSH 0 then optionally DUP."""
    return r'(?:6000|5f)(?:8[012])'

def null_address_regex() -> str:
    """Regex matching a null address, in the bytecode."""
    return null_value_regex() + cast_to_address_regex()

def coinbase_address_regex() -> str:
    """Regex matching a coinbase cast to address, in the bytecode."""
    return r'41' + cast_to_address_regex()

def equality_test_regex() -> str:
    """Regex matching an equality test: SUB / EQ then PUSH the destination then JUMPI."""
    return r'(?:03|1415)6[012][0-9a-f]{2,6}57'

def coinbase_test_regex() -> str:
    """Regex matching a test on block.coinbase, in the bytecode."""
    __coinbase = coinbase_address_regex()
    __null = null_address_regex()
    __eq = equality_test_regex()
    return '(?:{null})?{coinbase}(?:{null})?{test}'.format(null=__null, coinbase=__coinbase, test=__eq)

def difficulty_test_regex() -> str:
    """Regex matching a test on block.difficulty / prevrandao (0x44), in the bytecode."""
    __null = null_value_regex()
    __eq = equality_test_regex()
    return '{null}44{test}'.format(null=__null, test=__eq)

# RED-PILL TESTS ##############################################################

def bytecode_has_coinbase_test(bytecode: str) -> bool:
    """Check whether the contract tries to detect a simulation env by looking for default values in block.coinbase."""
    return bool(re.findall(pattern=coinbase_test_regex(), string=bytecode))

def bytecode_has_difficulty_test(bytecode: str) -> bool:
    """Check whether the contract tries to detect a simulation env by looking for default values in block.difficulty."""
    return bool(re.findall(pattern=difficulty_test_regex(), string=bytecode))
