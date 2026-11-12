# Plano — Mensuração de sessões de agentes


## Arquitetura e implementação

Uma skill nova em agent-engineering mantém procedimento e referência local. Asset `assets/session-lens/` contém runtime do plugin original, sem testes/scripts de manutenção upstream, com subset de runtime completo. Metadados/sources.lock/imports em manifesto permitem reconstrução; overrides guardam as adaptações nos mesmos caminhos. Nenhum hooks.json do domínio é alterado: o asset só carrega se explicitamente passado ao cliente.

1. Ler fonte fixada e licença, mapear efeitos de FS/processos/SDK e precificação.
2. Registrar fonte e chave hook detectada por `tools.inventory.build.kind_of`, sem executar upstream; associar a capacidade dona.
3. Copiar arquivos runtime necessários, remover dependência automática e ações de relatório/configuração, atualizar rates, registrar overrides e proveniência completa.
4. Criar testes sintéticos de aritmética/deduplicação e revisão de limites; validar plugin nativo estaticamente e pacote sem cliente ao vivo.
5. Reconstruir metadados, rodar gates, comparar recursos importados/overrides e preparar publicação para aprovação específica.

Os testes de runtime puro usam apenas o subconjunto revisado e fixtures sintéticas, sem engine de Claude, rede ou dados pessoais. Uma sessão real só será iniciada se seu alvo/efeito/custo forem aprovados.
