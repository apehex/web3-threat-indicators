"""Test the reference ABIs."""

import pytest

import ioseeth.parsing.abi as ipa

# FIXTURES ####################################################################

INTERFACES = {
    'erc-20': (
        # totalSupply()
        '18160ddd',
        # balanceOf(address)
        '70a08231',
        # transfer(address,uint256)
        'a9059cbb',
        # allowance(address,address)
        'dd62ed3e',
        # approve(address,uint256)
        '095ea7b3',
        # transferFrom(address,address,uint256)
        '23b872dd'),
    'erc-721': (
        # balanceOf(address)
        '70a08231',
        # ownerOf(uint256)
        '6352211e',
        # safeTransferFrom(address,address,uint256,bytes)
        'b88d4fde',
        # safeTransferFrom(address,address,uint256)
        '42842e0e',
        # transferFrom(address,address,uint256)
        '23b872dd',
        # approve(address,uint256)
        '095ea7b3',
        # setApprovalForAll(address,bool)
        'a22cb465',
        # getApproved(uint256)
        '081812fc',
        # isApprovedForAll(address,address)
        'e985e9c5'),
    'erc-777': (
        # name()
        '06fdde03',
        # symbol()
        '95d89b41',
        # granularity()
        '556f0dc7',
        # totalSupply()
        '18160ddd',
        # balanceOf(address)
        '70a08231',
        # send(address,uint256,bytes)
        '9bd9bbc6',
        # burn(uint256,bytes)
        'fe9d9303',
        # isOperatorFor(address,address)
        'd95b6371',
        # authorizeOperator(address)
        '959b8c3f',
        # revokeOperator(address)
        'fad8b32a',
        # defaultOperators()
        '06e48538',
        # operatorSend(address,address,uint256,bytes,bytes)
        '62ad1b83',
        # operatorBurn(address,uint256,bytes,bytes)
        'fc673c4f'),
    'erc-1155': (
        # balanceOf(address,uint256)
        '00fdd58e',
        # balanceOfBatch(address[],uint256[])
        '4e1273f4',
        # setApprovalForAll(address,bool)
        'a22cb465',
        # isApprovedForAll(address,address)
        'e985e9c5',
        # safeTransferFrom(address,address,uint256,uint256,bytes)
        'f242432a',
        # safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)
        '2eb2c2d6'),}

@pytest.fixture
def erc777_abi():
    return ipa.load(path='interfaces/IERC777.json')

@pytest.fixture
def erc20_abi():
    return ipa.load(path='token/ERC20/ERC20.json')

@pytest.fixture
def erc721_abi():
    return ipa.load(path='token/ERC721/ERC721.json')

@pytest.fixture
def erc1155_abi():
    return ipa.load(path='token/ERC1155/ERC1155.json')

# HASH ########################################################################

def test_function_selector_hashing_on_common_abi(erc777_abi, erc20_abi, erc721_abi, erc1155_abi):
    __erc777_function_selectors = list(ipa.map_selectors_to_signatures(abi=erc777_abi, target='function').keys())
    __erc20_function_selectors = list(ipa.map_selectors_to_signatures(abi=erc20_abi, target='function').keys())
    __erc721_function_selectors = list(ipa.map_selectors_to_signatures(abi=erc721_abi, target='function').keys())
    __erc1155_function_selectors = list(ipa.map_selectors_to_signatures(abi=erc1155_abi, target='function').keys())
    assert all(__s in __erc777_function_selectors for __s in INTERFACES['erc-777'])
    assert all(__s in __erc20_function_selectors for __s in INTERFACES['erc-20'])
    assert all(__s in __erc721_function_selectors for __s in INTERFACES['erc-721'])
    assert all(__s in __erc1155_function_selectors for __s in INTERFACES['erc-1155'])
