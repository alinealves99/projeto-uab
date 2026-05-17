from app.models.evento import Evento
from app.extensions import db, cache
from flask import session

def verificar_conflito(data_inicio, data_fim, local, ignore_id=None):
    query = Evento.query.filter(
        Evento.local == local,
        Evento.status != "INDEFERIDO",
        Evento.data_inicio < data_fim,
        Evento.data_fim > data_inicio
    )
    if ignore_id:
        query = query.filter(Evento.id != ignore_id)
    
    return query.first() is not None

def listar_eventos_por_perfil(user_role):
    # Regra: Agenda Modo Lista deve exibir TODOS os eventos (PENDENTE, DEFERIDO, INDEFERIDO)
    # para todos os perfis de usuário.
    return Evento.query.order_by(Evento.data_inicio.desc()).all()

def criar_novo_evento(dados, solicitante_id):
    novo_evento = Evento(**dados, solicitante_id=solicitante_id, status="PENDENTE")
    try:
        db.session.add(novo_evento)
        db.session.commit()
        # Invalida o cache do dashboard ao criar novo evento
        cache.delete('dashboard_stats')
        return novo_evento, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)
