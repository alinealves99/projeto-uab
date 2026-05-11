from tests.factories import UsuarioFactory
from app.models.usuario import Usuario

def test_admin_acessa_lista_usuarios(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    response = client.get('/users')
    assert response.status_code == 200

def test_consultor_bloqueado_lista_usuarios(auth_client):
    client = auth_client(role="CONSULTOR")
    response = client.get('/users')
    assert response.status_code == 302

def test_criar_usuario_valido(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    data = {
        "nome": "Novo User",
        "email": "novo@teste.com",
        "senha": "password123",
        "role": "SECRETARIO"
    }
    response = client.post('/users/create', data=data)
    assert response.status_code == 302
    
    user = Usuario.query.filter_by(email="novo@teste.com").first()
    assert user is not None
    assert user.role == "SECRETARIO"

def test_toggle_usuario_ativo(auth_client, db_session):
    user = UsuarioFactory(ativo=True)
    db_session.commit()
    
    client = auth_client(role="ADMINISTRADOR")
    response = client.post(f'/users/toggle/{user.id}')
    assert response.status_code == 302
    
    db_session.refresh(user)
    assert user.ativo is False

def test_login_usuario_inativo(client, db_session):
    user = UsuarioFactory(ativo=False)
    user.set_password("senha123")
    db_session.commit()
    
    data = {"email": user.email, "senha": "senha123"}
    response = client.post('/login', data=data)
    assert "Sua conta está desativada" in response.get_data(as_text=True)
