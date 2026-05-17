import pytest
from app.models.evento import Evento
from tests.factories import EventoFactory, UsuarioFactory
from datetime import datetime, timedelta

def test_acesso_relatorios_negado_consultor(auth_client):
    client = auth_client(role="CONSULTOR")
    response = client.get('/relatorios', follow_redirects=True)
    assert response.status_code == 200
    assert "Acesso não autorizado" in response.get_data(as_text=True)

def test_acesso_relatorios_permitido_admin(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    response = client.get('/relatorios')
    assert response.status_code == 200
    assert "Relatórios Administrativos" in response.get_data(as_text=True)

def test_acesso_relatorios_permitido_secretario(auth_client, db_session):
    client = auth_client(role="SECRETARIO")
    response = client.get('/relatorios')
    assert response.status_code == 200

def test_filtros_relatorio(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    
    # Criar eventos
    u1 = UsuarioFactory(nome="User 1")
    EventoFactory(titulo="Evento A", local="Local 1", status="DEFERIDO", solicitante=u1)
    EventoFactory(titulo="Evento B", local="Local 2", status="PENDENTE")
    db_session.commit()
    
    # Filtrar por status
    response = client.get('/relatorios?status=DEFERIDO')
    assert response.status_code == 200
    assert "Evento A" in response.get_data(as_text=True)
    assert "Evento B" not in response.get_data(as_text=True)
    
    # Filtrar por local
    response = client.get('/relatorios?local=Local 2')
    assert "Evento B" in response.get_data(as_text=True)
    assert "Evento A" not in response.get_data(as_text=True)

    # Filtrar por usuário
    response = client.get(f'/relatorios?usuario_id={u1.id}')
    assert "Evento A" in response.get_data(as_text=True)
    assert "Evento B" not in response.get_data(as_text=True)

def test_exportar_csv(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    EventoFactory(titulo="CSV Evento")
    db_session.commit()
    
    response = client.get('/relatorios/exportar/csv')
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "CSV Evento" in response.get_data(as_text=True)

def test_exportar_pdf(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    EventoFactory(titulo="PDF Evento")
    db_session.commit()
    
    response = client.get('/relatorios/exportar/pdf')
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"

def test_filtros_avancados_relatorio(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    
    # Criar eventos com datas específicas
    d1 = datetime(2024, 1, 15)
    d2 = datetime(2024, 2, 20)
    EventoFactory(titulo="Evento Jan", data_inicio=d1, data_fim=d1+timedelta(hours=1))
    EventoFactory(titulo="Evento Fev", data_inicio=d2, data_fim=d2+timedelta(hours=1))
    db_session.commit()
    
    # Filtro de data inicio
    response = client.get('/relatorios?data_inicio=2024-02-01')
    assert "Evento Fev" in response.get_data(as_text=True)
    assert "Evento Jan" not in response.get_data(as_text=True)
    
    # Filtro de data fim
    response = client.get('/relatorios?data_fim=2024-01-31')
    assert "Evento Jan" in response.get_data(as_text=True)
    assert "Evento Fev" not in response.get_data(as_text=True)
    
    # Filtro de mes e ano
    response = client.get('/relatorios?mes=2&ano=2024')
    assert "Evento Fev" in response.get_data(as_text=True)
    assert "Evento Jan" not in response.get_data(as_text=True)

def test_dashboard_counters(auth_client, db_session):
    client = auth_client(role="ADMINISTRADOR")
    
    # Criar eventos no mês atual
    agora = datetime.now()
    EventoFactory(titulo="Evento Atual 1", data_inicio=agora)
    EventoFactory(titulo="Evento Atual 2", data_inicio=agora)
    
    # Criar evento em outro mês
    mes_passado = agora - timedelta(days=32)
    EventoFactory(titulo="Evento Passado", data_inicio=mes_passado)
    
    db_session.commit()
    
    # Invalida cache para garantir que os novos eventos sejam contabilizados
    from app.extensions import cache
    cache.delete('dashboard_stats')
    
    response = client.get('/dashboard')
    assert response.status_code == 200
    conteudo = response.get_data(as_text=True)
    
    # Verificar Total (3)
    assert 'Eventos Totais' in conteudo
    assert '3</h2>' in conteudo
    
    # Verificar Eventos este Mês (2)
    assert 'Eventos este Mês' in conteudo
    assert '2</h2>' in conteudo
