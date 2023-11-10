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

# ABIs ########################################################################

# TODO variants with / without indexing

ERC20_APPROVAL_EVENT = json.loads('{"name":"Approval","type":"event","anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}]}')
ERC20_TRANSFER_EVENT = json.loads('{"name":"Transfer","type":"event","anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}]}')
ERC721_APPROVAL_EVENT = json.loads('{"name":"Approval","type":"event","anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_approved","type":"address"},{"indexed":true,"name":"_tokenId","type":"uint256"}]}')
ERC721_APPROVAL_FOR_ALL_EVENT = json.loads('{"name":"ApprovalForAll","type":"event","anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_operator","type":"address"},{"indexed":false,"name":"_approved","type":"bool"}]}')
ERC721_TRANSFER_EVENT = json.loads('{"name":"Transfer","type":"event","anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":true,"name":"_tokenId","type":"uint256"}]}')

def _get_input_names(abi: dict) -> tuple:
    """Extract the name of each input of an event, from its ABI."""
    return tuple(_a.get('name', '') for _a in abi.get('inputs', []))

def _abi_codec() -> eth_abi.abi.ABICodec:
    """Wrapper around the registry for encoding & decoding ABIs."""
    return eth_abi.abi.ABICodec(web3._utils.abi.build_strict_registry())

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
    __mask = indexed * (True,) + (__count - indexed) * (False,) # index from left to right, without gaps
    return _apply_indexation_mask(abi=abi, mask=__mask)

def _compare_abi_to_log(abi: dict, log: dict) -> bool:
    """Returns True if the abi and log match, False otherwise."""
    __topics = log.get('topics', ())
    return (
        bool(__topics)
        and ioseeth.parsing.abi.calculate_hash(abi=abi) == forta_toolkit.parsing.common.to_hexstr(__topics[0])) # compare hexstr

# FORMAT ######################################################################

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

# DECODE ######################################################################

def get_event_data(log: dict, abi: dict, codec: eth_abi.abi.ABICodec=_abi_codec()) -> dict:
    """Extract event data from the hex log topics."""
    __abi = _generate_the_most_probable_abi_indexation_variant(abi=abi, indexed=len(log.get('topics', [])) - 1)
    return web3._utils.events.get_event_data(codec, __abi, log)

def parse_event_log(log: dict, abi: dict, codec: eth_abi.abi.ABICodec=_abi_codec()) -> dict:
    """Extract and format the event data."""
    __data = {}
    if _compare_abi_to_log(abi=abi, log=log):
        __inputs = _get_input_names(abi)
        __event = get_event_data(log=log, abi=abi, codec=codec)
        __data = {__name: _get_arg_value(event=__event, name=__name) for __name in __inputs}
    return __data

def parse_logs_factory(abi: dict=ERC20_TRANSFER_EVENT, codec: eth_abi.abi.ABICodec=_abi_codec()) -> callable:
    """Adapt the parsing logic to a given event."""
    __inputs = _get_input_names(abi)

    def _parse_logs(logs: tuple) -> tuple:
        """Extract all the event matching a given ABI."""
        # parse
        _events = (get_event_data(log=__log, abi=abi, codec=codec) for __log in logs if _compare_abi_to_log(abi=abi, log=__log))
        # return the args of each event in a dict
        return tuple(_parse_event(event=_e, names=__inputs) for _e in _events)

    return _parse_logs

# SHORTHANDS ##################################################################

filter_logs_for_erc20_transfer_events = parse_logs_factory(abi=ERC20_TRANSFER_EVENT, codec=_abi_codec())

filter_logs_for_erc721_transfer_events = parse_logs_factory(abi=ERC721_TRANSFER_EVENT, codec=_abi_codec())
