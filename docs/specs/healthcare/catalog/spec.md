# Spec — Tecnologia e apoio clínico em saúde

- **Domínio:** healthcare
- **Status:** em implementação
- **Demanda:** solicitação explícita do mantenedor em 2026-11-11.
- **Decisão:** [ADR do domínio](../../../adr/foundation/healthcare-domain.md)

## Fronteira

Sistemas e interoperabilidade de saúde, preparação de evidência para profissionais e documentação clínica rastreável. Dados biomédicos para pesquisa continuam em science; revisão de literatura genérica em research; privacidade jurídica em legal-compliance.

## Capacidades

- `healthcare/health-informatics` — Sistemas de prontuário, interoperabilidade, fluxos CDS e verificação de dados de saúde.
- `healthcare/clinical-evidence` — Perguntas clínicas, evidência atual e verificável, limites de aplicação e revisão profissional.
- `healthcare/clinical-documentation` — Minutas clínicas baseadas somente em fatos fornecidos e fontes verificadas, com revisão e assinatura profissional.

## Requisitos

- **R1.** Uma entrada por capacidade, nomes sem marca, procedimento executável em inglês e referências privadas por ferramenta/tema. Não duplicar donos existentes.
- **R2.** Reabrir as decisões relevantes do inventário fixado, somente após leitura do conteúdo e licença efetiva; registrar fonte, commit, caminho e modificação por arquivo.
- **R3.** Só copiar MIT, Apache-2.0 ou BSD. Texto restrito, desconhecido ou materiais proprietários ficam somente como link; uma biblioteca citada não transfere sua licença ao texto do guia.
- **R4.** Separar capacidade genérica de procedimento do harness de origem. Remover instalação remota, versões flutuantes executáveis, helpers não incluídos e aplicação de mudanças sem autorização.
- **R5.** Manter receita, supersedes, exclusões, facetas, plugin, catálogo e índices coerentes. Procedimentos gerais de outros domínios são referenciados, não copiados como nova capacidade.
- **R6.** Publicar como experimental; escrever casos de roteamento e de fronteira sem afirmar que avaliações de modelo foram executadas.

## Contrato clínico e de dados

- Apoio a profissionais e minutas revisáveis, sem diagnóstico, prescrição ou alteração autônoma de prontuário. Não criar doses, achados, códigos, resultados ou referências ausentes da entrada.
- Separar fatos, hipóteses, evidência publicada e decisão do profissional; registrar data, população, limitações e versão das fontes. Evidência não localizada permanece explicitamente não localizada.
- Dados reais de pacientes exigem autorização e ambiente apropriado; fixtures e exemplos usam dados sintéticos. Não enviar dados clínicos a serviços externos por padrão.
- Interoperabilidade declara versão FHIR e perfil local; conformidade de schema não significa segurança clínica. Regulação depende da função e jurisdição; não declarar certificação.
- Fontes primárias para a revisão de risco: [OMS](https://www.who.int/publications/i/item/9789240084759), [FDA CDS, janeiro de 2026](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software), [FHIR R4, versão explícita](https://hl7.org/fhir/R4/overview.html). São referências externas, sem copiar seu texto/licença.

## Critérios de aceite

1. Todas as capacidades acima têm procedimento próprio, fontes selecionadas e links válidos.
2. Nenhuma chave é decidida duas vezes; decisões reabertas têm motivo verificável.
3. Reconstrução do domínio repetida sem diferença, validador 0/0 e suíte de tooling verde.
4. Revisão estática de comandos, licenças e limites registrada antes da aprovação de publicação.

## Fora de escopo

Executar código upstream, instalar produtos em máquinas reais, alterar sistemas externos, publicar sem aprovação específica, avaliações pagas ou certificação profissional/operacional.
