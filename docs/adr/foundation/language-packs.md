# Pacotes de linguagem em vez de artefatos por linguagem
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

O ECC tem, por linguagem, reviewer (agent), build-resolver (agent), testing (skill), patterns (skill), security (skill), verification (skill), commands `*-review`, `*-test`, `*-build` e rules — perto de 80 artefatos que repetem os mesmos procedimentos genéricos com detalhes da linguagem.

## Decisão

Cada linguagem tem uma única skill no domínio `languages` (ex.: `typescript`, `python`, `go`, `rust`, `jvm`, `swift`, `dart`, `dotnet`, `cpp`, `php`, `ruby`), com `references/` para padrões, testes, segurança, build e frameworks, e rules próprias. Procedimentos genéricos (TDD, review, debugging, auditoria) ficam nos seus domínios e carregam a referência da linguagem.

## Consequências

- Correções de procedimento são feitas uma vez só.
- A skill genérica precisa de uma instrução clara de "carregue `languages/<x>/references/<tópico>.md` se existir".
