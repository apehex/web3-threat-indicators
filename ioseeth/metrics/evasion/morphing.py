"""Evaluate the probability that multiple transfers were bundled in a transaction."""

from web3 import Web3

import ioseeth.indicators.generic
import ioseeth.indicators.metamorphism
import ioseeth.metrics.probabilities
import ioseeth.parsing.bytecode

# CONSTANTS ###################################################################

UNUSUAL_OPCODES = (ioseeth.parsing.bytecode.BLOCKHASH,)
RED_PILL_OPCODES = (ioseeth.parsing.bytecode.COINBASE,)
RESET_OPCODES = (ioseeth.parsing.bytecode.SELFDESTRUCT, ioseeth.parsing.bytecode.DELEGATECALL, ioseeth.parsing.bytecode.CALLCODE)
FACTORY_SELECTORS = ('aaf10f42', '0d917df4', '25ff967e', 'c7fcb49b') # getImplementation(), ?, setByteCode(bytes), ?

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

# TRANSACTIONS

def is_transaction_metamorphic_transient_contract_deployment() -> float:
    """Evaluate the probability that a transaction deployed a transient contract.
    Ex: 0x3c48308839cc60046615d0b0984ded9e47ac9467a2692cfd19e1c7abcb30d6e5"""
    __scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_transaction_metamorphic_factory_contract_deployment(
    bytecode: str,
    **kwargs
) -> float:
    """Evaluate the probability that a transaction deployed a mutant factory.
    Ex: 0x0f7c1dad199b29bc016c0984194b7b29ba68b130bd3d9a83e5bb20de7159d33c"""
    __scores = []
    # deploys implementation with CREATE
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode=bytecode, opcode=ioseeth.parsing.bytecode.CREATE),
        true_score=0.6, # legitimate contracts also use CREATE
        false_score=0.4)) # the implementation could be deployed outside of the factory, it only needs its address
    # deploys mutant with CREATE2
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode=bytecode, opcode=ioseeth.parsing.bytecode.CREATE2),
        true_score=0.6, # legitimate contracts also use CREATE2
        false_score=0.1)) # CREATE2 is required to morph
    # stores metamorphic init code for the mutant contract
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.metamorphism.bytecode_has_known_metamorphic_init_code(bytecode=bytecode),
        true_score=0.9, # certainty
        false_score=0.5)) # the factory could use another variation on the init code
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_transaction_metamorphic_mutant_contract_deployment() -> float:
    """Evaluate the probability that a transaction (re)deployed a mutant contract.
    Ex: 0x2309f6e8e041dfadafbd73c60b08f33e60337b6330704b494f902bb9c4766fb3"""
    __scores = []
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_transaction_contract_destruction() -> float:
    """Evaluate the probability that a transaction destroyed a contract.
    Ex: 0xff7c1a73c054b75f146afe109972a608afd9503b6962e062c392e131b1678b89"""
    __scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

# ADRESSES

def is_address_metamorphic_transient(
    bytecode: str,
    **kwargs
) -> float:
    """Evaluate the probability that a contract can deploy code that is metamorphic."""
    __scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_address_metamorphic_factory(
    bytecode: str,
    **kwargs
) -> float:
    """Evaluate the probability that a contract can deploy code that is metamorphic."""
    __scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_address_metamorphic_implementation(
    bytecode: str,
    **kwargs
) -> float:
    """Evaluate the probability that a contract can deploy code that is metamorphic."""
    __scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_address_metamorphic_mutant(
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
    # check for known factory code
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.metamorphism.bytecode_has_known_metamorphic_init_code(bytecode=target_creation_bytecode),
        true_score=0.6, # 
        false_score=0.1))
    # check whether the code actually changed
    return ioseeth.metrics.probabilities.conflation(__scores)
