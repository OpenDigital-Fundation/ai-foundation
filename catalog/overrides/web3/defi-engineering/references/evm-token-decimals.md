# evm-token-decimals — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/evm-token-decimals/SKILL.md#how-it-works,rules`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Identify an asset by chain ID and contract address, not symbol. Obtain and validate decimals from an authorized read or verified configuration; handle optional, reverting or malformed metadata explicitly instead of assuming 18 or retrying indefinitely.

Use integer/decimal-safe arithmetic, record input/output units and rounding, and bound scaling operations. Cache metadata with its chain/address and verification context; reconsider wrappers, upgrades and bridges. Test heterogeneous decimals, edge amounts and conversion round trips. A normalized WAD value is an internal representation, not proof that tokens are economically equivalent.
