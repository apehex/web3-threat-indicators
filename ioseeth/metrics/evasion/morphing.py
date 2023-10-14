"""Evaluate the probability that multiple transfers were bundled in a transaction."""

from web3 import Web3

import ioseeth.indicators.generic
import ioseeth.metrics.probabilities
import ioseeth.parsing.bytecode

# CONSTANTS ###################################################################

UNUSUAL_OPCODES = (ioseeth.parsing.bytecode.BLOCKHASH,)

RED_PILL_OPCODES = (ioseeth.parsing.bytecode.COINBASE,)

# RED PILL ####################################################################

def is_red_pill(
    bytecode: str,
) -> float:
    """Evaluate the probability that a contract is trying to evade simulation environments."""
    __scores = []
    # opcodes used to detect simulation environments
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcodes(bytecode=bytecode, opcodes=RED_PILL_OPCODES, check=any),
        true_score=0.7,
        false_score=0.5))
    return ioseeth.metrics.probabilities.conflation(__scores)
