# Especificação do Sistema de Gestão de Agenda do Plenário - Frontend & UX

## 1. Design System e Identidade Visual

### 1.1 Cores e Contraste
- **Primária**: Bootstrap `bg-dark` / `#212529` (Navegação e Brand).
- **Sucesso (Deferido)**: `#198754` (Badge e Evento).
- **Perigo (Indeferido)**: `#dc3545` (Badge e Erros).
- **Aviso (Pendente)**: `#ffc107` (Badge e Alertas).
- **Contraste**: Garantir razão mínima de 4.5:1 para legibilidade de texto sobre fundos coloridos.

### 1.2 Tipografia e Espaçamento
- **Fonte**: Sans-serif padrão (interação via Bootstrap 5).
- **Hierarquia**: H1/H2 para títulos de seção, H6/Strong para labels.
- **Espaçamento**: Uso consistente de utilitários `m-*` e `p-*` do Bootstrap para manter respiro visual.

### 1.3 Padronização de Botões Administrativos
- **Regra de Ouro**: Nenhum botão administrativo deve conter apenas ícones.
- **Estrutura**: Todo botão de ação deve conter **Ícone + Texto Visível**.
- **Labels Padronizadas**:
    - "Ver Detalhes"
    - "Editar"
    - "Excluir"
    - "Ativar"
    - "Desativar"
    - "Analisar"
- **Estilo**: Botões Bootstrap 5 (`btn-sm` para listas, `btn-md` para formulários).
- **Alinhamento**: Alinhamento consistente em tabelas e cards, evitando desalinhamentos verticais.

## 2. Componentes de Interface (UI)

### 2.1 Navegação (Layout)
- **Menu Superior**: Fixo no topo, responsivo (hambúrguer em mobile).
- **Visibilidade Condicional**:
  - `Usuários`: Apenas `ADMINISTRADOR`.
  - `Eventos Indeferidos`: `ADMINISTRADOR` e `SECRETARIO`.
- **Feedback de Seção**: Classe `active` no link do menu correspondente à rota atual.

### 2.2 Agenda e Calendário
- **Modo Calendário (FullCalendar)**:
    - Exibe APENAS eventos com status **DEFERIDO**.
    - Responsividade: Alternar para visão de lista (`listMonth`) em telas menores que 768px.
    - Interação: Clique no evento redireciona para detalhes.
- **Modo Lista**:
    - Exibe TODOS os eventos (**PENDENTE**, **DEFERIDO**, **INDEFERIDO**).
    - Badges visuais obrigatórios para cada status.
    - Suporte a parâmetro `?view=list` para abertura direta.

### 2.3 Formulários
- **Layout**: Campos empilhados verticalmente com labels superiores.
- **Validação**: Feedback em tempo real via CSS `:invalid` e mensagens de erro (`invalid-feedback`).
- **Placeholders**: Devem ser institucionais e coerentes com o campo.
- **Botões**:
  - Estado desabilitado (`disabled`) durante submissão.
  - Spinner interno no botão (`.btn-loading`) durante processamento.

### 2.4 Listagens e Cards
- **Badges**: Uso de `.badge` com cores semânticas para Status.
- **Tabelas**: Responsivas (`.table-responsive`), com linhas alternadas e hover.
- **Ações**: Botões de ação devem seguir a regra de **Ícone + Texto**.

### 2.5 Relatórios e Dashboards
- **Regras de Contagem (KPIs)**:
  - **Eventos Totais**: Contabiliza TODOS os eventos (PENDENTE, DEFERIDO, INDEFERIDO).
  - **Eventos este Mês**: Contabiliza apenas PENDENTE e DEFERIDO. Exclui INDEFERIDO.
- **Navegação**: O card de "Eventos Totais" e o botão "Ver Agenda" devem direcionar para a Agenda no modo Lista.

## 3. Experiência do Usuário (UX)

### 3.1 Estados de Tela
- **Carregamento (Loading)**: Uso de spinners ou skeletons em áreas de dados assíncronos.
- **Vazio (Empty State)**: Mensagem amigável com ícone ilustrativo quando não houver dados.
- **Erro**: Alertas (`.alert-danger`) claros com instrução de correção ou feedback de timeout/falha de API.
- **Sucesso**: Alertas (`.alert-success`) para confirmação de ações realizadas.

### 3.2 Acessibilidade (A11y)
- **Navegação por Teclado**: Foco visível (`outline`) em todos os elementos clicáveis.
- **ARIA**: Uso de `aria-label`, `aria-hidden` e `role="alert"` onde apropriado.
- **Labels**: Garantir que todos os inputs tenham labels associados.

## 4. Responsividade
- **Desktop**: Grid completo, menu expandido.
- **Tablet**: Ajuste de colunas, menus colapsados se necessário.
- **Mobile**: Tabelas com scroll horizontal ou transformação em cards, botões em largura total onde apropriado, agenda em modo lista.

## 5. Integração Frontend/Backend
- Sincronização rigorosa entre os status retornados pela API e a renderização visual.
- Tratamento de timeouts e erros de rede com feedback visual para o usuário.

## 7. Segurança e Proteção de Dados

### 7.1 Autenticação e Sessão
- **Hashes de Senha**: Utilização de `PBKDF2` com salt (via Werkzeug) para armazenamento seguro de credenciais.
- **Gestão de Sessão**:
  - Cookies configurados com `HttpOnly=True` e `SameSite=Lax`.
  - Regeneração de ID de sessão após login bem-sucedido para prevenir Session Fixation.
  - Tempo de expiração de sessão definido para 1 hora de inatividade.

### 7.2 Proteção Contra Ataques Comuns
- **CSRF**: Proteção global via `Flask-WTF`. Todos os formulários e chamadas AJAX (fetch) devem incluir e validar tokens CSRF.
- **Brute Force**: Implementação de rate limiting na rota de login (máximo de 5 tentativas por minuto por IP).
- **Enumeração de Usuários**: Mensagens de erro de autenticação padronizadas e genéricas ("Credenciais inválidas").
- **Exposição de Dados**: Tratamento de exceções para evitar que erros técnicos do banco de dados ou do sistema sejam exibidos ao usuário final.
- **Sanitização de Input**: Uso da biblioteca `Bleach` para limpar campos de texto livre (`titulo`, `descricao`), removendo scripts e tags HTML perigosas.

### 7.4 Proteção de Infraestrutura e Arquivos
- **Headers de Segurança**: Implementação do `Flask-Talisman` para forçar headers `HSTS`, `X-Content-Type-Options`, `X-Frame-Options` e `Content-Security-Policy`.
- **Armazenamento Privado**: Documentos e ofícios são armazenados em um diretório fora da área pública (`private_uploads`).
- **Acesso Controlado a Arquivos**: Downloads de ofícios são realizados através de uma rota autenticada (`/events/download/<filename>`), impedindo acesso anônimo direto.
- **Secret Key**: Bloqueio de inicialização em produção caso a `SECRET_KEY` não esteja configurada.

### 7.3 Autorização
- Controle de acesso baseado em perfis (`ADMINISTRADOR`, `SECRETARIO`, `CONSULTOR`) implementado via decorators de rota.
