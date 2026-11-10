# Licença do repositório e proveniência
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

As fontes são majoritariamente MIT/Apache-2.0, mas há exceções: `docx`, `pdf`, `pptx`, `xlsx` da Anthropic são proprietárias; `agent-pentester` (Shannon) é AGPL-3.0; os checklists da SecurityStandards são CC BY-NC-SA 4.0 (veda uso comercial); `security-standards` não declara licença.

## Decisão

- O repositório é **MIT**, com `THIRD_PARTY_NOTICES.md` para as fontes MIT e Apache-2.0 (Apache exige preservar avisos e marcar modificações).
- Só se copia ou funde conteúdo de licença permissiva.
- AGPL, NC, proprietário e sem licença entram só como **referência** (link + descrição própria), por exemplo uma skill que orienta a instalar o Shannon ou as skills de documentos da Anthropic separadamente.
- Todo arquivo derivado tem entrada em `PROVENANCE.yaml`, e o CI bloqueia cópia por hash.

## Consequências

- Uso comercial seguro pela OpenDigital.
- Algumas capacidades (Office, pentest autônomo) dependem de instalação externa.
