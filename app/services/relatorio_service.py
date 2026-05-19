from app.models.evento import Evento
from app.models.usuario import Usuario
from sqlalchemy import func, case, select
from app.extensions import db, cache
from datetime import datetime, timezone

def filtrar_query_eventos(filtros=None):
    query = select(Evento)
    if not filtros:
        return query

    if filtros.get('data_inicio'):
        try:
            data_ini = datetime.strptime(filtros['data_inicio'], '%Y-%m-%d')
            query = query.filter(Evento.data_inicio >= data_ini)
        except ValueError:
            pass
    
    if filtros.get('data_fim'):
        try:
            data_fim = datetime.strptime(filtros['data_fim'], '%Y-%m-%d')
            query = query.filter(Evento.data_inicio <= data_fim)
        except ValueError:
            pass

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
    agora = datetime.now()
    mes_atual = agora.strftime('%m')
    ano_atual = agora.strftime('%Y')

    # Base query com filtros
    base_stmt = filtrar_query_eventos(filtros)
    
    # Extrair a cláusula WHERE da base_stmt para aplicar nas contagens se necessário
    # No SQLAlchemy 2.0, podemos usar base_stmt.whereclause se for um Select
    
    # Query otimizada para contagens principais
    # Para o dashboard, "Eventos Totais" segue os filtros se fornecidos.
    # Mas "Eventos este Mês" tem regra fixa.
    
    stmt_counts = select(
        func.count(Evento.id).label('total'),
        func.count(case((Evento.status == 'DEFERIDO', 1))).label('deferidos'),
        func.count(case((Evento.status == 'INDEFERIDO', 1))).label('indeferidos'),
        func.count(case((Evento.status == 'PENDENTE', 1))).label('pendentes')
    )
    
    if filtros:
        # Aplicar os mesmos filtros à query de contagem
        # filtrar_query_eventos já retorna um select(Evento), podemos mudar o que selecionamos
        stmt_counts = select(
            func.count(Evento.id).label('total'),
            func.count(case((Evento.status == 'DEFERIDO', 1))).label('deferidos'),
            func.count(case((Evento.status == 'INDEFERIDO', 1))).label('indeferidos'),
            func.count(case((Evento.status == 'PENDENTE', 1))).label('pendentes')
        ).select_from(Evento)
        
        # Re-aplicar filtros (simplificado: re-gerar a query de filtros mas com counts)
        tmp_stmt = filtrar_query_eventos(filtros)
        if tmp_stmt.whereclause is not None:
            stmt_counts = stmt_counts.where(tmp_stmt.whereclause)

    res = db.session.execute(stmt_counts).one()
    
    total = res.total
    deferidos = res.deferidos
    indeferidos = res.indeferidos
    pendentes = res.pendentes

    # Eventos no mês atual (Regra fixa: PENDENTE/DEFERIDO este mês)
    stmt_mes = select(func.count(Evento.id)).where(
        Evento.status != 'INDEFERIDO',
        func.strftime('%m', Evento.data_inicio) == mes_atual,
        func.strftime('%Y', Evento.data_inicio) == ano_atual
    )
    eventos_mes = db.session.execute(stmt_mes).scalar()

    taxa_aprovacao = (deferidos / total * 100) if total > 0 else 0

    # Eventos por mês (respeitando filtros se aplicável, ou geral)
    por_mes_stmt = select(
        func.strftime('%Y-%m', Evento.data_inicio).label('mes'),
        func.count(Evento.id).label('total')
    ).group_by('mes').order_by('mes')
    
    if filtros:
        tmp_stmt = filtrar_query_eventos(filtros)
        if tmp_stmt.whereclause is not None:
            por_mes_stmt = por_mes_stmt.where(tmp_stmt.whereclause)
            
    por_mes = db.session.execute(por_mes_stmt).all()

    # Eventos por local
    por_local_stmt = select(
        Evento.local,
        func.count(Evento.id).label('total')
    ).group_by(Evento.local)
    if filtros:
        tmp_stmt = filtrar_query_eventos(filtros)
        if tmp_stmt.whereclause is not None:
            por_local_stmt = por_local_stmt.where(tmp_stmt.whereclause)
    por_local = db.session.execute(por_local_stmt).all()

    # Eventos por status
    por_status_stmt = select(
        Evento.status,
        func.count(Evento.id).label('total')
    ).group_by(Evento.status)
    if filtros:
        tmp_stmt = filtrar_query_eventos(filtros)
        if tmp_stmt.whereclause is not None:
            por_status_stmt = por_status_stmt.where(tmp_stmt.whereclause)
    por_status = db.session.execute(por_status_stmt).all()

    # Eventos por usuário responsável (solicitante)
    por_usuario_stmt = select(
        Usuario.nome,
        func.count(Evento.id).label('total')
    ).join(Usuario, Evento.solicitante_id == Usuario.id).group_by(Usuario.nome)
    if filtros:
        tmp_stmt = filtrar_query_eventos(filtros)
        if tmp_stmt.whereclause is not None:
            por_usuario_stmt = por_usuario_stmt.where(tmp_stmt.whereclause)
    por_usuario = db.session.execute(por_usuario_stmt).all()

    # Últimos eventos (Respeitando filtros)
    ultimos_eventos_stmt = base_stmt.order_by(Evento.data_criacao.desc()).limit(10)
    ultimos_eventos = db.session.execute(ultimos_eventos_stmt).scalars().all()

    return {
        "total": total,
        "total_eventos": total,
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
    return obter_dados_dashboard()

def gerar_relatorio_detalhado():
    return obter_dados_dashboard()

