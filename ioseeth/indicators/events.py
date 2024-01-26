"""Generic indicators for smart contracts."""

import enum

import toolblocks.parsing.common
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

# MAP TOPICS TO CONSTRAINTS ###################################################

EVENT_CONSTRAINTS = {__hash: _no_constraints for __hash, _ in ioseeth.parsing.events.EVENT_ABIS.items()}

def get_event_constraints(log: dict, default: callable=_no_constraints, index: dict=EVENT_CONSTRAINTS) -> callable:
    """Return the constraints for known events or empty constraints that can still be processed."""
    return index.get(ioseeth.parsing.events._get_log_topics_hash(log=log), default)

# CHECK ALL CONSTRAINTS #######################################################

def check_event_constraints(log: dict, default: callable=_no_constraints, index: dict=EVENT_CONSTRAINTS) -> int:
    """Check the log against its matching constraints."""
    __constraints = get_event_constraints(log=log, default=default, index=index)
    __inputs = ioseeth.parsing.events.parse_event_log(log=log)
    return __constraints(inputs=__inputs)

# ERC-20 ######################################################################

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

EVENT_CONSTRAINTS[ioseeth.utils.keccak(text='Transfer(address,address,uint256)')] = erc20_transfer_constraints

# ERC-721 #####################################################################

def erc721_transfer_constraints(inputs: dict, **kwargs) -> int:
    """Check constraints on ERC20 """
    __from = inputs.get('from', '')
    __to = inputs.get('to', '')
    __value = inputs.get('tokenId', '0')
    if __from == __to:
        return EventIssue.ERC20_TransferSenderEqualsRecipient
    return EventIssue.Null

# EVENT_CONSTRAINTS[ioseeth.utils.keccak(text='Transfer(address,address,uint256)')] = erc721_transfer_constraints # ERC-20 and ERC-712 transfer events have the same signature

# ERC-1155 ####################################################################
