"""Generic indicators for smart contracts."""

import functools

import ioseeth.parsing.bytecode
import ioseeth.parsing.inputs

# INTERFACES ##################################################################

@functools.lru_cache(maxsize=128)
def bytecode_implements_interface(bytecode: str, interface: tuple, threshold: float=0.8) -> bool:
    __selectors = ioseeth.parsing.bytecode.get_function_selectors(bytecode=bytecode)
    return (sum(__s in interface for __s in __selectors) / len(interface)) >= threshold # only requires to have threshold % of the interface

# CONFLICTS ###################################################################

@functools.lru_cache(maxsize=128)
def bytecode_has_implementation_for_transaction_selector(bytecode: str, data: str) -> bool:
    return (
        not data
        or (len(data) < 6)
        or (ioseeth.parsing.inputs.get_function_selector(data=data) in ioseeth.parsing.bytecode.get_function_selectors(bytecode=bytecode)))

# UNUSUAL CODING PATTERNS #####################################################

@functools.lru_cache(maxsize=128)
def bytecode_has_specific_opcodes(bytecode: str, opcodes: str, check: callable=any) -> bool:
    return check(_o in bytecode for _o in opcodes)
