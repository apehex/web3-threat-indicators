"""Track the evolution of native token balances."""

import functools

import web3.Web3

# DELTA #######################################################################

@functools.lru_cache(maxsize=128)
def get_balance_delta(provider: web3.Web3, address: str, block: int) -> int:
    """Calculate the difference in balance before / after a given block."""
    _before = _after = 0
    if address:
        _before = provider.eth.get_balance(web3.Web3.toChecksumAddress(address), block - 1)
        _after = provider.eth.get_balance(web3.Web3.toChecksumAddress(address), block)
    return _after - _before

@functools.lru_cache(maxsize=128)
def get_balance_deltas(provider: web3.Web3, addresses: list, block: int) -> dict:
    """List all the addresses that sustained a balance change."""
    _deltas = {_a: get_balance_delta(provider=provider, address=_a, block=block) for _a in addresses}
    return {_a: _d for _a, _d in _deltas.items() if abs(_d) > 0}
