import pytest
from tests.factories import EventoFactory, UsuarioFactory
from app.models.evento import Evento

def test_processar_decisao_deferido_sucesso(auth_client, db_session):
    admin = UsuarioFactory(role="ADMINISTRADOR")
    evento = EventoFactory(status="PENDENTE")
    db_session.commit()

    # Login como admin
    client = auth_client(role="ADMINISTRADOR")
    
    payload = {"decisao": "DEFERIDO"}
    response = client.post(f'/aprovacoes/{evento.id}/decisao', json=payload)
    
    assert response.status_code == 200
    assert response.get_json()['message'] == "Decisão processada com sucesso"
    
    db_session.refresh(evento)
    assert evento.status == "DEFERIDO"
    assert evento.responsavel_decisao_id is not None

def test_processar_decisao_evento_ja_analisado(auth_client, db_session):
    evento = EventoFactory(status="DEFERIDO")
    db_session.commit()

    client = auth_client(role="ADMINISTRADOR")
    
    payload = {"decisao": "DEFERIDO"}
    response = client.post(f'/aprovacoes/{evento.id}/decisao', json=payload)
    
    assert response.status_code == 400
    assert "Evento já analisado" in response.get_json()['error']

def test_processar_decisao_indeferido_sem_justificativa(auth_client, db_session):
    evento = EventoFactory(status="PENDENTE")
    db_session.commit()

    client = auth_client(role="ADMINISTRADOR")
    
    payload = {"decisao": "INDEFERIDO"}
    response = client.post(f'/aprovacoes/{evento.id}/decisao', json=payload)
    
    assert response.status_code == 400
    assert "Justificativa é obrigatória" in response.get_json()['error']
