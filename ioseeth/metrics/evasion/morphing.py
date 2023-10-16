"""Evaluate the probability that multiple transfers were bundled in a transaction."""

from web3 import Web3

import ioseeth.indicators.generic
import ioseeth.metrics.probabilities
import ioseeth.parsing.bytecode

# CONSTANTS ###################################################################

UNUSUAL_OPCODES = (ioseeth.parsing.bytecode.BLOCKHASH,)
RED_PILL_OPCODES = (ioseeth.parsing.bytecode.COINBASE,)
RESET_OPCODES = (ioseeth.parsing.bytecode.SELFDESTRUCT, ioseeth.parsing.bytecode.DELEGATECALL)

# RED PILL ####################################################################

def is_red_pill(
    bytecode: str,
    **kwargs
) -> float:
    """Evaluate the probability that a contract is trying to evade simulation environments."""
    __scores = []
    # opcodes used to detect simulation environments
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcodes(bytecode=bytecode, opcodes=RED_PILL_OPCODES, check=any),
        true_score=0.6,
        false_score=0.5))
    return ioseeth.metrics.probabilities.conflation(__scores)

# METAMORPHIC CONTRACTS #######################################################

# has reset opcodes?
    # no
        # => out
    # yes
        # does deployer use CREATE2?
            # no
                # => out
            # yes
                #

def is_metamorphic(
    deployer_runtime_bytecode: str,
    target_creation_bytecode: str,
    target_runtime_bytecode: str,
    **kwargs
) -> float:
    """Evaluate the probability that a contract can change its code."""
    __scores = []
    # requires SELFDESTRUCT to replace the code, either from the contract itself or from a delegate
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcodes(bytecode=runtime_bytecode, opcodes=RESET_OPCODES, check=any),
        true_score=0.5, # required but not conclusive
        false_score=0.1))
    # must be deployed by another contract using CREATE2
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode=deployer_bytecode, opcode=ioseeth.parsing.bytecode.CREATE2),
        true_score=0.6, # 
        false_score=0.1))
    # check whether the code actually changed
    return ioseeth.metrics.probabilities.conflation(__scores)