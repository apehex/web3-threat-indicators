"""Evaluate the probability that a transaction resulted in transfers of ERC20 tokens."""

import collections.abc

import ioseeth.indicators.batch
import ioseeth.metrics.probabilities

# FT ##########################################################################

# TODO: add ERC115

def has_log_multiple_fungible_token_transfers(
    logs: collections.abc.Iterable,
    min_transfer_count: int=8,
    min_transfer_total: int=0,
    **kwargs
) -> float:
    """Evaluate the probability that a transaction handled ERC20 tokens."""
    _scores = []
    # events
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.batch.log_has_multiple_erc20_transfer_events(logs=logs, min_count=min_transfer_count, min_total=min_transfer_total),
        true_score=0.9, # certainty
        false_score=0.2)) # the token could follow another std
    # combine
    return ioseeth.metrics.probabilities.conflation(_scores)

# TODO: the ERC20 balance of the contract increased

def has_log_malicious_fungible_token_transfer(
    logs: tuple,
    **kwargs
) -> float:
    """Evaluate the provabability that an ERC20 transaction is malicious."""
    _scores = []
    # transfer of amount 0
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.batch.log_has_erc20_transfer_of_null_amount(logs=logs),
        true_score=0.9, # certainty
        false_score=0.5)) # neutral
    # combine
    return ioseeth.metrics.probabilities.conflation(_scores)

# NFT #########################################################################

def has_log_multiple_non_fungible_token_transfers(
    logs: collections.abc.Iterable,
    min_transfer_count: int=8,
    **kwargs
) -> float:
    """Evaluate the probability that a transaction handled NFT tokens."""
    _scores = []
    # events
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.batch.log_has_multiple_erc721_transfer_events(logs=logs, min_count=min_transfer_count),
        true_score=0.9, # certainty
        false_score=0.2)) # the token could follow another std
    # combine
    return ioseeth.metrics.probabilities.conflation(_scores)

def has_log_malicious_non_fungible_token_transfer(
    **kwargs
) -> float:
    """Evaluate the provabability that a NFT transaction is malicious."""
    _scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(_scores)
