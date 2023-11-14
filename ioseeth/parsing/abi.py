"""Handle ABIs."""

import json
import os.path

import ioseeth.utils

# DATA ########################################################################

def load(path: str) -> tuple:
    """Load an ABI from the references on disk."""
    with open(os.path.join(ioseeth.utils.get_data_dir_path(), 'abi/', path), 'r') as __f:
        return tuple(json.load(__f))

# SIGNATURE ###################################################################

def format_signature(name: str, types: tuple) -> str:
    """Compose a function / event / error signature from its name and argument types."""
    return '{name}({arguments})'.format(
        name=name,
        arguments=','.join(types))

def calculate_signature(abi: dict) -> str:
    """Compose a function / event / error signature from its ABI."""
    return format_signature(
        name=abi.get('name', ''),
        types=(__input.get('type', '') for __input in abi.get('inputs', [])))

def calculate_hash(abi: dict) -> str:
    """Compose a function / event / error hash from its ABI."""
    return ioseeth.utils.keccak(text=calculate_signature(abi=abi))

# HASH ########################################################################

def calculate_selector(signature: str) -> str:
    """Compute the selector for a single signature."""
    return (ioseeth.utils.keccak(text=signature.replace(' ', '')))[:8] # 4 bytes without prefix

# INDEX #######################################################################

def map_hashes_to_abis(abi: tuple, target: str='function') -> dict:
    """Compute the hash of each element in the ABI and returns a dictionary {hash => ABI}."""
    __result = {}
    for __abi in abi:
        if __abi.get('type', '') in target: # allows to specify several targets, like "event,error"
            __hash = calculate_hash(abi=__abi)
            __result[__hash] = __abi
    return __result

def map_hashes_to_signatures(abi: tuple, target: str='function') -> dict:
    """Compute the hash of each element in the ABI and returns a dictionary {hash => signature}."""
    return {
        __hash: calculate_signature(abi=__abi)
        for __hash, __abi in map_hashes_to_abis(abi=abi, target=target).items()
    }

def map_selectors_to_signatures(abi: tuple, target: str='function') -> dict:
    """Compute the selector of each element in the ABI and returns a dictionary {selector => signature}."""
    return {__hash[:8]: __signature for __hash, __signature in map_hashes_to_signatures(abi=abi, target=target).items()}

# ABIS ########################################################################

ABIS = {
    'erc-777': load(path='interfaces/IERC777.json'),
    'erc-20': load(path='token/ERC20/ERC20.json'),
    # 'erc-721': load(path='token/ERC721/ERC721.json'),
    'erc-1155': load(path='token/ERC1155/ERC1155.json'),}
