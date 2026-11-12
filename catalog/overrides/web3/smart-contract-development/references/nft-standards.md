# nft-standards — reviewed procedure

Adapted by OpenDigital from `wshobson/agents` at `9c61ab2`, `plugins/blockchain-web3/skills/nft-standards/SKILL.md#metadata-standards,royalties-eip-2981`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Declare the token interface and metadata schema separately from artwork storage and licensing. Check token identity, metadata availability/integrity, optional fields and access/update policy. Preserve source/content rights when using remote or content-addressed assets.

For royalty information, confirm the target interface/version and calculate in explicit units with reviewed rounding and authorization for changes. [ERC-2981](https://eips.ethereum.org/EIPS/eip-2981) provides royalty information; it does not itself force a marketplace to pay it. Validate interface detection and edge sale amounts against the actual contract. No incomplete ERC721/Base64 sample or live mint/deployment command is bundled here.
