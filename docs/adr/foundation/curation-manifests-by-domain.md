# Manifestos de curadoria por domínio

- **Status:** aceito na implementação; revisão e integração local solicitadas pelo usuário em 2026-11-07
- **Data:** 2026-11-07
- **Domínio:** foundation

## Contexto

A revisão estrutural da baseline 908ad6c identificou mistura de entradas editoriais com resultados gerados e convenções internas importadas de fontes distintas. O repositório precisa de fronteiras verificáveis sem alterar a instalação seletiva por domínio.

## Decisão

Cada domínio tem um manifesto em catalog/curation/domains/<domain>.yaml. Ele é a fonte de seus registros e receitas. Exclusões editoriais têm arquivo próprio; catálogo e exclusões públicos são projeções. Dados operacionais ficam em catalog/inventory/. Não há resultado intermediário de decisão para editar.

## Consequências

A posse editorial acompanha o plugin e as specs. Reconstrução não depende da ordem de lotes históricos. Mais informação fica em cada manifesto, mas metadados, receita e importações têm campos distintos. Mudanças em manifests são validadas antes de escrever saídas.
