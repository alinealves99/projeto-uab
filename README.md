# Sistema de Gestão de Agenda do Plenário - Projeto UAB

Sistema para gerenciamento de eventos, controle de agenda do plenário e fluxo de aprovação de solicitações.

## Principais Funcionalidades

- **Design System Moderno**: Padronização visual com Bootstrap 5, foco em legibilidade e contraste.
- **Acessibilidade**: Navegação por teclado, labels semânticas e suporte a leitores de tela (ARIA).
- **Responsividade**: Experiência otimizada para Desktop, Tablet e Mobile (Agenda dinâmica).
- **Gestão de Usuários**: Cadastro, edição, ativação/desativação e redefinição de senha (apenas administradores).
- **Agenda Interativa**: Visualização de eventos deferidos em calendário (FullCalendar).
- **Fluxo de Aprovação**: Solicitação de eventos com upload de ofício e análise por secretários.
- **Eventos Indeferidos**: Listagem administrativa detalhada de solicitações rejeitadas com justificativa.
- **Segurança**: Controle de acesso baseado em perfis (ADMINISTRADOR, SECRETARIO, CONSULTOR) e bloqueio de usuários inativos.

## Tecnologias Utilizadas

- **Backend**: Flask 3.0, SQLAlchemy
- **Frontend**: Bootstrap 5, FullCalendar 6
- **Testes**: Pytest, Factory Boy, Coverage

## Instalação e Execução

1. **Clonar o repositório**
2. **Criar ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux
   ```
3. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar variáveis de ambiente**:
   Crie um arquivo `.env` baseado no `.env.example`.
5. **Executar a aplicação**:
   ```bash
   python run.py
   ```

## Execução de Testes

Para garantir a qualidade e segurança do sistema, execute a suite de testes:

```bash
# Todos os testes
PYTHONPATH=. pytest

# Relatório de cobertura
PYTHONPATH=. coverage run -m pytest
coverage report -m
```

## Documentação Técnica

- [Especificações Detalhadas](doc/03-especs.md)
- [Plano de Testes](doc/testing.md)
