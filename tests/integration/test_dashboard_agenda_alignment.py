import pytest
from app.models.evento import Evento
from tests.factories import EventoFactory, UsuarioFactory
from datetime import datetime, timedelta

def test_dashboard_stats_alignment(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    
    agora = datetime.now()
    # Evento DEFERIDO no mês atual
    EventoFactory(status="DEFERIDO", data_inicio=agora)
    # Evento PENDENTE no mês atual
    EventoFactory(status="PENDENTE", data_inicio=agora)
    # Evento INDEFERIDO no mês atual
    EventoFactory(status="INDEFERIDO", data_inicio=agora)
    # Evento DEFERIDO em outro mês
    mes_proximo = agora + timedelta(days=32)
    EventoFactory(status="DEFERIDO", data_inicio=mes_proximo)
    
    db_session.commit()
    
    # Invalida cache se houver
    from app.extensions import cache
    cache.delete('dashboard_stats')
    
    response = client.get('/dashboard')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    
    # "Eventos Totais" deve ser 4 (DEFERIDO x2, PENDENTE, INDEFERIDO)
    assert 'Eventos Totais' in html
    assert '4</h2>' in html
    
    # "Eventos este Mês" deve ser 2 (Apenas DEFERIDO e PENDENTE do mês atual. Exclui INDEFERIDO)
    assert 'Eventos este Mês' in html
    assert '2</h2>' in html

def test_calendar_api_only_deferidos(auth_client, db_session):
    client = auth_client(role="CONSULTOR")
    
    EventoFactory(status="DEFERIDO", titulo="Evento Deferido")
    EventoFactory(status="PENDENTE", titulo="Evento Pendente")
    EventoFactory(status="INDEFERIDO", titulo="Evento Indeferido")
    db_session.commit()
    
    response = client.get('/api/events')
    assert response.status_code == 200
    data = response.get_json()
    
    # Apenas o DEFERIDO deve aparecer no calendário
    assert len(data) == 1
    assert data[0]['title'] == "Evento Deferido"

def test_agenda_list_view_all_statuses_consultor(auth_client, db_session):
    client = auth_client(role="CONSULTOR")
    
    EventoFactory(status="DEFERIDO", titulo="List Deferido")
    EventoFactory(status="PENDENTE", titulo="List Pendente")
    EventoFactory(status="INDEFERIDO", titulo="List Indeferido")
    db_session.commit()
    
    # Na agenda (modo lista), o consultor deve ver todos os eventos agora
    response = client.get('/events')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    
    assert "List Deferido" in html
    assert "List Pendente" in html
    assert "List Indeferido" in html

def test_dashboard_links_to_list_view(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    response = client.get('/dashboard')
    html = response.get_data(as_text=True)
    
    # Verifica se os links da agenda agora incluem ?view=list
    assert 'href="/events?view=list"' in html
