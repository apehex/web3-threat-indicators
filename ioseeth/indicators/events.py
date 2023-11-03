"""Generic indicators for smart contracts."""

import enum

import ioseeth.parsing.abi
import ioseeth.parsing.events
import ioseeth.utils

# TODO several events have the same hash, but the index only stores one

# TAXONOMY ####################################################################

class EventIssue(enum.IntEnum):
    Null = 0
    ERC20_TransferSenderEqualsRecipient = enum.auto()
    ERC20_TransferNullAmount = enum.auto()
    ERC721_TransferSenderEqualsRecipient = enum.auto()

# GENERIC #####################################################################

def _no_constraints(**kwargs) -> int:
    """Default function for non indexed events, always return EventIssue.Null"""
    return EventIssue.Null

EMPTY_EVENT_ABI = {'name': '', 'inputs': (), 'type': 'event'}
EMPTY_EVENT_METADATA = {'signature': '', 'parent': '', 'abi': EMPTY_EVENT_ABI, 'constraints': _no_constraints}
    
# ABIS ########################################################################

ABIS = {
    'erc-777': ioseeth.parsing.abi.load(path='interfaces/IERC777.json'),
    'erc-20': ioseeth.parsing.abi.load(path='token/ERC20/ERC20.json'),
    # 'erc-721': ioseeth.parsing.abi.load(path='token/ERC721/ERC721.json'),
    'erc-1155': ioseeth.parsing.abi.load(path='token/ERC1155/ERC1155.json'),}

# MAP TOPICS TO CONSTRAINTS ###################################################

def map_hashes_to_event_metadata(abis: tuple=ABIS) -> dict:
    """Create a map from event hash (topic) to event metadata (constraints)."""
    return {
        __hash: {'signature': ioseeth.parsing.abi.calculate_signature(abi=__child_abi), 'parent': __parent, 'abi': __child_abi, 'constraints': _no_constraints}
        for __parent, __parent_abi in abis.items()
        for __hash, __child_abi in ioseeth.parsing.abi.map_hashes_to_abis(abi=__parent_abi, target='event').items()}

EVENT_INDEX = map_hashes_to_event_metadata(abis=ABIS)

# ERC-20 ######################################################################

# check whether "from" is a legit contract?

def erc20_transfer_constraints(inputs: dict, **kwargs) -> int:
    """Check constraints on ERC20 """
    __from = inputs.get('from', '')
    __to = inputs.get('to', '')
    __value = inputs.get('value', '0')
    if __from == __to:
        return EventIssue.ERC20_TransferSenderEqualsRecipient
    if int(__value) == 0:
        return EventIssue.ERC20_TransferNullAmount
    return EventIssue.Null

EVENT_INDEX[ioseeth.utils.keccak(text='Transfer(address,address,uint256)')]['constraints'] = erc20_transfer_constraints

# ERC-721 #####################################################################

def erc721_transfer_constraints(inputs: dict, **kwargs) -> int:
    """Check constraints on ERC20 """
    __from = inputs.get('from', '')
    __to = inputs.get('to', '')
    __value = inputs.get('tokenId', '0')
    if __from == __to:
        return EventIssue.ERC20_TransferSenderEqualsRecipient
    return EventIssue.Null

# ERC-1155 ####################################################################

# CHECK ALL CONSTRAINTS #######################################################

def check_event_constraints(log: dict, index: dict=EVENT_INDEX, empty_metadata: dict=EMPTY_EVENT_METADATA, empty_abi: dict=EMPTY_EVENT_ABI) -> int:
    """Check the log against its matching constraints."""
    __hash = getattr(log, 'topics', (b'',))[0].hex().lower().replace('0x', '')
    __metadata = index.get(__hash, empty_metadata)
    __constraints = __metadata.get('constraints', _no_constraints)
    __abi = __metadata.get('abi', empty_abi)
    __data = ioseeth.parsing.events.parse_event_log(log=log, abi=__abi)
    return __constraints(inputs=__data)
