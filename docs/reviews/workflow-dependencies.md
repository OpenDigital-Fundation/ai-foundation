# Revisão — Dependências de workflows

- **Baseline:** main 9813abf; PRs #2–#6 reconferidos abertos, heads sem alteração em 2026-11-12.
- **Implementado localmente:** cinco versões propostas com SHA fixado em 12 usos existentes e cinco usos no smoke. Inputs conferidos contra action.yml dos commits oficiais; os quatro workflows existentes preservam a semântica além dos pins.
- **Verificado:** seis testes stdlib de empacotamento/integridade passaram; roundtrip local de quatro ZIPs reais, 140 skills/workflows em cada, transportou também o verificador stdlib e preservou arquivos ocultos. O conjunto real usado é o adaptador da candidata local de capacidades 2aedd36; a branch de dependências continua baseada em 9813abf até integração local.
- **Compatibilidade:** Actions Node 24; runner da main observado em log 2.338.2. Projeto Python 3.12 e Node 22 continuam iguais; setup-node do smoke não ativa cache automático de gerenciador.
- **Limites:** nenhum upload/download real do serviço Actions, avaliação paga ou release foi executado. As checks antigas de PR não cobrem os novos runtimes de setup-node/upload/download. O smoke novo exercita os cinco pins com contents:read, timeout e retenção de um dia, sem secrets e sem checkout no job de download. Esse job executa o verificador do próprio PR transportado no artefato, com o mesmo nível de confiança da CI comum; ele não extrai nem executa conteúdo dos ZIPs.

Publicação, integração na main e eventual fechamento dos cinco PRs ficam sujeitos à aprovação específica do alvo conjunto e à CI verde. Nenhuma ação de merge/close foi tomada nesta revisão.
