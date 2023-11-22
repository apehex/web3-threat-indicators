# Changelog

## v0.1.19

### Changes

- account for compiler optimization in the red-pill regex

## v0.1.17 - v0.1.18

### Additions

- analyse all traces at once

## v0.1.16

### Additions

- detect red-pill contracts on creation

## v0.1.12 - v0.1.15

### Changes

- parse event logs without any input ABI

### Additions

- index common ABIs / events
- check event constraints on tokens

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
