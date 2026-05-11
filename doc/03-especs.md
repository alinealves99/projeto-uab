# Especificação do Sistema de Gestão de Agenda do Plenário (Revisada)

## 1. Configurações e Ambiente

/requirements.txt
- ação: atualizar
- descrição: Dependências do projeto.
- dependências:
  Flask==3.0.0
  Flask-SQLAlchemy==3.1.1
  python-dotenv==1.0.0
  gunicorn==21.2.0
  factory-boy (para testes)
  pytest (para testes)
  pytest-flask (para testes)
  coverage (para testes)

/.env.example
- variáveis:
  SECRET_KEY=chave_segura
  DATABASE_URL=sqlite:///database.db
  DEBUG_MODE=True
  ADMIN_EMAIL=admin@instituicao.com
  ADMIN_PASSWORD=senha_inicial

## 2. Inicialização e Infraestrutura

/app/__init__.py
- Registrar blueprints: auth, eventos, aprovacoes, relatorios, usuarios, main.

/run.py
- Inicialização do banco e criação do usuário ADMINISTRADOR padrão (se não existir).

## 3. Camada de Dados (Models)

/app/models/usuario.py
- Atributos:
  - id (PK)
  - nome (String)
  - email (String, Unique)
  - senha_hash (String)
  - role (Enum: ADMINISTRADOR, SECRETARIO, CONSULTOR)
  - ativo (Boolean, Default=True)

/app/models/evento.py
- Atributos:
  - id (PK)
  - titulo (String)
  - descricao (Text)
  - data_inicio (DateTime)
  - data_fim (DateTime)
  - local (String)
  - status (Enum: PENDENTE, DEFERIDO, INDEFERIDO)
  - oficio_path (String)
  - justificativa_indeferimento (Text)
  - data_criacao (DateTime)
  - data_decisao (DateTime)
  - responsavel_decisao_id (FK -> usuarios.id)
  - solicitante_id (FK -> usuarios.id)

## 4. Serviços (Services)

/app/services/evento_service.py
- Validar conflitos (ignorar eventos INDEFERIDOS).
- Filtragem de eventos por status.

/app/services/usuario_service.py (Novo)
- CRUD de usuários.
- Lógica de ativação/desativação.
- Redefinição de senha.

## 5. Controllers (Rotas)

/app/routes/auth.py
- Login: Validar se usuário existe e se está ATIVO.
- Logout: Limpar sessão.

/app/routes/eventos.py
- Agenda Pública: Exibe apenas eventos DEFERIDOS.
- Detalhes: Acessível conforme permissão.
- Eventos Indeferidos: Listagem exclusiva para ADMINISTRADOR e SECRETARIO.

/app/routes/usuarios.py (Novo)
- Interface administrativa para CRUD de usuários.
- Acesso restrito a ADMINISTRADOR.
- Ações: Listar, Criar, Editar, Ativar/Desativar, Resetar Senha.

/app/routes/aprovacoes.py
- Fluxo de análise (PENDENTE -> DEFERIDO/INDEFERIDO).
- Registrar data_decisao e responsavel_decisao_id.

## 6. Utilitários

/app/utils/auth_utils.py
- Decorator `@login_required`.
- Decorator `@role_required(*roles)`.

## 7. Regras de Negócio (Atualizadas)

1.  **Exibição de Eventos:**
    *   Eventos DEFERIDOS: Agenda pública (FullCalendar).
    *   Eventos PENDENTES: Visíveis apenas em telas de aprovação e para o solicitante.
    *   Eventos INDEFERIDOS: **Não aparecem na agenda principal**. Listados em tela administrativa específica.
2.  **Gestão de Usuários:**
    *   Apenas ADMINISTRADORES gerenciam usuários.
    *   Usuários inativos não podem logar.
    *   Perfis: ADMINISTRADOR (pleno), SECRETARIO (aprova eventos), CONSULTOR (apenas visualiza/solicita).
3.  **Segurança:**
    *   Feedback via Flash Messages em todas as operações.
    *   Redirecionamento para login ou dashboard em caso de acesso negado.

## 8. Interface e Menus

Menu | Perfil Autorizado | Destino
-----|-------------------|--------
Dashboard | Todos (Logados) | /dashboard
Agenda | Todos | /events
Criar Evento | ADMINISTRADOR, SECRETARIO | /events/create
Aprovações | ADMINISTRADOR, SECRETARIO | /approvals/pending
Eventos Indeferidos | ADMINISTRADOR, SECRETARIO | /events/indeferidos
Usuários | ADMINISTRADOR | /users
Sair | Todos (Logados) | /logout
