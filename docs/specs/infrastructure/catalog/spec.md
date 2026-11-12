# Spec — Homelab e redes

- **Domínio:** infrastructure
- **Status:** em implementação
- **Demanda:** solicitação explícita do mantenedor em 2026-11-11.
- **Decisão:** [ADR do domínio](../../../adr/foundation/infrastructure-domain.md)

## Fronteira

Infraestrutura de rede e laboratórios auto-hospedados: conectividade, segmentação, DNS, VPN, hardware, recuperação e operação local. CI/CD, deploy de aplicações e SRE genérico continuam em platform.

## Capacidades

- `infrastructure/network-operations` — Inventário, diagnóstico e revisão de redes, roteamento, segmentação, DNS e VPN.
- `infrastructure/homelab-operations` — Planejamento e operação de serviços auto-hospedados, armazenamento, acessos, backups e recuperação.

## Requisitos

- **R1.** Uma entrada por capacidade, nomes sem marca, procedimento executável em inglês e referências privadas por ferramenta/tema. Não duplicar donos existentes.
- **R2.** Reabrir as decisões relevantes do inventário fixado, somente após leitura do conteúdo e licença efetiva; registrar fonte, commit, caminho e modificação por arquivo.
- **R3.** Só copiar MIT, Apache-2.0 ou BSD. Texto restrito, desconhecido ou materiais proprietários ficam somente como link; uma biblioteca citada não transfere sua licença ao texto do guia.
- **R4.** Separar capacidade genérica de procedimento do harness de origem. Remover instalação remota, versões flutuantes executáveis, helpers não incluídos e aplicação de mudanças sem autorização.
- **R5.** Manter receita, supersedes, exclusões, facetas, plugin, catálogo e índices coerentes. Procedimentos gerais de outros domínios são referenciados, não copiados como nova capacidade.
- **R6.** Publicar como experimental; escrever casos de roteamento e de fronteira sem afirmar que avaliações de modelo foram executadas.

## Critérios de aceite

1. Todas as capacidades acima têm procedimento próprio, fontes selecionadas e links válidos.
2. Nenhuma chave é decidida duas vezes; decisões reabertas têm motivo verificável.
3. Reconstrução do domínio repetida sem diferença, validador 0/0 e suíte de tooling verde.
4. Revisão estática de comandos, licenças e limites registrada antes da aprovação de publicação.

## Fora de escopo

Executar código upstream, instalar produtos em máquinas reais, alterar sistemas externos, publicar sem aprovação específica, avaliações pagas ou certificação profissional/operacional.
