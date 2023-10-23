"""."""

import web3

# CREATION ####################################################################

def find_deployment_block_for_contract(
    provider: web3.Web3,
    address: str,
    left: int=0,
    right: int=-1
) -> int:
    """Find the deployment block for a contract."""
    __left = left
    __right = right if right > left else provider.eth.get_block('latest').number
    while __left < __right:
        __next = (__left + __right) // 2
        __code = provider.eth.get_code(account=address, block_identifier=__next)
        if len(__code) == 0:
            __left = __next + 1
        else:
            __right = __next
        print('{block}: {code} => {id}'.format(block=__next, code=__code.hex()[:10], id=hash(__code)))
    return __left
