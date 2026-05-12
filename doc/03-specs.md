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

## 2. Componentes de Interface (UI)

### 2.1 Navegação (Layout)
- **Menu Superior**: Fixo no topo, responsivo (hambúrguer em mobile).
- **Visibilidade Condicional**:
  - `Usuários`: Apenas `ADMINISTRADOR`.
  - `Eventos Indeferidos`: `ADMINISTRADOR` e `SECRETARIO`.
- **Feedback de Seção**: Classe `active` no link do menu correspondente à rota atual.

### 2.2 Agenda (FullCalendar)
- **Responsividade**: Alternar para visão de lista (`listWeek`) em telas menores que 768px.
- **Loading State**: Spinner visual centralizado durante o fetch da API `/api/events`.
- **Estado Vazio**: Mensagem informativa se a API retornar lista vazia.
- **Interação**: Clique no evento redireciona para `/events/<id>`.

### 2.3 Formulários
- **Layout**: Campos empilhados verticalmente com labels superiores.
- **Validação**: Feedback em tempo real via CSS `:invalid` e mensagens de erro (`invalid-feedback`).
- **Botões**:
  - Estado desabilitado (`disabled`) durante submissão.
  - Spinner interno no botão durante processamento.
- **Upload**: Área de drop ou botão claro, exibindo nome do arquivo selecionado.

### 2.4 Listagens e Cards
- **Badges**: Uso de `.badge` com cores semânticas para Status.
- **Tabelas**: Responsivas (`.table-responsive`), com linhas alternadas e hover.
- **Ações**: Botões de ação em tabelas devem utilizar `d-flex gap-2` para garantir espaçamento e alinhamento, evitando o uso de `btn-group` quando envolverem formulários ou modais.

## 3. Experiência do Usuário (UX)

### 3.1 Estados de Tela
- **Carregamento**: Skeleton screens ou Spinners Bootstrap em ações assíncronas.
- **Botões Administrativos**: Devem entrar em estado `disabled` e exibir um spinner (`.btn-loading`) durante o processamento de requisições `fetch/AJAX` ou submissões de formulário.
- **Prevenção de Cliques Duplos**: Bloqueio obrigatório de botões após o primeiro clique válido.
- **Erro**: Alertas (`.alert-danger`) claros com instrução de correção. Em requisições AJAX, exibir erros específicos retornados pelo servidor via `alert()` ou modais.
- **Vazio**: Ilustração ou ícone com texto descritivo quando não houver dados.

### 3.2 Acessibilidade (A11y)
- **Semântica**: Uso correto de `<nav>`, `<main>`, `<footer>`, `<header>`.
- **Navegação**: Tabulação lógica entre campos de formulário e links.
- **ARIA**:
  - `aria-label` em botões de ícone (ex: fechar modal).
  - `aria-invalid` em campos com erro.
  - `role="alert"` em mensagens flash.
- **Foco**: Outline visível em todos os elementos clicáveis.

## 4. Integração Frontend/Backend

- **Flash Messages**: Renderização centralizada no `layout.html`, mapeando categorias Flask (`success`, `danger`, `warning`, `info`) para classes de alerta Bootstrap correspondentes.
- **Formulários**: 
  - Submissão via POST tradicional para rotas Flask.
  - Validação via `needs-validation` (Bootstrap JS) impedindo o envio de campos vazios ou inválidos.
  - Bloqueio de cliques duplos via JavaScript (estado `disabled` no submit).
- **APIs Assíncronas**: 
  - Consumo de `/api/events` pelo FullCalendar com tratamento de estados de carregamento (spinner) e erro (console log/visual fallback).

## 6. Arquitetura de Banco de Dados e Performance

### 6.1 Persistência e Sincronização
- **Engine**: SQLite (em arquivo `instance/database.db`).
- **ORM**: SQLAlchemy 3.x.
- **Caminho Absoluto**: O banco é configurado com caminho absoluto para garantir permissões de escrita e suporte a arquivos de log (`-wal`, `-shm`) do SQLite em qualquer ambiente de execução.
- **Tratamento de Transações**: Todas as operações de escrita (`add`, `delete`, `commit`) devem ser encapsuladas em blocos `try/except` com `db.session.rollback()` automático para prevenir travamentos e corrupção de dados.
- **Migrações**: Gerenciadas pelo **Flask-Migrate** (Alembic).

### 6.2 Otimização de Performance
- **Cache de Dados**: Utilização de **Flask-Caching** para armazenar resultados de consultas pesadas (ex: estatísticas do Dashboard e Relatórios) por períodos curtos (ex: 5 minutos).
- **Processamento Assíncrono (Jobs)**: Implementação de tarefas em segundo plano (via threads ou agendadores leves) para operações de manutenção, como limpeza de arquivos órfãos na pasta de uploads.
- **Minificação de Ativos**: Garantir que o CSS e JS sejam entregues de forma eficiente, evitando redundâncias.

### 6.3 Modularização e Manutenibilidade
- **Service Layer**: Toda a lógica de negócio deve residir em `/app/services/`, evitando código pesado dentro das rotas (controllers).
- **Eliminação de Duplicidade**: Centralizar cálculos de estatísticas e filtros de consulta em serviços reutilizáveis.
- **Singleton Pattern**: Garantir instâncias únicas de extensões (db, migrate, cache) para evitar imports circulares.

## 7. Responsividade (Breakpoints)
- **Mobile (< 576px)**: Formulários em coluna única, agenda em lista.
- **Tablet (576px - 992px)**: Menus colapsados, cards em grid 2 colunas.
- **Desktop (> 992px)**: Grid completo, menu expandido.
