# Revisão — Protótipo de supervisão orientada a eventos

- **Fonte:** deepseek-ai/dsh-superagent-prototype no commit 8c32a9dc5d72c033816c6a8110b37f40cf94fba4; MIT, única LICENSE na raiz, sem licença local diferente nas duas skills.
- **Universo:** README/licença, duas skills, seções selecionadas de 000/002/003; conteúdo de código/SETUP/pnpm não foi executado.
- **Decisão:** uma referência revisada no dono existente harness-design, sem novo artefato público; duas skills excluídas vendor-specific porque dependem do protocolo e identidades DSH. Não são falsos duplicate-of.

## Achados confirmados

1. README declara protótipo de pesquisa, não produto oficial nem código pronto para produção; a referência preserva esse limite e não confunde documento de design com recurso executado.
2. docs/003-execution.md, The Executor, descreve comandos sem aprovação como usuário do SO e diz que wrappers/diretórios não são fronteira de segurança. Esse default não é adotado; a adaptação exige enforcement real do host.
3. O merge depende de instruções, não de lógica específica no host; os defaults numéricos/contas do protótipo não substituem aprovação/CI/proteção de branch locais.
4. docs/002-authorization.md distingue entrega de contexto de autoridade, versão de política e revalidação na retomada; esses contratos são a contribuição incorporada, junto da posse de follow-ups e reconciliação de efeitos após restart.

## Evidência executada em 2026-11-13

Receita e overrides registram as três origens documentais e a licença. Três casos sintéticos são escritos, not-run; uma rota e aliases para dsh superagent/DeepSeek apontam ao dono. Preflight da receita harness-design passou contra os clones fixados; a adaptação/entrada/licença/casos conferem byte a byte com os overrides. Projeções foram reconstruídas duas vezes com hashes estáveis; 222 testes de ferramentas e 12 casos sintéticos do runtime passaram, e o validador retornou 0 erros/0 avisos. A busca local e a portátil nos quatro adaptadores localizaram harness-design para dsh superagent/DeepSeek; cada pacote contém 140 skills/workflows e a referência/licença. O roundtrip local dos quatro ZIPs confirmou hashes/estrutura/quantidades. Não houve instalação, conexão de contas ou validação operacional do protótipo; a CI real depende da publicação aprovada.
