"""Evaluate the probability that multiple transfers were bundled in a transaction."""

from web3 import Web3

import ioseeth.metrics.probabilities
import ioseeth.parsing.bytecode
import ioseeth.indicators.redpill

# CONSTANTS ###################################################################

UNUSUAL_OPCODES = (ioseeth.parsing.bytecode.BLOCKHASH,)
RED_PILL_OPCODES = (ioseeth.parsing.bytecode.COINBASE,)

# RED PILL ####################################################################

def is_trace_red_pill_contract_creation(
    action: str, # trace.type
    runtime_bytecode: str, # trace.result.code
    **kwargs
) -> float:
    """Evaluate the probability that a contract is trying to evade simulation environments."""
    __scores = []
    # trace must be a contract creation
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator='create' in action.lower(), # works also for create2
        true_score=0.5, # legitimate contracts also use CREATE
        false_score=0.1)) # not a contract creation
    # contract checks block.coinbase agains default values
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.redpill.bytecode_has_coinbase_test(bytecode=runtime_bytecode),
        true_score=0.8,
        false_score=0.5))
    # contract checks block.difficulty agains default values
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.redpill.bytecode_has_difficulty_test(bytecode=runtime_bytecode),
        true_score=0.8,
        false_score=0.5))
    return ioseeth.metrics.probabilities.conflation(__scores)
