"""Evaluate the probability that multiple transfers were bundled in a transaction."""

import collections.abc
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

def is_traces_red_pill_contract_creation(
    traces: collections.abc.Iterable,
    **kwargs
) -> float:
    """Evaluate the probability that any internal transaction (re)deployed a mutant contract.
    0x0f7c1dad199b29bc016c0984194b7b29ba68b130bd3d9a83e5bb20de7159d33c
    0x29b2d5787757d494907b349662a3730340c88641d5ae78037928c2870d2b4cce"""
    __scores = [
        is_trace_red_pill_contract_creation(
            action=__t.get('type', ''),
            runtime_bytecode=__t.get('output', ''))
        for __t in traces]
    # a single match is enough
    return max(__scores)
