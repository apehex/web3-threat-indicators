"""Identify generic properties of transactions / traces / addresses."""

import ioseeth.metrics.probabilities

# SUICIDE #####################################################################

def is_trace_contract_self_destruction(
    action: str, # trace.type
    **kwargs
) -> float:
    """Evaluate the probability that a transaction destroyed a contract.
    0xff7c1a73c054b75f146afe109972a608afd9503b6962e062c392e131b1678b89"""
    __scores = []
    # trace type = suicide
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator='suicide' in action,
        true_score=0.9,
        false_score=0.1))
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)
