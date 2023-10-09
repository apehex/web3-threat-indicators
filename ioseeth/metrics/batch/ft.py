"""Evaluate the probability that a transaction resulted in transfers of ERC20 tokens."""

from forta_agent.transaction_event import TransactionEvent
from web3 import Web3

import ioseeth.indicators.batch
import ioseeth.metrics.probabilities
import ioseeth.options

# CONFIDENCE ##################################################################

# TODO: add ERC115

def confidence_score(
    log: TransactionEvent,
    w3: Web3,
    min_transfer_count: int=ioseeth.options.MIN_TRANSFER_COUNT,
    min_transfer_total: int=ioseeth.options.MIN_TRANSFER_TOTAL_ERC20
) -> float:
    """Evaluate the probability that a transaction handled ERC20 tokens."""
    _scores = []
    _logs = tuple(log.logs)
    # events
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.batch.log_has_multiple_erc20_transfer_events(logs=_logs, min_count=min_transfer_count, min_total=min_transfer_total),
        true_score=0.9, # certainty
        false_score=0.2)) # the token could follow another std
    return ioseeth.metrics.probabilities.conflation(_scores)

# MALICIOUS ###################################################################

# TODO: the ERC20 balance of the contract increased

def malicious_score(log: TransactionEvent, w3: Web3) -> float:
    """Evaluate the provabability that an ERC20 transaction is malicious."""
    _scores = []
    _logs = tuple(log.logs)
    # transfer of amount 0
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.batch.log_has_erc20_transfer_of_null_amount(logs=_logs),
        true_score=0.9, # certainty
        false_score=0.5)) # neutral
    return ioseeth.metrics.probabilities.conflation(_scores)
