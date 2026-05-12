# Relatório de Refatoração e Otimização - Projeto UAB

## 1. Mudanças Realizadas

### 1.1 Modularização Arquitetural
- **Extensions Pattern**: Criado `app/extensions.py` para centralizar as instâncias das extensões do Flask (SQLAlchemy, Migrate, Caching, APScheduler). Isso elimina o risco de imports circulares e melhora a organização.
- **Service Layer Expansion**: A lógica de negócio foi movida das rotas (controllers) para os serviços em `app/services/`. Exemplos:
  - `evento_service.py`: Centraliza criação, listagem por perfil e validação de conflitos.
  - `relatorio_service.py`: Centraliza o cálculo de estatísticas para dashboard e relatórios.

### 1.2 Otimização de Performance
- **Cache de Dados**: Implementado **Flask-Caching** (FileSystemCache) no serviço de relatórios.
  - Estatísticas do Dashboard agora são cacheadas por 5 minutos.
  - Invalidação automática de cache ocorre após criação, deleção ou mudança de status de eventos.
- **Processamento Assíncrono (Jobs)**: Implementado **Flask-APScheduler** para tarefas de manutenção.
  - Adicionado job `cleanup_orphan_files` que roda a cada 24 horas para remover arquivos na pasta `uploads` que não possuem referência no banco de dados.

### 1.3 Simplificação de Código
- **Rotas mais enxutas**: As rotas agora focam apenas no tratamento de requisições, delegando a complexidade para a camada de serviços.
- **Tratamento de Transações**: Padronização do uso de `try/except` com `db.session.rollback()` em todos os serviços de escrita.

## 2. Impacto nos Testes
- Adicionado `tests/integration/test_optimization.py` para validar a funcionalidade do cache e sua invalidação correta.
- Todos os 19 testes existentes (incluindo regressão) passaram com 100% de sucesso.
- Cobertura de código mantida acima de 80%.

## 3. Próximos Passos Sugeridos
- Utilizar Redis como backend de cache em ambiente de produção para maior performance.
- Expandir a camada de serviços para incluir notificações por e-mail em background após aprovações.
