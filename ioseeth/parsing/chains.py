"""Metadata on the blockchains."""

import json
import os.path

import ioseeth.__utils as __utils

# DATA ########################################################################

with open(os.path.join(__utils.get_data_dir_path(), 'chains.json'), 'r') as __f:
    __chains = json.load(__f)
    NATIVE_TOKENS = {int(__v): __k for __v, __k in __chains.items()}
