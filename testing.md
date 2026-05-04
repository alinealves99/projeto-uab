# Plano de Testes - Projeto UAB
**Abordagem:** Test-Driven Development (TDD)
**Data:** 02/05/2026

## 1. Estratégia de Testes (TDD First)

Este projeto adota a metodologia **TDD First**, onde os testes são concebidos e implementados antes das funcionalidades correspondentes. O ciclo de desenvolvimento seguirá o padrão **Red-Green-Refactor**:

1.  **Red**: Criar um teste que falha para uma funcionalidade ainda não existente.
2.  **Green**: Implementar o código mínimo necessário para fazer o teste passar.
3.  **Refactor**: Melhorar o código mantendo a funcionalidade e garantindo que os testes continuem passando.

### Objetivos
- Garantir que todos os requisitos da especificação (`doc/03-especs.md`) sejam atendidos.
- Prevenir regressões durante a evolução do sistema.
- Validar rigorosamente o controle de acesso por perfis (Roles).

---

## 2. Cenários de Teste

### 2.1 Autenticação e Sessão
| Nome do Teste | Cenário (Dado/Quando/Então) | Tipo | Mocks/Notas |
| :--- | :--- | :--- | :--- |
| `test_login_valido` | **Dado** usuário cadastrado, **Quando** envia credenciais corretas, **Então** status 302 (redirect) e sessão criada. | Integração | DB (SQLite em memória) |
| `test_login_invalido` | **Dado** usuário cadastrado, **Quando** envia senha errada, **Então** exibe mensagem de erro e permanece no login. | Integração | - |
| `test_logout` | **Dado** usuário logado, **Quando** acessa `/logout`, **Então** sessão é limpa e redireciona para login. | Integração | - |

### 2.2 Controle de Acesso (@role_required)
| Nome do Teste | Cenário (Dado/Quando/Então) | Tipo | Mocks/Notas |
| :--- | :--- | :--- | :--- |
| `test_acesso_admin_permitido` | **Dado** usuário ADMINISTRADOR, **Quando** acessa `/events/create`, **Então** status 200. | Integração | Sessão mockada |
| `test_acesso_comum_negado` | **Dado** usuário CONSULTOR, **Quando** acessa `/events/create`, **Então** exibe flash "Acesso não autorizado" e status 302. | Integração | Sessão mockada |

### 2.3 Gestão de Eventos e Uploads
| Nome do Teste | Cenário (Dado/Quando/Então) | Tipo | Mocks/Notas |
| :--- | :--- | :--- | :--- |
| `test_criar_evento_valido` | **Dado** admin logado, **Quando** envia form completo com arquivo, **Então** evento criado com status PENDENTE. | Integração | Mock `salvar_arquivo` |
| `test_criar_evento_conflito` | **Dado** evento existente no mesmo horário, **Quando** tenta criar novo, **Então** falha com mensagem de conflito. | Integração | - |
| `test_upload_invalido` | **Dado** arquivo sem extensão permitida, **Quando** envia form, **Então** exibe erro de validação. | Unitário | Mock `storage` |
| `test_excluir_evento_admin` | **Dado** admin logado, **Quando** envia POST para delete, **Então** registro é removido do banco. | Integração | - |

### 2.4 Fluxo de Aprovação
| Nome do Teste | Cenário (Dado/Quando/Então) | Tipo | Mocks/Notas |
| :--- | :--- | :--- | :--- |
| `test_aprovar_evento` | **Dado** evento PENDENTE, **Quando** secretário aprova, **Então** status muda para DEFERIDO e data_decisao é salva. | Integração | - |
| `test_rejeitar_evento_com_justificativa` | **Dado** evento PENDENTE, **Quando** secretário rejeita com texto, **Então** status INDEFERIDO e justificativa salva. | Integração | - |
| `test_listar_indeferidos_autorizado` | **Dado** admin logado, **Quando** acessa `/events/indeferidos`, **Então** lista apenas eventos rejeitados. | Integração | - |

### 2.5 Relatórios
| Nome do Teste | Cenário (Dado/Quando/Então) | Tipo | Mocks/Notas |
| :--- | :--- | :--- | :--- |
| `test_gerar_dados_relatorio` | **Dado** 5 eventos cadastrados, **Quando** chama service de relatório, **Então** retorna contagem exata por status. | Unitário | DB (fakes) |

---

## 3. Dependências de Teste

Além das dependências base (`Flask`, `SQLAlchemy`), serão necessárias as seguintes bibliotecas:

```bash
# Instalação
pip install pytest pytest-flask coverage factory-boy pytest-mock
```

### Análise:
- **pytest**: Framework principal de execução.
- **pytest-flask**: Facilita o uso do cliente de teste do Flask e contextos de aplicação.
- **coverage**: Gera relatórios de cobertura de código.
- **factory-boy**: Para criação rápida de dados de teste (usuários e eventos).
- **pytest-mock**: Para isolar chamadas de sistema (ex: salvar arquivos no disco).

---

## 4. Estrutura de Diretórios

A pasta `tests/` deve espelhar a estrutura da `app/`:

```text
projeto-uab/
├── app/
└── tests/
    ├── conftest.py          # Fixtures globais (app, client, db_session)
    ├── unit/                # Testes de lógica isolada
    │   ├── test_auth_utils.py
    │   └── test_services.py
    └── integration/         # Testes de rotas e fluxo completo
        ├── test_auth_routes.py
        ├── test_event_routes.py
        └── test_approval_flow.py
```

---

## 5. Instruções de Execução

### Executar todos os testes:
```bash
pytest
```

### Executar com relatório de cobertura:
```bash
coverage run -m pytest
coverage report -m
# Para ver em HTML:
coverage html
```

---

## 6. Critérios de Aceitação

Para considerar uma entrega válida, os seguintes critérios devem ser satisfeitos:
1.  **Sucesso**: 100% dos testes devem passar.
2.  **Cobertura**: Mínimo de **80% de cobertura** das linhas de código.
3.  **Regressão**: Nenhuma funcionalidade existente deve quebrar ao adicionar novos testes ou código.
4.  **Segurança**: Todas as rotas administrativas devem ter testes de "negação de acesso" para usuários comuns.

---

## 7. Propostas de Melhoria

1.  **Testes E2E (End-to-End)**: Implementar testes com `Selenium` ou `Playwright` para validar a interação do FullCalendar no navegador.
2.  **CI/CD Pipeline**: Configurar **GitHub Actions** para executar os testes automaticamente em cada `push`.
3.  **Testes de Carga**: Usar `Locust` para simular múltiplos secretários acessando a agenda simultaneamente.
4.  **Limpeza de Uploads**: Adicionar um hook no teardown dos testes para apagar arquivos físicos criados na pasta `app/static/uploads` durante a suite.
