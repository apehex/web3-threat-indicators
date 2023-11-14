"""Filter the logs for relevant ERC20 / ERC721 events."""

import copy
import functools
import itertools
import json

import eth_abi.abi
import web3._utils.abi
import web3._utils.events

import forta_toolkit.parsing.common
import ioseeth.parsing.abi

# CONSTANTS ###################################################################

EVENT_EMPTY_ABI = {'name': '', 'inputs': (), 'type': 'event'}

EVENT_ABIS = {
    __hash: __child_abi
    for __parent, __parent_abi in ioseeth.parsing.abi.ABIS.items()
    for __hash, __child_abi in ioseeth.parsing.abi.map_hashes_to_abis(abi=__parent_abi, target='event').items()}

EVENT_SIGNATURES = {
    __hash: ioseeth.parsing.abi.calculate_signature(abi=__abi)
    for __hash, __abi in EVENT_ABIS.items()}

# ABIs ########################################################################

def _abi_codec() -> eth_abi.abi.ABICodec:
    """Wrapper around the registry for encoding & decoding ABIs."""
    return eth_abi.abi.ABICodec(web3._utils.abi.build_strict_registry())

def _get_input_names(abi: dict) -> tuple:
    """Extract the name of each input of an event, from its ABI."""
    return tuple(_a.get('name', '') for _a in abi.get('inputs', []))

# TOPICS ######################################################################

def _parse_log_topics(log: dict) -> list:
    """Normalize the log topics."""
    return forta_toolkit.parsing.common.get_field(dataset=log, keys=('topics',), default=(b'',), callback=lambda __l: [forta_toolkit.parsing.common.to_bytes(__t) for __t in __l])

def _get_log_topics_hash(log: dict) -> str:
    """Return the hash of the topics, even when empty."""
    __topics = _parse_log_topics(log=log)
    return forta_toolkit.parsing.common.to_hexstr(__topics[0] if __topics else ioseeth.utils.keccak(text=''))

def _compare_abi_to_log(abi: dict, log: dict) -> bool:
    """Returns True if the abi and log match, False otherwise."""
    return ioseeth.parsing.abi.calculate_hash(abi=abi) == _get_log_topics_hash(log=log) # compare hexstr

def get_event_abi(log: dict, default: dict=EVENT_EMPTY_ABI, index: dict=EVENT_ABIS) -> dict:
    """Return the ABI for known events or an empty ABI that can still be processed."""
    return index.get(_get_log_topics_hash(log=log), default)

# INPUT INDEXATION ############################################################

def _apply_indexation_mask(abi: dict, mask: tuple) -> dict:
    """Change the "indexed" field of the ABI according to the mask."""
    _abi = copy.deepcopy(abi)
    for _i in range(len(mask)):
        _abi['inputs'][_i]['indexed'] = mask[_i]
    return _abi

def _generate_all_abi_indexation_variants(abi: dict) -> dict:
    """Generate all the variants of the ABI by switching each "indexed" field true / false for the inputs."""
    _count = len(abi.get('inputs', ()))
    _indexed = tuple(itertools.product(*(_count * ((True, False), ))))
    _abis = {_c: [] for _c in range(_count + 1)} # order by number of indexed inputs
    for _i in _indexed: # each indexation variant
        _abis[sum(_i)].append(_apply_indexation_mask(abi=abi, mask=_i))
    return _abis

def _generate_the_most_probable_abi_indexation_variant(abi: dict, indexed: int) -> dict:
    """Generate the most probable variant of the ABI for a given count of indexed inputs."""
    __count = len(abi.get('inputs', ()))
    __indexed = min(__count, max(0, indexed)) # 0 <= indexed <= count
    __mask = __indexed * (True,) + (__count - __indexed) * (False,) # index from left to right, without gaps
    return _apply_indexation_mask(abi=abi, mask=__mask)

# PARSE LOGS ##################################################################

def _get_arg_value(event: dict, name: str) -> str:
    """Extract the value of an event input from its log."""
    return str(event.get('args', {}).get(name, ''))

def _get_token_address(event: dict) -> str:
    """Extract the address of the token that emitted the event."""
    return str((event.get('address', '')))

def _parse_event(event: dict, names: tuple) -> dict:
    """Extract the relevant data from a log and format it."""
    return {
        'token': _get_token_address(event=event),
        'from': _get_arg_value(event=event, name=names[0]),
        'to': _get_arg_value(event=event, name=names[1]),
        'value': _get_arg_value(event=event, name=names[2])}

# DECODE LOGS #################################################################

def get_event_data(log: dict, abi: dict, codec: eth_abi.abi.ABICodec=_abi_codec()) -> dict:
    """Extract event data from the hex data & log topics."""
    __abi = _generate_the_most_probable_abi_indexation_variant(abi=abi, indexed=len(log.get('topics', [])) - 1)
    return web3._utils.events.get_event_data(codec, __abi, log)

def get_event_inputs(log: dict, abi: dict, codec: eth_abi.abi.ABICodec=_abi_codec()) -> dict:
    """Extract & index the event inputs from the hex data & log topics."""
    __names = _get_input_names(abi)
    __data = get_event_data(log=log, abi=abi, codec=codec)
    return {__name: _get_arg_value(event=__data, name=__name) for __name in __names}

def parse_event_log(log: dict, abi: dict={}, index: dict=EVENT_ABIS, codec: eth_abi.abi.ABICodec=_abi_codec()) -> dict:
    """Extract and format the event data."""
    __data = {}
    __abi = abi if abi else get_event_abi(log=log, default=EVENT_EMPTY_ABI, index=index)
    if _compare_abi_to_log(abi=__abi, log=log):
        __data = get_event_inputs(log=log, abi=__abi, codec=codec)
    return __data

# FILTER LOGS #################################################################

def parse_event_logs_factory(abi: dict, codec: eth_abi.abi.ABICodec=_abi_codec()) -> callable:
    """Adapt the parsing logic to a given event."""
    __inputs = _get_input_names(abi)

    def __parse_logs(logs: tuple) -> tuple:
        """Extract all the event matching a given ABI."""
        # parse
        _events = (get_event_data(log=__log, abi=abi, codec=codec) for __log in logs if _compare_abi_to_log(abi=abi, log=__log))
        # return the args of each event in a dict
        return tuple(_parse_event(event=_e, names=__inputs) for _e in _events)

    return __parse_logs

# SHORTHANDS ##################################################################

filter_logs_for_erc20_transfer_events = parse_event_logs_factory(abi=EVENT_ABIS.get('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef', EVENT_EMPTY_ABI), codec=_abi_codec())

filter_logs_for_erc721_transfer_events = parse_event_logs_factory(abi=EVENT_ABIS.get('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef', EVENT_EMPTY_ABI), codec=_abi_codec()) # ERC-20 and ERC-712 "Transfer" events have the same signature
