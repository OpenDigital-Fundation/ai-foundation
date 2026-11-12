# Spec — Aprender e ensinar

- **Domínio:** education
- **Status:** implementado e verificado localmente; publicação pendente
- **Baseline:** main `9813abf`, 137 artefatos em 33 domínios.
- **Fronteira:** aprendizagem humana, facilitação de ensino, desenho instrucional e avaliação da aprendizagem. Memória de agentes pertence a agent-engineering; modelos de aprendizado de máquina a ai-engineering; pesquisa bibliográfica a research.

## Requisitos

Criar quatro capacidades experimentais, sem persona nem marca no nome:

| ID | Resultado e limite |
|---|---|
| `education/learn` | Plano de estudo pessoal e tutoria adaptada às tentativas do aprendiz; não treinamento de modelos. |
| `education/teach` | Condução de uma aula ou sessão com modelagem, prática guiada, participação e checagens; cursos completos vão para instructional-design. |
| `education/instructional-design` | Desenho reverso de unidade/curso, objetivos observáveis, Bloom revisada e alinhamento objetivo–evidência–atividade. |
| `education/learning-assessment` | Diagnóstico, itens, rubricas, feedback e revisão de evidência; não certificação ou notas oficiais autônomas. |

Usar conteúdo procedural original em inglês com leituras externas citadas, sem importar gráficos, tabelas, templates ou texto de licença não permissiva. Bloom é ferramenta de classificação de tarefas, não medida de inteligência, escala de domínio ou sequência obrigatória. Distinguir processo cognitivo de tipo de conhecimento. Combinar recuperação ativa, espaçamento, exemplos resolvidos, autoexplicação, prática com apoio progressivamente reduzido, aprendizagem por problemas/projetos quando adequada e reflexão metacognitiva. Distinguir pressuposto de projeto de eficácia comprovada. Evitar estilos fixos de aprendizagem e cronogramas universais.

## Aceite

- Uma entrada por capacidade no manifesto editorial; plugin, domínio, ADR, facetas, profile e índices coerentes.
- SKILL.md curto com referências locais autocontidas; nenhum caminho cruzado entre plugins ou helper ausente.
- Cinco gatilhos positivos e cinco negativos por skill, incluindo as vizinhas; dois casos sintéticos de tarefa por skill, marcados como não executados.
- Testes e validador existentes passam; reconstrução dos índices estável e quatro adaptadores contêm as novas entradas/referências.
- Publicação e limpeza somente mediante aprovação específica do lote preparado.

## Fora de escopo

Executar avaliações pagas, instalar plugins nos clientes, usar dados reais de alunos, prometer eficácia educacional ou conceder credenciais, notas e diagnósticos individuais.
