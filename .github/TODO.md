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
[ ] specify typings

## Parsing

[x] operate on bytecode instead of assembly
[x] split creation data into: creation bytecode + runtime bytecode + args
[x] move interfaces in `token.py` to the ABI tests

## Metrics

[ ] metamorphic contracts
    [ ] when a trace is identified, also label the sibling traces & related entities:
        [ ] mutant deployment => implementation deployment + factory.getImplementation
        [ ] factory deployment => deployer
    [ ] new init code: return implementation code from the factory => instead of calling `getImplementation()`, the init code directly calls `getBytecode`
    [ ] selector wordlist?
    [ ] `is_bytecode_metamorphic_init_code` => `HAS_bytecode_metamorphic_init_code`: equality vs inclusion => broader
[ ] event poisoning
    [x] erc-20
    [x] erc-721
    [ ] erc-1155
    [ ] erc-1967
[x] red pill contracts
[ ] scan ALL the data:
    [ ] for example, the metamorphic init code can be in: the factory creation bytecode, the factory runtime bytecode, the mutation input data, yet another contract...
    [ ] the implementation address can be retrieved from the factory or another contract
    [ ] etc

## Testing

[ ] test on cryo data
[x] pickle dataset:
    [x] metamorphic tx
    [ ] metamorphic traces
[ ] modules:
    [ ] indicators
        [ ] batch
        [ ] events
        [ ] generic
        [ ] metamorphic
        [ ] proxy
        [ ] token
        [ ] wordlists
    [ ] metrics
        [ ] batch
        [ ] evasion
        [ ] generic
        [ ] normal
        [ ] probabilities
    [ ] parsing
        [ ] abi
        [ ] balances
        [ ] bytecode
        [ ] events
        [ ] inputs
    [ ] scraping
        [ ] bytecode
    [ ] utils
