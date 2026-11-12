# Revisão dos domínios especializados solicitados

- Data: 2026-11-11
- Responsável: Codex
- Baseline: main 7d840dc4ba2c00315d4aca89a46c80fb4e733e52 (PR #7)
- Estado: implementado e testado localmente; publicação depende da aprovação do commit exato.

## Entrega

O catálogo passa de 123 para 137 artefatos experimentais e de 26 para 33 domínios. São 14 novas skills e sete perfis de instalação. Cada domínio tem uma spec, um plano, tarefas e um ADR próprios. A seleção reabre 46 chaves upstream de licença MIT em cinco fontes já fixadas, com proveniência por arquivo; não houve nova fonte ou execução de código upstream.

| Domínio | Capacidades |
|---|---|
| games | game-design; game-engineering |
| geospatial | geospatial-analysis; geospatial-engineering |
| extended-reality | immersive-development |
| healthcare | health-informatics; clinical-evidence; clinical-documentation |
| web3 | smart-contract-development; defi-engineering |
| infrastructure | network-operations; homelab-operations |
| logistics | supply-chain-planning; logistics-operations |

GeoPandas já pertence a science/scientific-computing: o novo domínio reutiliza esse dono pelo perfil e referências, sem outra cópia. ETL e ML genéricos permanecem em data/ai-engineering; auditoria em security; deploy/SRE em platform; gestão genérica em operations. O recorte de importação é a matriz vertical-domains-curation.yaml, não uma afirmação de que todo perfil upstream desses setores foi incorporado.

## Achados confirmados e adaptações

| Prioridade | Evidência de origem | Correção no conteúdo incorporado |
|---|---|---|
| Alto — afirmações clínicas superestimadas | Clinical Evidence Agent associa revisão/publicação a uso de alegações sem qualificação; healthcare-reviewer exige ausência de falsos negativos | Ledger de alegações com aplicabilidade, incerteza e revisão; validação baseada em risco, sem garantia automática de eficácia, segurança ou conformidade |
| Alto — helpers não incluídos | clinical-reports e treatment-plans apontam para geradores/validadores/assets locais da fonte | Referências adaptadas a procedimento manual; manifestos vazios originais, sem mandar executar arquivos ausentes |
| Alto — defaults operacionais e jurídicos sem contexto | carrier/exception/returns trazem prazos, percentuais, responsabilidade e destinação como regras gerais | Verificar contrato, jurisdição, produto e política; retirar valores e regras universais; exigir aprovação para reembolso, descarte e compromissos |
| Médio — rede aplicava mudanças na triagem | Pi-hole inclui allow-list/restart; WireGuard inclui restart; VLAN sugere ping como prova de isolamento e há conflito home.lan/home.arpa | Primeira fase somente leitura; mudanças autorizadas separadamente; testar fluxos permitidos/proibidos e IPv6; nome residencial ancorado em RFC 8375 |
| Médio — amostras Web3 incompletas | web3-testing tem variáveis/contrato ausentes e testFail legado; nft-standards depende de helpers omitidos | Plano de testes contra ABI/toolchain reais, sem exemplo falsamente executável, fork pago ou transação real automática |
| Médio — números e regras de engine como universais | Perfis impõem limites/tamanhos/estilos e alvos fixos de FPS; GIS promete precisão com GCP | Validar versão, hardware e carga; preservar método de medição e pontos de verificação independentes, sem garantias universais |
| Baixo — perfis XR só listavam escopo | Três perfis What You Can Do e um perfil nativo focado em branding/versão | Quatro exclusões low-quality com motivo; procedimento próprio e uma referência vr-ar adaptada, com orçamento por dispositivo |

## Verificação

- 190 testes de tooling passaram; validador: zero erros/zero avisos.
- Duas reconstruções dos sete domínios e índices: zero alteração na segunda, em 3.611 caminhos comparados por hash.
- 46 origens MIT: licença efetiva, caminho, commit do lock e modificação conferidos; nenhum script/asset upstream novo copiado.
- 5.442 chaves do inventário decididas exatamente uma vez: 1.481 incorporadas e 3.961 excluídas.
- Adaptadores Agent Skills, Cursor, Gemini e OpenCode gerados: 133 skills/workflows em cada projeção; não instalados em clientes reais.
- Casos escritos: 28 de roteamento; dois gatilhos positivos e um negativo por nova skill; sete tarefas clínicas sintéticas. Não foram executadas avaliações com modelos.
- A main e o original parcial de Claude permanecem preservados. Worktree própria: vertical-domains, branch matbrgz/vertical-domains; sem publicação durante a preparação.

## Fontes primárias consultadas

- Saúde: [OMS, governança de IA em saúde](https://www.who.int/publications/i/item/9789240084759), [FDA CDS, janeiro de 2026](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software), [HL7 FHIR R4](https://hl7.org/fhir/R4/overview.html). Referenciadas para revisão de risco e versão, sem copiar o texto nem inferir certificação.
- Redes: [RFC 8375](https://www.rfc-editor.org/rfc/rfc8375.html), para o namespace home.arpa.
- Web3: [ERC-2981](https://eips.ethereum.org/EIPS/eip-2981) e [considerações de segurança do Solidity](https://docs.soliditylang.org/en/latest/security-considerations.html); links informativos, sem copiar código GPL ou outro material restrito.
- XR: [WebXR, draft datado de 2026-11-09](https://www.w3.org/TR/2026/CRD-webxr-20261109/); o status do padrão não implica suporte universal.

## Limites e próximo gate

Esta é uma seleção editorial inicial por capacidade, com procedimentos próprios e adaptações revisadas. Perfis avançados, outras integrações e outras bibliotecas continuam sujeitos a suas decisões individuais. Não houve uso de dados de pacientes, avaliação clínica, transação financeira, alteração de rede, voo, instalação em agente real ou execução upstream. A publicação experimental não equivale a liberação para uso clínico ou produção.

O próximo gate é a aprovação específica do commit/destino, seguida de PR e CI. A limpeza de uma worktree futura exige outro lote específico; não faz parte do pedido de conteúdo.
