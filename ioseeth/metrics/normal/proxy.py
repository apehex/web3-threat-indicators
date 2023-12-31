"""Evaluate the probability that multiple transfers were bundled in a transaction."""

import ioseeth.indicators.proxy
import ioseeth.metrics.probabilities

# PROXY #######################################################################

#TODO improve bytecode disassembly: wrong opcode
#TODO delegatecall opcode appears after disassembly when it's not used in original sources...

def is_redirecting_execution_to_another_contract(
    data: str,
    bytecode: str
) -> float:
    """Evaluate the probability that a given contract redirects the execution to another contract."""
    __scores = []
    # uses staticcall/delegatecall/callcode
    # __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
    #     indicator=ioseeth.indicators.proxy.bytecode_redirects_execution(bytecode=bytecode),
    #     true_score=1, # has instructions that definitely redirect to another contract
    #     false_score=0.3)) # can still use the logic of another contract without modifying its state 
    # list of recipients and amounts with same length
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=not ioseeth.indicators.generic.bytecode_has_implementation_for_transaction_selector(bytecode=bytecode, data=data),
        true_score=0.7, # execution goes through the fallback, possibly to another contract
        false_score=0.1))
    return ioseeth.metrics.probabilities.conflation(__scores)

def is_standard_proxy(
    data: str,
    bytecode: str
) -> float:
    """Evaluate the probability that the given contract is a proxy."""
    __scores = []
    # uses staticcall/delegatecall/callcode
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=is_redirecting_execution_to_another_contract(data=data, bytecode=bytecode),
        true_score=0.6, # acts like a proxy, but may still be another type of contract
        false_score=0.)) # proxies can't work without redirecting execution
    # list of recipients and amounts with same length
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.proxy.bytecode_uses_standard_proxy_slots(bytecode=bytecode),
        true_score=0.8, # very little chance another type of con
        false_score=0.3))
    return ioseeth.metrics.probabilities.conflation(__scores)

# ISSUES ######################################################################

def has_broken_proxy_implementation(
    bytecode: str
) -> float:
    """Evaluate the probability the proxy is not properly written."""
    __scores = []
    # has logic slots from several standards
    __scores.append(ioseeth.metrics.probabilities.indicator_to_probability(
        indicator=ioseeth.indicators.proxy.bytecode_has_proxy_slots_from_several_standards(bytecode=bytecode),
        true_score=0.6,
        false_score=0.5))
    return ioseeth.metrics.probabilities.conflation(__scores)
