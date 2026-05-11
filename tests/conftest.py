import pytest
from app import create_app
from app.database import db
from app.models.usuario import Usuario
from app.models.evento import Evento
from app.models.anexo import Anexo

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False  # Facilita testes de formulário
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def db_session(app):
    with app.app_context():
        # Limpa as tabelas a cada teste para garantir isolamento
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        yield db.session

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client, app):
    """Helper para criar clientes autenticados com diferentes roles"""
    def _login(role="CONSULTOR", email="test@test.com"):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_role'] = role
            sess['user_nome'] = "Usuário Teste"
        return client
    return _login
