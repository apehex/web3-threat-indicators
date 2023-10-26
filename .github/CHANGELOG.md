# Changelog

## v0.1.11

### Changes

- add `0` padding to the left of HEX bytecode when normalizing so that it has a pair length => full bytes

## v0.1.10

### Fixes

- fixed typo that made the indicator `bytecode_has_known_metamorphic_init_code` always succeed

### Changes

- improved creation bytecode parsing

### Additions

- added metrics for mutant contract deployment & destruction
- added metrics for metamorphic factory deployment
- improved parsing of the input data for contract creations
