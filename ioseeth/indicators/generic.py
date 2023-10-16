"""Generic indicators for smart contracts."""

import ioseeth.parsing.abi
import ioseeth.parsing.bytecode
import ioseeth.parsing.inputs

# META ########################################################################

def transaction_is_contract_creation(recipient: str) -> bool:
    """Check whether the transaction created a new contract at the target address."""
    return not recipient

# OPCODES #####################################################################

def bytecode_has_selfdestruct(bytecode: str) -> bool:
    """Check if the runtime code contains the SELFDESTRUCT opcode"""
    return ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode, ioseeth.parsing.bytecode.SELFDESTRUCT)

def bytecode_has_create2(bytecode: str) -> bool:
    """Check if the runtime code contains the CREATE2 opcode"""
    return ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode, ioseeth.parsing.bytecode.CREATE2)

def bytecode_has_delegatecall(bytecode: str) -> bool:
    """Check if the runtime code contains the DELEGATECALL opcode"""
    return ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode, ioseeth.parsing.bytecode.DELEGATECALL)

# INTERFACES ##################################################################

def bytecode_has_specific_interface(bytecode: str, abi: tuple, threshold: float=0.8, raw: bool=False) -> bool:
    __selectors = ioseeth.parsing.bytecode.get_function_selectors(bytecode=bytecode, raw=raw)
    __interface = tuple(ioseeth.parsing.abi.calculate_all_selectors(abi=abi, target='function').values())
    return (sum(__s in __interface for __s in __selectors) / len(__interface)) >= threshold # only requires to have threshold % of the interface

# CONFLICTS ###################################################################

def bytecode_has_implementation_for_transaction_selector(bytecode: str, data: str) -> bool:
    return (
        not data
        or (len(data) < 6)
        or (ioseeth.parsing.inputs.get_function_selector(data=data) in ioseeth.parsing.bytecode.get_function_selectors(bytecode=bytecode)))
