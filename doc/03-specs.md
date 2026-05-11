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

## 3. Experiência do Usuário (UX)

### 3.1 Estados de Tela
- **Carregamento**: Skeleton screens ou Spinners Bootstrap em ações assíncronas.
- **Erro**: Alertas (`.alert-danger`) claros com instrução de correção.
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

- **Flash Messages**: Renderização no topo do `<main>`, desaparecendo após 5 segundos (opcional) ou via botão fechar.
- **Responses**:
  - Erros 403/404: Páginas customizadas ou redirecionamento com flash informativo.
  - Erros de Validação: Mapeamento de erros do backend para os campos correspondentes no frontend.

## 5. Responsividade (Breakpoints)
- **Mobile (< 576px)**: Formulários em coluna única, agenda em lista.
- **Tablet (576px - 992px)**: Menus colapsados, cards em grid 2 colunas.
- **Desktop (> 992px)**: Grid completo, menu expandido.
