from app.models.evento import Evento
from app.database import db

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
