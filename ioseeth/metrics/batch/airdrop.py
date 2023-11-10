"""Evaluate the probability that a transaction resulted in an airdrop."""

import collections.abc

import ioseeth.indicators.batch
import ioseeth.metrics.probabilities

# CONFIDENCE ##################################################################

def confidence_score(
    data: str,
    logs: collections.abc.Iterable,
    min_transfer_count: int=8,
    min_transfer_total: int=0,
    **kwargs
) -> float:
    """Evaluate the probability that a transaction is an airdrop."""
    _scores = []
    # performs token transfers
    _has_token_mint_events = (
        ioseeth.indicators.batch.log_has_multiple_erc20_mint_events(logs=logs, min_count=min_transfer_count, min_total=min_transfer_total)
        or ioseeth.indicators.batch.log_has_multiple_erc721_mint_events(logs=logs, min_count=min_transfer_count))
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=_has_token_mint_events,
        true_score=0.9, # the tokens were minted
        false_score=0.2)) # could be another standard
    # doesn't have input
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=not ioseeth.indicators.batch.input_data_has_array_of_addresses(data=data, min_length=min_transfer_count),
        true_score=0.6, # not enough to conclude
        false_score=0.4)) # some airdrop functions take inputs
    # combine
    return ioseeth.metrics.probabilities.conflation(_scores)

# MALICIOUS ###################################################################

# TODO: contract accumulates wealth
# TODO: new contract / new token
# TODO: contract pretends to be a known token (ex: Tether USDT)

def malicious_score(
    **kwargs
) -> float:
    """Evaluate the provabability that an airdrop is malicious."""
    _scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(_scores)
