from app.models.evento import Evento
from sqlalchemy import func
from app.database import db

def gerar_relatorio():
    total_eventos = Evento.query.count()
    deferidos = Evento.query.filter_by(status="DEFERIDO").count()
    indeferidos = Evento.query.filter_by(status="INDEFERIDO").count()

    eventos_por_mes = db.session.query(
        func.strftime('%Y-%m', Evento.data_inicio).label('mes'),
        func.count(Evento.id).label('total')
    ).group_by('mes').all()

    return {
        "total_eventos": total_eventos,
        "deferidos": deferidos,
        "indeferidos": indeferidos,
        "eventos_por_mes": [{"mes": row.mes, "total": row.total} for row in eventos_por_mes]
    }
