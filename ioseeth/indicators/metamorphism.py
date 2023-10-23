"""Generic indicators for smart contracts."""

import ioseeth.parsing.bytecode

# KNWON #######################################################################

INIT_CODES = (
    '5860208158601c335a63aaf10f428752fa158151803b80938091923cf3')

# OPCODES #####################################################################

def bytecode_has_known_metamorphic_init_code(bytecode: str) -> bool:
    """Check whether the creation bytecode contains known init code to setup metamorphic contracts."""
    return any(__i in bytecode for __i in INIT_CODES)
