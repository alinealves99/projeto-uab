from app.models.evento import Evento
from app.extensions import db, cache
from datetime import datetime, timezone

class EventoService:
    @staticmethod
    def verificar_conflito(data_inicio, data_fim, local, ignore_id=None):
        query = db.session.query(Evento).filter(
            Evento.local == local,
            Evento.status != "INDEFERIDO",
            Evento.data_inicio < data_fim,
            Evento.data_fim > data_inicio
        )
        if ignore_id:
            query = query.filter(Evento.id != ignore_id)
        
        return query.first() is not None

    @staticmethod
    def listar_eventos_por_perfil(user_role=None):
        # Regra: Agenda Modo Lista deve exibir TODOS os eventos (PENDENTE, DEFERIDO, INDEFERIDO)
        return db.session.query(Evento).order_by(Evento.data_inicio.desc()).all()

    @staticmethod
    def listar_eventos_deferidos():
        return db.session.query(Evento).filter_by(status="DEFERIDO").all()

    @staticmethod
    def listar_indeferidos():
        return db.session.query(Evento).filter_by(status='INDEFERIDO').order_by(Evento.data_inicio.desc()).all()

    @staticmethod
    def listar_pendentes():
        return db.session.query(Evento).filter_by(status='PENDENTE').all()

    @staticmethod
    def buscar_por_id(evento_id):
        return db.session.get(Evento, evento_id)

    @staticmethod
    def criar_novo_evento(dados, solicitante_id):
        novo_evento = Evento(**dados, solicitante_id=solicitante_id, status="PENDENTE")
        try:
            db.session.add(novo_evento)
            db.session.commit()
            cache.delete('dashboard_stats')
            return novo_evento, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def excluir_evento(evento_id):
        evento = EventoService.buscar_por_id(evento_id)
        if not evento:
            return False, "Evento não encontrado."
        
        try:
            db.session.delete(evento)
            db.session.commit()
            cache.delete('dashboard_stats')
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def processar_decisao(evento_id, decisao, justificativa, responsavel_id):
        evento = EventoService.buscar_por_id(evento_id)
        if not evento:
            return None, "Evento não encontrado."

        if evento.status != "PENDENTE":
            return None, "Evento já analisado."

        if decisao == "DEFERIDO":
            evento.status = "DEFERIDO"
        elif decisao == "INDEFERIDO":
            if not justificativa:
                return None, "Justificativa é obrigatória para indeferimento."
            evento.status = "INDEFERIDO"
            evento.justificativa_indeferimento = justificativa
        else:
            return None, "Decisão inválida."

        evento.data_decisao = datetime.now(timezone.utc)
        evento.responsavel_decisao_id = responsavel_id

        try:
            db.session.commit()
            cache.delete('dashboard_stats')
            return evento, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
