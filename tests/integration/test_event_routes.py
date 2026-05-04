from tests.factories import EventoFactory, UsuarioFactory
import io
from datetime import datetime

def test_admin_pode_acessar_criacao_evento(auth_client):
    client = auth_client(role="ADMINISTRADOR")
    response = client.get('/events/create')
    assert response.status_code == 200

def test_consultor_nao_pode_acessar_criacao_evento(auth_client):
    client = auth_client(role="CONSULTOR")
    response = client.get('/events/create')
    assert response.status_code == 302
    assert response.location.endswith('/events') or response.location.endswith('/events/')

def test_upload_seguro_e_validacao(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    
    # Cenário: Tentativa de upload de arquivo não permitido (.exe)
    data = {
        "titulo": "Evento Teste",
        "data_inicio": "2026-05-10T10:00",
        "data_fim": "2026-05-10T12:00",
        "local": "Auditório",
        "oficio": (io.BytesIO(b"malicious content"), "hack.exe")
    }
    
    response = client.post('/events/create', data=data, content_type='multipart/form-data')
    assert "Extensão de arquivo não permitida" in response.get_data(as_text=True)

def test_conflito_de_horario(auth_client, db_session):
    # Cria um evento existente no banco
    EventoFactory(
        data_inicio=datetime(2026, 6, 1, 14, 0),
        data_fim=datetime(2026, 6, 1, 16, 0),
        local="Sala A",
        status="DEFERIDO"
    )
    db_session.commit()

    client = auth_client(role="ADMINISTRADOR")
    
    # Tenta criar um evento que sobrepõe
    data = {
        "titulo": "Evento Conflitante",
        "data_inicio": "2026-06-01T15:00:00",
        "data_fim": "2026-06-01T17:00:00",
        "local": "Sala A",
        "oficio": (io.BytesIO(b"oficio content"), "oficio.pdf")
    }
    
    response = client.post('/events/create', data=data, content_type='multipart/form-data')
    assert "Conflito de horário detectado" in response.get_data(as_text=True)
