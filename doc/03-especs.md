# Especificação do Sistema de Gestão de Agenda do Plenário

## 1. Configurações e Ambiente

/requirements.txt

- ação: criar
- descrição: Arquivo de dependências do projeto.
- pseudocódigo:
  Flask==3.0.0
  Flask-SQLAlchemy==3.1.1
  python-dotenv==1.0.0
  gunicorn==21.2.0

/.env.example

- ação: criar
- descrição: Variáveis de ambiente necessárias para execução do sistema.
- pseudocódigo:
  SECRET_KEY=chave_segura
  DATABASE_URL=sqlite:///database.db
  DEBUG_MODE=True
  ADMIN_EMAIL=admin@instituicao.com
  ADMIN_PASSWORD=senha_inicial

/config.py

- ação: criar
- descrição: Configuração geral do sistema.
- pseudocódigo:
  IMPORTAR os
  IMPORTAR dotenv
  EXECUTAR dotenv.load_dotenv()

  CLASSE Config:
      SECRET_KEY = os.getenv("SECRET_KEY")
      SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
      DEBUG = BOOLEANO(os.getenv("DEBUG_MODE"))
      ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
      ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


## 2. Inicialização e Infraestrutura

/app/database.py

- ação: criar
- descrição: Inicialização do banco de dados.
- pseudocódigo:
  IMPORTAR SQLAlchemy
  db = SQLAlchemy()

/app/__init__.py

- ação: criar
- descrição: Inicialização da aplicação Flask.
- pseudocódigo:
  IMPORTAR Flask
  IMPORTAR Config
  IMPORTAR db

  FUNCAO create_app():
      app = Flask(__name__)
      CARREGAR_CONFIG(app, Config)

      INICIALIZAR db COM app

      REGISTRAR_BLUEPRINT(auth)
      REGISTRAR_BLUEPRINT(eventos)
      REGISTRAR_BLUEPRINT(aprovacoes)
      REGISTRAR_BLUEPRINT(relatorios)

      RETORNAR app

/run.py

- ação: criar
- descrição: Ponto de entrada da aplicação.
- pseudocódigo:
  IMPORTAR create_app
  IMPORTAR db
  IMPORTAR Usuario

  app = create_app()

  COM CONTEXTO(app):
      CRIAR_TABELAS(db)

      SE admin não existe:
          criar usuário ADMINISTRADOR inicial

  INICIAR app


## 3. Camada de Dados (Models)

/app/models/usuario.py

- ação: criar
- descrição: Modelo de usuários.
- pseudocódigo:
  CLASSE Usuario(db.Model):
      id
      nome
      email
      senha_hash
      role ENUM("ADMINISTRADOR", "SECRETARIO", "CONSULTOR")

/app/models/evento.py

- ação: criar
- descrição: Modelo de eventos.
- pseudocódigo:
  CLASSE Evento(db.Model):
      id
      titulo
      descricao
      data_inicio
      data_fim
      local
      status ENUM("PENDENTE", "DEFERIDO", "INDEFERIDO")
      oficio_path
      justificativa_indeferimento
      data_criacao
      data_decisao

/app/models/anexo.py

- ação: criar
- descrição: Arquivos anexados (ofícios).
- pseudocódigo:
  CLASSE Anexo(db.Model):
      id
      caminho
      evento_id


## 4. Serviços (Services)

/app/services/evento_service.py

- ação: criar
- descrição: Regras de negócio dos eventos.
- pseudocódigo:

  FUNCAO verificar_conflito(data_inicio, data_fim):
      buscar eventos onde:
          data_inicio <= data_fim
          E data_fim >= data_inicio
          E status != "INDEFERIDO"

      SE existir:
          retornar TRUE
      SENAO:
          retornar FALSE


/app/services/upload_service.py

- ação: criar
- descrição: Upload de arquivos.
- pseudocódigo:

  FUNCAO salvar_arquivo(arquivo):
      gerar nome único
      salvar em pasta uploads
      retornar caminho


/app/services/relatorio_service.py

- ação: criar
- descrição: Geração de relatórios.
- pseudocódigo:

  FUNCAO gerar_relatorio():
      total_eventos = contar eventos
      deferidos = contar eventos DEFERIDOS
      indeferidos = contar eventos INDEFERIDOS

      agrupar por mês

      retornar dados


## 5. Controllers (Rotas)

/app/routes/auth.py

- ação: criar
- descrição: Autenticação.
- pseudocódigo:

  ROTA /login:
      validar usuário
      criar sessão

  ROTA /logout:
      limpar sessão


/app/routes/eventos.py

- ação: criar
- descrição: CRUD de eventos.
- pseudocódigo:

  ROTA /eventos [POST]:
      validar dados
      verificar conflito
      salvar arquivo
      criar evento PENDENTE

  ROTA /eventos [GET]:
      listar eventos DEFERIDOS

  ROTA /eventos/<id>:
      retornar detalhes


/app/routes/aprovacoes.py

- ação: criar
- descrição: Deferimento e indeferimento.
- pseudocódigo:

  ROTA /eventos/<id>/deferir:
      verificar status
      alterar para DEFERIDO

  ROTA /eventos/<id>/indeferir:
      salvar justificativa
      alterar para INDEFERIDO


/app/routes/relatorios.py

- ação: criar
- descrição: Relatórios.
- pseudocódigo:

  ROTA /relatorios:
      gerar dados
      retornar dashboard


## 6. Utilitários

/app/utils/auth_utils.py

- ação: criar
- descrição: Controle de acesso.
- pseudocódigo:

  verificar sessão

  verificar role do usuário


## 7. Regras de Negócio

- Eventos devem possuir ofício anexado
- Eventos não podem ter conflito de horário
- Apenas eventos DEFERIDOS aparecem na agenda
- Eventos só podem ser analisados uma vez
- Indeferimento deve permitir justificativa


## 8. Fluxo do Sistema

Etapa | Ação | Usuário
------|------|--------
1 | Cadastrar evento | Administrador
2 | Anexar ofício | Administrador
3 | Evento fica PENDENTE | Sistema
4 | Analisar evento | Secretário-Geral
5 | Deferir ou indeferir | Secretário-Geral
6 | Atualizar status | Sistema
7 | Exibir na agenda | Sistema
