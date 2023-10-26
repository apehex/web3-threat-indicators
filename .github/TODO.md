## Packaging / Tidying

[x] publish to PyPI
[x] import the code from my bots
[x] split the modules:
    [x] current metrics into metrics + indicators
    [x] update import paths
    [x] update tests
[ ] rm web3 deps
[x] replace options with default values
[x] use modules in bots
[x] option to set the LRU cache size

## Parsing

[x] operate on bytecode instead of assembly
[ ] split creation data into: creation bytecode + runtime bytecode + args
[x] move interfaces in `token.py` to the ABI tests

## Metrics

[ ] metamorphic contracts
    [ ] when a trace is identified, also label the sibling traces & related entities:
        [ ] mutant deployment => implementation deployment + factory.getImplementation
        [ ] factory deployment => deployer
[ ] red pill contracts
[ ] event poisoning
[ ] scan ALL the data:
    [ ] for example, the metamorphic init code can be in: the factory creation bytecode, the factory runtime bytecode, the mutation input data, yet another contract...
    [ ] the implementation address can be retrieved from the factory or another contract
    [ ] etc

## Testing

[ ] test on cryo data
[ ] pickle dataset:
    [ ] metamorphic tx
    [ ] metamorphic traces
