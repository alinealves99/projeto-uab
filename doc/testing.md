# Plano de Testes (Foco em Frontend e Interface)

## 1. Estratégia de Testes

- **Unitários**: Validação de filtros, formatadores e lógica de negócio isolada.
- **Integração**: Verificação de renderização de templates Flask, resposta a sessões e integração com APIs internas.
- **E2E e Responsividade**: Testes de fluxos de usuário em diferentes dispositivos.

## 2. Cenários de Teste de Interface (UI)

### 2.1 Padronização de Botões
- `test_buttons_contain_text`: Verifica se todos os botões de ação nas listas (Agenda, Usuários, Aprovações) possuem texto visível além do ícone.
- `test_buttons_accessibility`: Valida a presença de `aria-label` e foco visível em botões de ação.

### 2.2 Dashboard e Indicadores
- `test_dashboard_total_counter`: Garante que "Eventos Totais" inclui PENDENTE, DEFERIDO e INDEFERIDO.
- `test_dashboard_monthly_counter`: Garante que "Eventos este Mês" exclui INDEFERIDO.
- `test_dashboard_links_to_list`: Verifica se os links do dashboard redirecionam para a Agenda no modo lista (`?view=list`).

### 2.3 Agenda e FullCalendar
- `test_calendar_only_shows_deferido`: Verifica se a API `/api/events` retorna apenas eventos DEFERIDOS.
- `test_list_shows_all_statuses`: Valida que a visualização de lista exibe todos os status com seus respectivos badges.
- `test_agenda_view_param_handling`: Verifica se o parâmetro `?view=list` abre corretamente a visualização de lista.

### 2.4 Responsividade
- `test_responsive_tables`: Verifica se as tabelas possuem scroll horizontal em resoluções mobile.
- `test_responsive_calendar_view`: Valida se o FullCalendar muda para modo lista em telas pequenas.
- `test_responsive_buttons_no_overlap`: Garante que botões de ação não se sobrepõem em telas menores.

### 2.5 Estados de Tela e Feedback
- `test_form_loading_state`: Verifica se o botão de submit fica `disabled` e exibe spinner ao ser clicado.
- `test_empty_states_rendering`: Valida a exibição de mensagens de "Nenhum dado encontrado" em tabelas vazias.
- `test_error_feedback_alerts`: Verifica a renderização de alertas de erro em caso de falhas de validação ou API.

### 2.6 Acessibilidade
- `test_keyboard_navigation_tab_order`: Valida a ordem de tabulação em formulários.
- `test_contrast_ratios`: (Manual/Auditoria) Garantir legibilidade de textos sobre fundos coloridos.
- `test_input_label_association`: Verifica se todos os inputs possuem labels associados.

### 2.7 Segurança
- `test_csrf_protection`: Verifica se requisições POST sem token CSRF são bloqueadas (403 Forbidden).
- `test_rate_limiting_login`: Valida se múltiplas tentativas de login em curto intervalo retornam erro 429 (Too Many Requests).
- `test_generic_auth_messages`: Garante que o sistema não diferencia erros de "usuário não encontrado" de "senha incorreta" ou "usuário inativo".
- `test_session_regeneration`: Verifica se o ID da sessão muda após o login.
- `test_private_uploads_inaccessible_anonymously`: Garante que arquivos na pasta de uploads não são servidos diretamente via static.
- `test_protected_download_route`: Valida que apenas usuários logados podem baixar ofícios.
- `test_input_sanitization`: Verifica se tags `<script>` são removidas do título/descrição ao salvar um evento.
- `test_security_headers_present`: Valida a presença de X-Frame-Options e CSP nos responses.

## 3. Ferramentas
- **Pytest**: Execução de testes de integração e backend.
- **Coverage**: Monitoramento da cobertura de código (meta >= 80%).
- **Lighthouse (Auditoria Manual)**: Verificação de performance e acessibilidade.

## 4. Instruções de Execução
```bash
# Rodar suite completa de testes
PYTHONPATH=. pytest

# Rodar com cobertura
PYTHONPATH=. coverage run -m pytest
coverage report -m
```
