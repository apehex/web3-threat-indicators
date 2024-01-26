import os.path
import pytest

import toolblocks.parsing.common as fpc
import ioseeth.utils as iu

# FIXTURES ####################################################################

@pytest.fixture
def various_iterable_objects():
    return [range(10), 'abcdef', '', {'a': 1, 'b': 2}, b'32', '0xdeadbeef', '0x', ('some', 'random', 'items'), {'a', 'similar', 'set', 'of', 'random', 'items'}, 'i guess this is enough test data'.split(' ')]

# DATA ########################################################################

def test_data_path_is_valid() -> str:
    assert 'data' in iu.get_data_dir_path()
    assert os.path.isdir(iu.get_data_dir_path())

# COVERAGE ####################################################################

def test_coverage_is_a_ratio(various_iterable_objects) -> float:
    for __a in various_iterable_objects:
        for __b in various_iterable_objects:
            __a_over_b = iu.coverage(left=__a, right=__b)
            __b_over_a = iu.coverage(left=__b, right=__a)
            assert (__a_over_b >= 0. and __a_over_b <= 1.)
            assert (__b_over_a >= 0. and __b_over_a <= 1.)

# CRYPTO ######################################################################

def test_hash_format():
    assert fpc.is_hexstr(iu.keccak(text='heyhey'))
    assert fpc.is_hexstr(iu.keccak(primitive='airdrop(address[],uint256)'.encode('utf-8')))
    assert fpc.is_hexstr(iu.keccak(hexstr='0000000000000000000000005b1995416bd61e468941e2258caacf15718a4d75'))
    assert len(iu.keccak(text='heyhey')) == 64
    assert len(iu.keccak(primitive='airdrop(address[],uint256)'.encode('utf-8'))) == 64
    assert len(iu.keccak(hexstr='0000000000000000000000005b1995416bd61e468941e2258caacf15718a4d75')) == 64
    assert iu.keccak(text='Transfer(address,address,uint256)') == 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
