from app.models.evento import Evento
from sqlalchemy import func
from app.extensions import db, cache

@cache.cached(timeout=300, key_prefix='dashboard_stats')
def gerar_estatisticas_dashboard():
    total_eventos = Evento.query.count()
    pendentes = Evento.query.filter_by(status='PENDENTE').count()
    
    # Eventos no mês atual
    agora = func.now()
    eventos_mes = Evento.query.filter(
        func.strftime('%Y-%m', Evento.data_inicio) == func.strftime('%Y-%m', agora)
    ).count()

    return {
        "total_eventos": total_eventos,
        "pendentes": pendentes,
        "eventos_mes": eventos_mes
    }

def gerar_relatorio_detalhado():
    stats = gerar_estatisticas_dashboard()
    deferidos = Evento.query.filter_by(status="DEFERIDO").count()
    indeferidos = Evento.query.filter_by(status="INDEFERIDO").count()

    eventos_por_mes = db.session.query(
        func.strftime('%Y-%m', Evento.data_inicio).label('mes'),
        func.count(Evento.id).label('total')
    ).group_by('mes').all()

    return {
        **stats,
        "deferidos": deferidos,
        "indeferidos": indeferidos,
        "eventos_por_mes": [{"mes": row.mes, "total": row.total} for row in eventos_por_mes]
    }
