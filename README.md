# Sistema de Gestão de Agenda do Plenário - Projeto UAB

Sistema para gerenciamento de eventos, controle de agenda do plenário e fluxo de aprovação de solicitações.

## Principais Funcionalidades

- **Design System Moderno**: Padronização visual com Bootstrap 5, foco em legibilidade e contraste.
- **Performance Otimizada**: Uso de Cache (Flask-Caching) para estatísticas e relatórios.
- **Tarefas em Background**: Automação de manutenção (limpeza de arquivos) via Flask-APScheduler.
- **Arquitetura Modular**: Camada de serviços (Service Layer) separada das rotas para melhor manutenibilidade.
- **Acessibilidade**: Navegação por teclado, labels semânticas e suporte a leitores de tela (ARIA).
- **Responsividade**: Experiência otimizada para Desktop, Tablet e Mobile (Agenda dinâmica).
- **Gestão de Usuários**: Cadastro, edição, ativação/desativação e redefinição de senha (apenas administradores).
- **Agenda Interativa**: Visualização de eventos **deferidos** em calendário (FullCalendar) e listagem completa de todos os status (Pendente, Deferido, Indeferido) no modo lista com filtros.
- **Módulo de Relatórios**: Dashboard gerencial com estatísticas inteligentes (exclusão de indeferidos nos indicadores operacionais mensais), gráficos (Chart.js) e exportação (CSV/PDF).
- **Fluxo de Aprovação**: Solicitação de eventos com upload de ofício e análise por secretários.
- **Eventos Indeferidos**: Listagem administrativa detalhada de solicitações rejeitadas com justificativa.
- **Segurança e Hardening**: 
  - Controle de acesso baseado em perfis (ADMINISTRADOR, SECRETARIO, CONSULTOR).
  - Proteção global contra **CSRF** (Cross-Site Request Forgery).
  - Mitigação de ataques de **Brute Force** via Rate Limiting.
  - Prevenção de **Session Fixation** com regeneração de ID de sessão.
  - Cookies de sessão protegidos (`HttpOnly`, `SameSite=Lax`).
  - Headers de segurança HTTP (**HSTS, CSP, X-Frame-Options**) via Flask-Talisman.
  - Armazenamento privado de documentos (**Private Uploads**) fora da área pública.
  - Downloads autenticados de anexos.
  - Sanitização de entrada (**XSS Protection**) com Bleach.
  - Mensagens de erro padronizadas para evitar **Enumeração de Usuários** e vazamento de informações técnicas.

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

## Gerenciamento de Banco de Dados

O projeto utiliza **Flask-Migrate** para gerenciar o esquema do banco de dados.

### Inicialização do Banco (Setup Inicial)
Se estiver rodando pela primeira vez ou o banco foi excluído:
```bash
export FLASK_APP=run.py
flask db upgrade
```

### Criar novas migrações (após alterar Models)
```bash
flask db migrate -m "Descrição da alteração"
flask db upgrade
```

### Reset do Banco (Limpeza Total)
```bash
rm instance/database.db
flask db upgrade
```

## Solução de Problemas (Troubleshooting)

### Erro: "attempt to write a readonly database"
Este erro geralmente ocorre devido a permissões de pasta ou caminhos incorretos no SQLite.
1. Certifique-se de que a pasta `instance/` tem permissão de escrita:
   ```bash
   chmod 775 instance
   ```
2. O sistema está configurado para usar caminhos absolutos no `config.py`, o que evita este erro em diferentes ambientes.
3. Se o erro persistir, verifique se não há processos órfãos travando o arquivo:
   ```bash
   pkill -9 python
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

- [Especificações Detalhadas](doc/03-specs.md)
- [Plano de Testes](doc/testing.md)
