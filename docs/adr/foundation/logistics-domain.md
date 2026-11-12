# Domínio `logistics` para logística e cadeia de suprimentos

- **Status:** aceito para implementação local
- **Data:** 2026-11-11
- **Domínio:** foundation

## Contexto

O ROADMAP mantinha este nicho fora do escopo por ausência de demanda. O mantenedor solicitou expressamente sua incorporação. O catálogo atual não tem um dono que cubra sua intenção especializada sem atravessar fronteiras.

## Decisão

Criar `logistics` com as capacidades da [spec](../../specs/logistics/catalog/spec.md). Planejamento de suprimentos e operação física de transporte, exceções, transportadoras, estoque e logística reversa. Gestão de projeto genérica fica em operations; segurança de dependências de software não é logística. Frameworks e produtos pertinentes aparecem como referências privadas, mantendo os nomes públicos sem marca; esse recorte não reabre integrações comerciais sem relação com a capacidade.

## Consequências

Uma capacidade continua tendo um único dono. O inventário é reavaliado de forma explícita, sem importar cegamente tudo que correspondia a uma palavra-chave. O conteúdo depende de licença permissiva, proveniência e revisão. O domínio permanece experimental até avaliações próprias de tarefa e gatilho.
