"""Indicators on token contracts."""

import ioseeth.indicators.generic
import ioseeth.parsing.abi
import ioseeth.parsing.bytecode
import ioseeth.parsing.inputs

# CONSTANTS ###################################################################

ERC777_ABI = ioseeth.parsing.abi.load(path='interfaces/IERC777.json')
ERC20_ABI = ioseeth.parsing.abi.load(path='token/ERC20/ERC20.json')
ERC721_ABI = ioseeth.parsing.abi.load(path='token/ERC721/ERC721.json')
ERC1155_ABI = ioseeth.parsing.abi.load(path='token/ERC1155/ERC1155.json')

# ERC-20 ######################################################################

def bytecode_has_erc20_interface(bytecode: str, abi: tuple=ERC20_ABI, threshold: float=0.8) -> bool:
    return ioseeth.indicators.generic.bytecode_has_specific_interface(bytecode=bytecode, abi=abi, threshold=threshold)

# ERC-721 #####################################################################

def bytecode_has_erc721_interface(bytecode: str, abi: tuple=ERC721_ABI, threshold: float=0.8) -> bool:
    return ioseeth.indicators.generic.bytecode_has_specific_interface(bytecode=bytecode, abi=abi, threshold=threshold)

# ERC-777 #####################################################################

def bytecode_has_erc777_interface(bytecode: str, abi: tuple=ERC777_ABI, threshold: float=0.8) -> bool:
    return ioseeth.indicators.generic.bytecode_has_specific_interface(bytecode=bytecode, abi=abi, threshold=threshold)

# ERC-1155 ####################################################################

def bytecode_has_erc1155_interface(bytecode: str, abi: tuple=ERC1155_ABI, threshold: float=0.8) -> bool:
    return ioseeth.indicators.generic.bytecode_has_specific_interface(bytecode=bytecode, abi=abi, threshold=threshold)

# ANY TOKEN ###################################################################

def bytecode_has_any_token_interface(bytecode: str, threshold: float=0.8) -> bool:
    return (
        bytecode_has_erc20_interface(bytecode=bytecode, threshold=threshold)
        or bytecode_has_erc721_interface(bytecode=bytecode, threshold=threshold)
        or bytecode_has_erc777_interface(bytecode=bytecode, threshold=threshold)
        or bytecode_has_erc1155_interface(bytecode=bytecode, threshold=threshold))
