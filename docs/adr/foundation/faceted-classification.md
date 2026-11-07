# Classificação por facetas sobre a posse por domínio

- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

Cada artefato pertence a exatamente um domínio, que é também o plugin instalável e a unidade da regra "uma capacidade, um artefato". Isso funciona para instalar e deduplicar, mas não para encontrar: uma skill de revisão de contratos é ao mesmo tempo direito, análise documental, LegalTech e segurança. A taxonomia "OpenDigital AI & Knowledge Landscape" propõe seis dimensões independentes (tecnologia, conhecimento, capacidade, setor, tipo de recurso, maturidade) com IDs estáveis e mapeamentos para classificações externas.

## Decisão

- O domínio continua sendo o dono único do artefato (plugin, unicidade, spec).
- Cada artefato recebe facetas N:N: `technology`, `knowledge`, `capabilities`, `industries`. `resource_type` é o `type` do catálogo; `maturity` deriva de `status`, licença e proveniência.
- Os vocabulários ficam em `catalog/taxonomy/*.yaml`, com IDs em inglês (kebab-case) independentes dos nomes, nomes em pt-BR e en, `parent` opcional e mapeamentos externos (IPL, ISCED, ESCO, O*NET, ISIC, CNAE) separados dos IDs internos.
- As facetas de cada artefato ficam em `catalog/facets.yaml`; o validador exige que todo artefato tenha facetas e que todo ID exista no vocabulário.
- O registro de recursos externos (repositórios, modelos, datasets, MCPs de terceiros) é um produto separado, `opendigital-ai-landscape`, com repositório próprio; ele consome estes vocabulários e o catálogo deste repositório.

## Consequências

- Navegação por qualquer dimensão (índices gerados), sem alterar plugins nem a regra de unicidade.
- Os vocabulários passam a ser contrato entre repositórios: mudanças de ID exigem ADR; nomes podem mudar livremente.
- Mapeamentos externos só entram com código verificado na fonte oficial; não se inventam códigos.
