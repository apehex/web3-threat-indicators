"""Evaluate the probability that a transaction resulted in transfers of native tokens."""

import toolblocks.parsing.common

import ioseeth.indicators.batch
import ioseeth.metrics.probabilities

# CONFIDENCE ##################################################################

def confidence_score(
    data: str,
    value: str,
    min_transfer_count: int=8,
    min_transfer_total: int=10**18,
    max_batching_fee: int=2*10**17,
    **kwargs
) -> float:
    """Evaluate the probability that a transaction resulted in transfers of native tokens."""
    _scores = []
    # parse
    __value = toolblocks.parsing.common.to_int(value) # all the transaction data is formated as hexstr
    # "from" contract balance significantly changed
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=__value >= max_batching_fee, # mvt below 0.1 ETH are ignored
        true_score=0.5, # required, but not conclusive
        false_score=0.1)) # certainty: no batch transfer without updating the sender's balance
    # check whether the transaction value is sprayed (split and sent to multiple recipients)
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.batch.transaction_value_matches_input_arrays(value=__value, data=data, min_count=min_transfer_count, tolerance=max_batching_fee),
        true_score=0.8, # very likely: the transaction value is split among recipients specified in the inputs
        false_score=0.2)) # addresses specified outside of the inputs could have had their balance changed
    # combine
    return ioseeth.metrics.probabilities.conflation(_scores)

# MALICIOUS ###################################################################

def malicious_score(
    min_transfer_count: int=8,
    max_batching_fee: int=2 * 10 ** 17,
    **kwargs
) -> float:
    """Evaluate the provabability that the transfer is malicious."""
    _scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(_scores)
