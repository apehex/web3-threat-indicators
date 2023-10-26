"""Evaluate the probability that contracts mutate / can change their code."""

from web3 import Web3

import ioseeth.indicators.generic
import ioseeth.indicators.metamorphism
import ioseeth.metrics.probabilities
import ioseeth.parsing.bytecode

# CONSTANTS ###################################################################

RESET_OPCODES = (ioseeth.parsing.bytecode.SELFDESTRUCT, ioseeth.parsing.bytecode.DELEGATECALL, ioseeth.parsing.bytecode.CALLCODE)
FACTORY_SELECTORS = ('aaf10f42', '0d917df4', '25ff967e', 'c7fcb49b') # getImplementation(), ?, setByteCode(bytes), ?
GET_IMPLEMENTATION_SELECTORS = ('aaf10f42')

# INIT CODE ###################################################################

def is_bytecode_metamorphic_init_code(
    bytecode: str,
    **kwargs
) -> float:
    """Evaluate the probability that the given bytecode is actually metamorphic bytecode."""
    __scores = []
    # small
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=len(bytecode) <= 128,
        true_score=0.6,
        false_score=0.2))
    # contains known init code
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.metamorphism.bytecode_has_known_metamorphic_init_code(bytecode=bytecode),
        true_score=0.9, # not 1 because some runtime code could contain init code while not being init code itself
        false_score=0.5))
    # copies code from another contract
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode=bytecode, opcode=ioseeth.parsing.bytecode.EXTCODECOPY),
        true_score=0.6,
        false_score=0.3))
    # retrieves implementation address from factory
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=any(__s in bytecode for __s in GET_IMPLEMENTATION_SELECTORS),
        true_score=0.6,
        false_score=0.5))
    return ioseeth.metrics.probabilities.conflation(__scores)

# FACTORY #####################################################################

def is_trace_factory_contract_creation(
    action: str, # trace.type
    creation_bytecode: str, # trace.action.init
    runtime_bytecode: str, # trace.result.code
    **kwargs
) -> float:
    """Evaluate the probability that an internal transaction deployed a metamorphic factory.
    0x0f7c1dad199b29bc016c0984194b7b29ba68b130bd3d9a83e5bb20de7159d33c
    0x29b2d5787757d494907b349662a3730340c88641d5ae78037928c2870d2b4cce"""
    __scores = []
    # trace must be a contract creation
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator='create' in action, # works also for create2
        true_score=0.5, # legitimate contracts also use CREATE
        false_score=0.1)) # not a contract creation
    # static analysis: the runtime bytecode deploys implementation with CREATE
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode=runtime_bytecode, opcode=ioseeth.parsing.bytecode.CREATE),
        true_score=0.6, # legitimate contracts also use CREATE
        false_score=0.4)) # the implementation could be deployed outside of the factory, it only needs its address
    # static analysis: the runtime bytecode deploys mutant with CREATE2
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.parsing.bytecode.bytecode_has_specific_opcode(bytecode=runtime_bytecode, opcode=ioseeth.parsing.bytecode.CREATE2),
        true_score=0.6, # legitimate contracts also use CREATE2
        false_score=0.1)) # CREATE2 is required to morph
    # stores metamorphic init code for the mutant contract
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.metamorphism.bytecode_has_known_metamorphic_init_code(bytecode=creation_bytecode), # could be set in the constructor
        true_score=0.9, # certainty
        false_score=0.5)) # the factory could use another variation on the init code
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_transaction_factory_contract_deployment(
    to: str, # tx.to
    data: str, # tx.data
    **kwargs
) -> float:
    """Evaluate the probability that a transaction deployed a mutant factory.
    0x0f7c1dad199b29bc016c0984194b7b29ba68b130bd3d9a83e5bb20de7159d33c
    0x29b2d5787757d494907b349662a3730340c88641d5ae78037928c2870d2b4cce"""
    __scores = []
    # parse the input data of the transaction
    __parts = ioseeth.parsing.bytecode.parse_creation_data(data=data)
    # contract creation by EOA
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=not bool(to),
        true_score=0.5, # could be any contract creation
        false_score=0.4)) # factories are (slightly) more likely to be deployed by an EOA than another contract 
    # static analysis
    if not to and len(__parts) > 1:
        __scores.append(is_trace_factory_contract_creation(action='create', creation_bytecode=data, runtime_bytecode=__parts[1]))
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

# TRANSIENT CONTRACT ##########################################################

def is_transaction_transient_contract_deployment() -> float:
    """Evaluate the probability that a transaction deployed a transient contract.
    0x3c48308839cc60046615d0b0984ded9e47ac9467a2692cfd19e1c7abcb30d6e5"""
    __scores = []
    # combine
    return ioseeth.metrics.probabilities.conflation(__scores)

# IMPLEMENTATION ##############################################################

# 0x3bfcc1c5838ee17eec1ddda2f1ff0ac1c1ccdbd30dd520ee41215c54227a847f

# MUTANT ######################################################################

def is_trace_mutant_contract_creation(
    action: str, # trace.type
    creation_bytecode: str, # trace.action.init
    runtime_bytecode: str, # trace.result.code
    **kwargs
) -> float:
    """Evaluate the probability that a transaction (re)deployed a mutant contract.
    0x2309f6e8e041dfadafbd73c60b08f33e60337b6330704b494f902bb9c4766fb3
    0x3bfcc1c5838ee17eec1ddda2f1ff0ac1c1ccdbd30dd520ee41215c54227a847f"""
    __scores = []
    __creation = ioseeth.parsing.bytecode.normalize(creation_bytecode)
    __runtime = ioseeth.parsing.bytecode.normalize(runtime_bytecode)
    # trace must be a contract creation
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator='create' in action, # unfortunately transaction traces don't differentiate CREATE and CREATE2
        true_score=0.5, # legitimate contracts also use CREATE ofc
        false_score=0.1)) # not a contract creation
    # the creation bytecode is actually metamorphic init code
    __scores.append(is_bytecode_metamorphic_init_code(bytecode=__creation))
    # the runtime bytecode is not in the creation bytecode => fetched from another contract
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=not __runtime in __creation,
        true_score=0.7,
        false_score=0.4)) # the code copy could be done from another transaction
    # the code changed
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_transaction_mutant_contract_deployment() -> float:
    """Evaluate the probability that a transaction (re)deployed a mutant contract.
    0x2309f6e8e041dfadafbd73c60b08f33e60337b6330704b494f902bb9c4766fb3
    0x3bfcc1c5838ee17eec1ddda2f1ff0ac1c1ccdbd30dd520ee41215c54227a847f"""
    __scores = []
    return ioseeth.metrics.probabilities.conflation(__scores)
