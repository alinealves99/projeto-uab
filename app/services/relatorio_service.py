from app.models.evento import Evento
from app.models.usuario import Usuario
from sqlalchemy import func, case
from app.extensions import db, cache
from datetime import datetime

def filtrar_query_eventos(filtros=None):
    query = Evento.query
    if not filtros:
        return query

    if filtros.get('data_inicio'):
        data_ini = datetime.strptime(filtros['data_inicio'], '%Y-%m-%d')
        query = query.filter(Evento.data_inicio >= data_ini)
    
    if filtros.get('data_fim'):
        data_fim = datetime.strptime(filtros['data_fim'], '%Y-%m-%d')
        query = query.filter(Evento.data_inicio <= data_fim)

    if filtros.get('status'):
        query = query.filter(Evento.status == filtros['status'])

    if filtros.get('local'):
        query = query.filter(Evento.local.ilike(f"%{filtros['local']}%"))

    if filtros.get('usuario_id'):
        query = query.filter(Evento.solicitante_id == filtros['usuario_id'])

    if filtros.get('mes'):
        query = query.filter(func.strftime('%m', Evento.data_inicio) == filtros['mes'].zfill(2))

    if filtros.get('ano'):
        query = query.filter(func.strftime('%Y', Evento.data_inicio) == filtros['ano'])

    return query

def obter_dados_dashboard(filtros=None):
    query_base = filtrar_query_eventos(filtros)
    
    total = query_base.count()
    deferidos = query_base.filter(Evento.status == 'DEFERIDO').count()
    indeferidos = query_base.filter(Evento.status == 'INDEFERIDO').count()
    pendentes = query_base.filter(Evento.status == 'PENDENTE').count()
    
    # Eventos no mês atual (baseado em data_inicio)
    # Regra: Apenas PENDENTE e DEFERIDO. Excluir INDEFERIDO.
    agora = datetime.now()
    mes_atual = agora.strftime('%m')
    ano_atual = agora.strftime('%Y')
    eventos_mes = query_base.filter(
        Evento.status != 'INDEFERIDO',
        func.strftime('%m', Evento.data_inicio) == mes_atual,
        func.strftime('%Y', Evento.data_inicio) == ano_atual
    ).count()

    taxa_aprovacao = (deferidos / total * 100) if total > 0 else 0

    # Eventos por mês
    por_mes = db.session.query(
        func.strftime('%Y-%m', Evento.data_inicio).label('mes'),
        func.count(Evento.id).label('total')
    ).filter(Evento.id.in_(query_base.with_entities(Evento.id))).group_by('mes').order_by('mes').all()

    # Eventos por local
    por_local = db.session.query(
        Evento.local,
        func.count(Evento.id).label('total')
    ).filter(Evento.id.in_(query_base.with_entities(Evento.id))).group_by(Evento.local).all()

    # Eventos por status
    por_status = db.session.query(
        Evento.status,
        func.count(Evento.id).label('total')
    ).filter(Evento.id.in_(query_base.with_entities(Evento.id))).group_by(Evento.status).all()

    # Eventos por usuário responsável (solicitante)
    por_usuario = db.session.query(
        Usuario.nome,
        func.count(Evento.id).label('total')
    ).join(Usuario, Evento.solicitante_id == Usuario.id)\
     .filter(Evento.id.in_(query_base.with_entities(Evento.id)))\
     .group_by(Usuario.nome).all()

    # Últimos eventos
    ultimos_eventos = query_base.order_by(Evento.data_criacao.desc()).limit(10).all()

    return {
        "total": total,
        "total_eventos": total, # Compatibilidade com dashboard.html
        "deferidos": deferidos,
        "indeferidos": indeferidos,
        "pendentes": pendentes,
        "eventos_mes": eventos_mes,
        "taxa_aprovacao": round(taxa_aprovacao, 2),
        "por_mes": [{"mes": r.mes, "total": r.total} for r in por_mes],
        "por_local": [{"local": r.local, "total": r.total} for r in por_local],
        "por_status": [{"status": r.status, "total": r.total} for r in por_status],
        "por_usuario": [{"nome": r.nome, "total": r.total} for r in por_usuario],
        "ultimos_eventos": ultimos_eventos
    }

@cache.cached(timeout=300, key_prefix='dashboard_stats')
def gerar_estatisticas_dashboard():
    # Mantendo compatibilidade se houver outros usos, mas agora com cache mais inteligente se necessário
    return obter_dados_dashboard()

def gerar_relatorio_detalhado():
    # Mantendo compatibilidade
    return obter_dados_dashboard()

