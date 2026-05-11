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

### 2.4 Visibilidade por Perfil
- `test_admin_menu_users_visibility`: ADMIN vê menu "Usuários".
- `test_secretario_menu_users_hidden`: SECRETARIO NÃO vê menu "Usuários".
- `test_consultor_menus_restricted`: CONSULTOR NÃO vê "Aprovações" nem "Eventos Indeferidos".

### 2.5 Componentes e Design
- `test_status_badges_colors`: Verifica se DEFERIDO é verde, PENDENTE é amarelo e INDEFERIDO é vermelho.
- `test_table_responsivity`: Garante que tabelas de usuários possuem scroll horizontal em telas pequenas.

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
