"""Handle ABIs."""

import json
import os.path

import eth_utils

import ioseeth.utils

# SIGNATURE ###################################################################

def format_signature(name: str, types: tuple) -> str:
    """Compose a function / event / error signature from its name and argument types."""
    return '{name}({arguments})'.format(
        name=name,
        arguments=','.join(types))

# HASH ########################################################################

def calculate_selector(signature: str) -> str:
    """Compute the method selector for a single signature."""
    return (eth_utils.crypto.keccak(text=signature).hex().lower())[:8] # "0x" prefix + 4 bytes

# ABI #########################################################################

def load(path: str) -> tuple:
    """Load an ABI from the references on disk."""
    with open(os.path.join(ioseeth.utils.get_data_dir_path(), 'abi/', path), 'r') as __f:
        return tuple(json.load(__f))

def calculate_all_selectors(abi: tuple, target: str='function') -> dict:
    """Compute the selector of each function and returns a dictionary {signature => selector}."""
    __result = {}
    for __o in abi:
        if __o.get('type', '') == target:
            __signature = format_signature(
                name=__o.get('name', ''),
                types=(__a.get('type', '') for __a in __o.get('inputs', [])))
            __result[__signature] = calculate_selector(signature=__signature)
    return __result
