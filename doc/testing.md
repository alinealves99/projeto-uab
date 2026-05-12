# Plano de Testes (Revisado - Foco em Frontend e Integração)

## 1. Estratégia de Testes

- **Unitários**: Validação de filtros e formatadores.
- **Integração**: Verificação de renderização de templates Flask e resposta a sessões.
- **E2E/Visual (Manual/Automático)**: Testes de responsividade e fluxos de UI.

## 2. Cenários de Teste de Frontend

### 2.1 Navegação e Responsividade
- `test_layout_responsivo_mobile`: Verifica se o menu colapsa em resoluções < 768px.
- `test_agenda_view_switch`: Verifica se o FullCalendar muda para `listWeek` em mobile.
- `test_active_menu_highlight`: Garante que o item de menu atual possui a classe `.active`.

### 2.2 Acessibilidade (A11y)
- `test_form_labels_association`: Verifica se todos os `<input>` possuem `<label>` associado via `for/id`.
- `test_keyboard_navigation`: Valida se o foco segue a ordem lógica (Tab) nos formulários de cadastro.
- `test_aria_attributes_alerts`: Verifica se os alertas flash possuem `role="alert"`.

### 2.3 Integração e Estados de Tela
- `test_agenda_loading_state`: Simula atraso na API e verifica se o spinner de carregamento é exibido.
- `test_agenda_empty_state`: Verifica a mensagem de "Nenhum evento" quando a API retorna `[]`.
- `test_form_submission_loading`: Verifica se o botão de envio fica `disabled` após o clique.
- `test_validation_feedback_visual`: Garante que campos inválidos exibem a borda vermelha e a mensagem de erro.
- `test_api_error_handling_alert`: Valida se o frontend exibe o erro específico retornado pela API em caso de falha no deferimento.

### 2.4 Visibilidade e Ações Administrativas
- `test_admin_menu_users_visibility`: ADMIN vê menu "Usuários".
- `test_secretario_menu_users_hidden`: SECRETARIO NÃO vê menu "Usuários".
- `test_consultor_menus_restricted`: CONSULTOR NÃO vê "Aprovações" nem "Eventos Indeferidos".
- `test_user_actions_buttons_alignment`: Verifica se os botões de ação na lista de usuários estão agrupados corretamente (CSS `gap-2`).
- `test_approve_event_flow_integration`: Valida o ciclo completo: Clique em Deferir -> Requisição API -> Mudança de Status no DB -> Reload da página.

### 2.6 Integridade de Dados e Transações
- `test_db_rollback_on_failure`: Simula um erro durante a criação de evento e verifica se o `rollback()` impediu a criação parcial ou inconsistência no banco.
- `test_db_write_permissions`: Valida se o ambiente de execução permite a escrita de arquivos temporários do SQLite (check de modo readonly).

### 2.7 Otimização e Performance
- `test_dashboard_cache`: Verifica se o acesso repetido ao dashboard em curto intervalo não gera novas consultas pesadas ao banco (validar via cache hit).
- `test_service_modularization`: Garante que as rotas utilizam métodos dos serviços em vez de lógica direta do SQLAlchemy.
- `test_background_cleanup_job`: Valida se o job de limpeza de arquivos remove arquivos temporários ou órfãos sem travar a thread principal da aplicação.

## 3. Ferramentas
- **Pytest**: Execução de testes de integração backend/frontend.
- **Lighthouse (Manual)**: Auditoria de acessibilidade e performance.
- **Playwright/Cypress (Opcional/Futuro)**: Para automação E2E completa.

## 4. Instruções de Execução
```bash
# Rodar testes de integração existentes
PYTHONPATH=. pytest

# Auditoria visual manual
python run.py # e acessar via navegador com ferramentas de desenvolvedor
```
