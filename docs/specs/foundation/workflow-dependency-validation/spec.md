# Spec — Verificação conjunta de dependências dos workflows

- **Domínio:** foundation
- **Data:** 2026-11-12
- **Baseline:** main 9813abf; cinco PRs Dependabot abertos (#2–#6), heads reconferidos sem alteração.

## Resultado

Atualizar as 12 referências existentes às cinco Actions propostas, com SHA imutável: setup-node 7.1.0, setup-uv 10.3.3, checkout 7.0.1, upload-artifact 7.0.2 e download-artifact 8.0.2. Metadados oficiais dos pins foram revisados; usam Node 24 e o runner observado da main (2.338.2) satisfaz o mínimo documentado. Manter gates de release por tag e de avaliações pagas por acionamento explícito.

## Problema verificável

As checks verdes dos PRs não exercitam setup-node/upload/download porque evals é pulado em PR normal e release só roda por tag. Portanto, adicionar um smoke de PR sem release/modelos: instalar runtimes com os novos pins, construir quatro adaptadores reais, empacotar, transferir pelo upload/download e conferir hashes, estrutura e quantidade de entradas.

## Aceite

- Todos os usos ficam fixados por SHA oficial; inputs atuais compatíveis são preservados.
- Smoke com pull_request e workflow_dispatch, permissions contents:read, timeout limitado, nenhum secret ou API de modelo, sem tag/release/push/issue.
- Download em job separado sem checkout; verificador stdlib transportado no mesmo artefato, sem dependências instaladas no segundo job. Ele lê os ZIPs sem extrair/executar seu conteúdo e verifica integridade/estrutura/contagem.
- Testes locais cobrem roundtrip real, alteração de bytes, pacote ausente, caminho que escapa e contagem incompatível. O helper não sobrescreve saída existente.
- Verificar contrato YAML contra metadados oficiais e revisar eventos/permissões. A transferência no serviço Actions só é considerada executada depois da publicação aprovada e CI correspondente verde.

## Fora de escopo

Release real, avaliações pagas, atualização do CLI Claude, instalação global local, fechamento dos PRs ou publicação/merge sem aprovação específica.
