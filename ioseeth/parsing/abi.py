"""Handle ABIs."""

import eth_utils

# SIGNATURE ###################################################################

def format_signature(name: str, types: tuple) -> str:
    """"""
    return '{name}({arguments})'.format(
        name=name,
        arguments=','.join(types))

# HASH ########################################################################

def selector(signature: str) -> str:
    """Compute the method selector for a single signature."""
    return (eth_utils.crypto.keccak(text=signature).hex().lower())[:8] # "0x" prefix + 4 bytes

# ABI #########################################################################

def calculate_selectors(abi: list, target: str='function') -> dict:
    """Compute the selector of each function and returns a dictionary {signature => selector}."""
    __result = {}
    for __o in abi:
        if __o.get('type', '') == target:
            __signature = format_signature(
                name=__o.get('name', ''),
                types=(__a.get('type', '') for __a in __o.get('inputs', [])))
            __result[__signature] = selector(signature=__signature)
    return __result
