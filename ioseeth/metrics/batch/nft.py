"""Evaluate the probability that a transaction resulted in transfers of NFTs."""

from forta_agent.transaction_event import TransactionEvent
from web3 import Web3

import ioseeth.indicators.batch
import ioseeth.metrics.probabilities
import ioseeth.options

# CONFIDENCE ##################################################################

def confidence_score(
    log: TransactionEvent,
    w3: Web3,
    min_transfer_count: int=ioseeth.options.MIN_TRANSFER_COUNT,
) -> float:
    """Evaluate the probability that a transaction handled NFT tokens."""
    _scores = []
    _logs = tuple(log.logs)
    # events
    _scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.batch.log_has_multiple_erc721_transfer_events(logs=_logs, min_count=min_transfer_count),
        true_score=0.9, # certainty
        false_score=0.2)) # the token could follow another std
    return ioseeth.metrics.probabilities.conflation(_scores)

# MALICIOUS ###################################################################

def malicious_score(log: TransactionEvent, w3: Web3) -> float:
    """Evaluate the provabability that a NFT transaction is malicious."""
    _scores = []
    return ioseeth.metrics.probabilities.conflation(_scores)
