"""Test the boolean indicators."""

import pytest

import ioseeth.indicators.batch as iib
import tests.test_data as td

# FIXTURES ####################################################################

TX_TO = [__t['to'] for __t in td.TRANSACTIONS['batch'].get('fungible-token', []) + td.TRANSACTIONS['batch'].get('native', [])]
TX_DATA_BATCH = [__t['input'] for __t in td.TRANSACTIONS['batch'].get('fungible-token', []) + td.TRANSACTIONS['batch'].get('native', [])]
TX_DATA_RANDOM = [__t['input'] for __t in td.TRANSACTIONS['random'].get('any', [])]

# SELECTORS ###################################################################

def test_indicators_detect_transaction_calls_to_known_methods():
    assert any([iib.input_data_has_batching_selector(_d) for _d in TX_DATA_BATCH]) # not all live transaction have known selectors

def test_indicators_ignore_transaction_calls_to_random_methods():
    assert all([not iib.input_data_has_batching_selector(_d) for _d in TX_DATA_RANDOM])

# INPUT DATA ##################################################################

def test_indicators_detect_arrays_in_input_data():
    assert(any([iib.input_data_has_array_of_addresses(data=_d, min_length=4) for _d in TX_DATA_BATCH])) # not all batch transactions have input data
    assert(any([iib.input_data_has_array_of_values(data=_d, min_length=4) for _d in TX_DATA_BATCH])) # not all batch transactions have input data

def test_indicators_ignore_other_data_types():
    assert(any([not iib.input_data_has_array_of_addresses(data=_d, min_length=4) for _d in TX_DATA_RANDOM])) # some random transactions have input arrays too
    assert(any([not iib.input_data_has_array_of_values(data=_d, min_length=4) for _d in TX_DATA_RANDOM])) # some random transactions have input arrays too

# EVENTS ######################################################################

# TRANSFERS ###################################################################
