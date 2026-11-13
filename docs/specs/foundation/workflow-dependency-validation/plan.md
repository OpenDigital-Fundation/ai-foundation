# Plano — Dependências de workflows

## Implementação

1. Trocar somente os 12 pins existentes pelos SHAs conferidos nos cinco PRs.
2. Criar helper stdlib em tools/build/artifact_smoke.py com pack e verify: quatro ZIPs, manifesto SHA-256/quantidade, cópia do próprio verificador e limites de estrutura/tamanho; nunca extrair ou executar pacotes.
3. Testar com árvore sintética pequena e casos adversariais. A verificação de CI usa os quatro adaptadores reais gerados do catálogo, inclusive arquivos ocultos de recursos.
4. Acrescentar workflow dependency-smoke com os cinco novos pins; primeiro job produz o artefato, segundo baixa e executa apenas o verificador. O segundo job não recebe credenciais extras nem permissões de escrita.
5. Integrar localmente ao lote de capacidades já verificado em branch própria, mantendo todos os commits assinados; testar o conjunto, apresentar SHA/destino para aprovação e só então obter evidência do serviço Actions.

## Contratos

O manifesto tem versão, quantidade esperada de entradas e exatamente os quatro nomes de pacote; cada ZIP tem um diretório raiz próprio e quantidade exata de SKILL.md nas posições públicas do adaptador. Caminhos absolutos, backslashes, duplicados e .. são recusados. A comparação SHA protege a transferência, não autentica código de uma origem arbitrária; o verificador é código do próprio PR, sob o mesmo escopo de confiança e permissões de leitura da CI normal.

A instalação padrão usa Python 3.12 e Node 22, enquanto o runtime das Actions é Node 24. Não confundir esses contratos. Não mudar gates de release ou run-evals para conseguir uma check verde.
