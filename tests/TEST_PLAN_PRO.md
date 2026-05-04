# Plano de Testes Avançado (PRO) - Projeto UAB

## 1. Análise Crítica do Plano Anterior

O plano de testes inicial (`testing.md`) estabeleceu uma base sólida com TDD, mas apresenta lacunas técnicas que podem comprometer a robustez do sistema em produção:

*   **Isolamento de Estado:** A fixture `auth_client` atual injeta valores na sessão, mas não garante a existência do objeto `User` correspondente no banco de dados, o que pode mascarar erros de integridade referencial em rotas que dependem de `current_user`.
*   **Lacunas de Segurança:**
    *   **Bypass de Autorização:** Testes focados apenas no "caminho feliz" e negação básica. Falta testar escalonamento de privilégios (ex: Consultor tentando deletar evento via ID direto no POST).
    *   **Path Traversal:** Nenhuma validação automatizada para nomes de arquivos sanitizados durante o upload de anexos.
*   **Cobertura de Integração:** O plano anterior foca em rotas individuais, negligenciando testes de estado (ex: um evento só pode ser aprovado se estiver com status `PENDENTE`).
*   **Performance e Concorrência:** O sistema gerencia recursos compartilhados (salas/auditórios). O plano original não aborda *Race Conditions* em reservas simultâneas.

---

## 2. Estratégia de Testes TDD Avançada

### 2.1 Níveis de Teste
Adotaremos a pirâmide de testes adaptada para a arquitetura Flask/SQLAlchemy:

1.  **Unitários (Services/Utils):** Foco total em `app/services/*.py`. Testaremos o `EventoService` isoladamente do Flask, mockando o `db.session` se necessário, para validar regras de negócio puras (ex: cálculo de overlap de horários).
2.  **Integração (Routes/DB):** Utilização do `client` do Flask para disparar requisições HTTP reais contra um banco SQLite em memória. Validação de contratos de API e persistência.
3.  **Funcionais (Fluxos):** Testes que mimetizam a jornada do usuário: `Login -> Criação de Evento -> Logout -> Login Secretário -> Aprovação`.

### 2.2 Mocking vs Spying Strategy
*   **Uploads:** Não escreveremos no disco real. Usaremos `unittest.mock.patch` para interceptar `app.services.upload_service.save_file` e verificar se foi chamado com os argumentos corretos (*Spying*).
*   **Notificações (Futuras):** Mockar serviços de e-mail/SMS para evitar dependências externas e lentidão.
*   **Sessão:** Manteremos o uso de `session_transaction` para simular estados de login sem passar pelo fluxo de UI em cada teste.

---

## 3. Matriz de Cobertura de Segurança

| Vetor de Ataque | Estratégia de Mitigação | Cenário de Teste (Pytest) |
| :--- | :--- | :--- |
| **Bypass @role_required** | Decoradores de autorização centralizados. | `test_unauthorized_access_raises_403` em todas as rotas `ADMINISTRADOR/SECRETARIO`. |
| **Path Traversal** | Sanitização via `werkzeug.utils.secure_filename`. | `test_upload_filename_sanitization` com input `"../../../etc/passwd.pdf"`. |
| **SQL Injection** | SQLAlchemy ORM (Parametrização automática). | `test_event_search_injection` injetando `' OR 1=1 --` em campos de busca. |
| **Double-booking** | Locks de banco de dados ou validação atômica. | `test_concurrent_booking_race_condition` simulando duas threads tentando reservar a mesma sala no mesmo segundo. |
| **Broken Auth** | Rotação de Session ID. | `test_session_id_changes_on_login` para evitar fixation. |

---

## 4. Infraestrutura Técnica

### 4.1 Fixtures Estruturadas (`conftest.py`)
Evoluiremos as fixtures para garantir integridade:
*   `db_session`: Utilizará `transaction.begin_nested()` para permitir rollbacks rápidos entre testes.
*   `authenticated_user(role)`: Fixture que cria um usuário real via `UsuarioFactory` e injeta seu ID na sessão.

### 4.2 Geração de Massa com Factory Boy
O uso de `factories.py` é obrigatório para evitar o "Mystery Guest" (dados mágicos nos testes).
*   **SubFactories:** Para vincular anexos a eventos automaticamente.
*   **Fuzzy Attributes:** Para datas e textos aleatórios que testam limites de tamanho de campo.

---

## 5. Guia de Implementação CI/CD

### 5.1 GitHub Actions Workflow
Arquivo: `.github/workflows/tests.yml` (proposto)

```yaml
name: Quality Gate - Python Pytest

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with: { python-version: '3.10' }
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov factory-boy
      - name: Run Tests with Coverage
        run: |
          pytest --cov=app --cov-report=xml --cov-fail-under=80
```

### 5.2 Quality Gate
*   **Métrica:** Cobertura de código.
*   **Hard Fail:** O build deve falhar se a cobertura cair abaixo de **80%**.
*   **Linting:** Adicionar `flake8` ou `black --check` como step obrigatório para garantir o estilo de código.

---

## 6. Padronização de Código de Teste

Todo novo teste deve seguir o padrão **AAA (Arrange, Act, Assert)**:

```python
def test_create_event_overlap_fails(auth_client, db_session):
    # Arrange: Criar evento pré-existente
    existing = EventoFactory(data_inicio=d1, data_fim=d2, local="Auditório")
    db_session.commit()
    
    # Act: Tentar criar evento sobreposto
    payload = {"data_inicio": overlap_d1, ...}
    response = auth_client(role="ADMIN").post('/events/create', data=payload)
    
    # Assert
    assert response.status_code == 200 # Se retornar formulário com erro
    assert "Conflito de horário" in response.get_data(as_text=True)
```
