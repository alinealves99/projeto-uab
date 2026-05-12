import pytest
import io
from app.extensions import cache
from tests.factories import EventoFactory

def test_dashboard_stats_cache(auth_client, db_session):
    # Garante cache limpo
    cache.clear()
    
    # Cria eventos
    EventoFactory(status="PENDENTE")
    db_session.commit()
    
    client = auth_client(role="ADMINISTRADOR")
    
    # Primeiro acesso - deve popular o cache
    res1 = client.get('/dashboard')
    assert res1.status_code == 200
    # Verifica o contador de aprovações pendentes (usando encode para lidar com acentos)
    assert "Aprovações Pendentes".encode('utf-8') in res1.data
    assert b"1</h2>" in res1.data
    
    # Altera dado no banco diretamente (sem passar pelo serviço que invalida)
    EventoFactory(status="PENDENTE")
    db_session.commit()
    
    # Segundo acesso - deve vir do cache (ainda exibindo 1)
    res2 = client.get('/dashboard')
    assert b"1</h2>" in res2.data
    assert b"2</h2>" not in res2.data
    
    # Invalida cache manualmente
    cache.delete('dashboard_stats')
    
    # Terceiro acesso - deve vir do banco (exibindo 2)
    res3 = client.get('/dashboard')
    assert b"2</h2>" in res3.data

def test_cache_invalidation_on_creation(auth_client, db_session):
    cache.clear()
    client = auth_client(role="ADMINISTRADOR")
    
    # Popula cache
    client.get('/dashboard')
    
    # Cria novo evento via rota (que deve invalidar cache)
    data = {
        "titulo": "Novo Evento",
        "data_inicio": "2026-12-01T10:00:00",
        "data_fim": "2026-12-01T11:00:00",
        "local": "Plenário",
        "oficio": (io.BytesIO(b"fake pdf"), "oficio.pdf")
    }
    
    client.post('/events/create', data=data, content_type='multipart/form-data')
    
    # Verifica dashboard - deve refletir o novo evento (cache invalidado)
    res = client.get('/dashboard')
    assert b"1</h2>" in res.data
