import factory
from app.database import db
from app.models.usuario import Usuario
from app.models.evento import Evento
from datetime import datetime, timedelta

class UsuarioFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Usuario
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    nome = factory.Faker("name")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    senha_hash = "pbkdf2:sha256:260000$mocked_hash"
    role = "CONSULTOR"

class EventoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Evento
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    titulo = factory.Faker("sentence")
    descricao = factory.Faker("paragraph")
    data_inicio = datetime.now() + timedelta(days=1)
    data_fim = datetime.now() + timedelta(days=1, hours=2)
    local = "Sala 01 - Bloco A"
    status = "PENDENTE"
