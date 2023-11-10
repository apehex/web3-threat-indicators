"""Test the selectors & signatures wordlist for the batching method."""

import pytest

import ioseeth.indicators.wordlists as iiw
import ioseeth.parsing.abi as ipa

# FIXTURES ####################################################################

KNOWN_SIGNATURES = [
    'multisendEther(address[],uint256[])',
    'multisendToken(address,address[],uint256[])',
    'disperseEther(address[],uint256[])',
    'disperseToken(address,address[],uint256[])',]

KNOWN_SELECTORS = [
    'e63d38ed',
    'c73a2d60',
    'ab883d28',
    '0b66f3f5',]

@pytest.fixture
def signature_wordlist():
    return (
        iiw.generate_signature_wordlist(pattern=iiw.PATTERNS[0])
        + iiw.generate_signature_wordlist(pattern=iiw.PATTERNS[1]))

@pytest.fixture
def selector_wordlist(signature_wordlist):
    return [ipa.calculate_selector(_s) for _s in signature_wordlist]

# SIGNATURES ##################################################################

def test_known_signatures_included_in_wordlist(signature_wordlist):
    assert all([_s in signature_wordlist for _s in KNOWN_SIGNATURES])

# SELECTORS ###################################################################

def test_known_selectors_included_in_wordlist(selector_wordlist):
    assert all([_s in selector_wordlist for _s in KNOWN_SELECTORS])
