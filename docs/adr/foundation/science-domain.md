# Domínio `science` para pesquisa científica computacional
- **Status:** proposto
- **Data:** 2026-11-10
- **Domínio:** foundation

## Contexto

A fatia 4 da expansão de fontes traz `K-Dense-AI/claude-scientific-skills` (177 skills) e as cópias de parte dela em `davila7/claude-code-templates`. São guias por biblioteca ou base de dados (Scanpy, RDKit, Qiskit, PyMC, pydicom…) para trabalho científico: ômica, química, simulação, estatística de estudos, escrita científica, imagem biomédica e automação de laboratório. Nenhum domínio atual é dono disso: `research` cobre pesquisa com fontes e revisão de literatura, `data` cobre bancos e engenharia de dados, `ai-engineering` cobre ML aplicado a produtos.

## Decisão

Criar o domínio `science` com sete capacidades: `bioinformatics`, `cheminformatics`, `scientific-computing`, `experimental-design`, `scientific-writing`, `biomedical-data` e `lab-automation`. Como nos pacotes de linguagem, cada capacidade é uma skill com procedimento próprio e `references/<biblioteca>/` para os guias de cada ferramenta; não há uma skill por biblioteca. Revisão de literatura e citações continuam em `research`; ML genérico (scikit-learn, SHAP) em `ai-engineering/ml-engineering`; documentos e diagramas em `documents`.

Uso clínico (apoio à decisão clínica, planos de tratamento, laudos) fica fora: é uso regulado e exige spec própria com revisão de risco.

## Consequências

- Uma busca por "single-cell" ou "docking" encontra uma skill, não dezenas.
- As referências por biblioteca podem crescer sem criar artefatos; cada uma registra origem e licença.
- Skills cuja licença declarada não é permissiva, ou é ambígua entre a ferramenta e o texto, entram só como link.
- O domínio precisa de evals de gatilho próprios antes de sair de `experimental`.
