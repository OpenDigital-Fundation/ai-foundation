# Tarefas — Curadoria das fontes

- [x] **T1.** Escrever `catalog/sources.lock.yaml` com as 14 fontes da spec. Verificar: valida no schema.
- [x] **T2.** Portar `inventory.py` e `classify.py` para `tools/inventory/` com `fetch.sh`. Verificar: rodar a partir do lock reproduz `inventory.csv` byte a byte.
- [x] **T3.** Escrever `THIRD_PARTY_NOTICES.md` com as fontes `merge` e o texto de licença de cada uma.
- [x] **T4.** Escrever o schema de `PROVENANCE.yaml`. Verificar: exemplo do plano valida.
- [x] **T5.** Criar verificação de CI que compara hashes de arquivos do repositório com os arquivos das fontes `reference` e falha se houver cópia.
- [ ] **T6.** Triar os 27 itens `unclassified` do inventário (atribuir domínio ou `exclude`).
