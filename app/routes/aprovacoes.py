from flask import Blueprint, request, jsonify, render_template, flash, session
from app.models.evento import Evento
from app.extensions import db, cache
from datetime import datetime
from app.utils.auth_utils import login_required, role_required

aprovacoes_bp = Blueprint('aprovacoes', __name__)

@aprovacoes_bp.route('/aprovacoes/pendentes')
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def listar_pendentes():
    eventos = Evento.query.filter_by(status='PENDENTE').all()
    return render_template('events/approve.html', eventos=eventos)

@aprovacoes_bp.route('/aprovacoes/<int:id>/decisao', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def processar_decisao(id):
    data = request.get_json()
    decisao = data.get('decisao')
    justificativa = data.get('justificativa')

    evento = Evento.query.get_or_404(id)

    if evento.status != "PENDENTE":
        return jsonify({"error": "Evento já analisado"}), 400

    if decisao == "DEFERIDO":
        evento.status = "DEFERIDO"
        flash(f"Evento '{evento.titulo}' deferido com sucesso!", "success")
    elif decisao == "INDEFERIDO":
        if not justificativa:
            return jsonify({"error": "Justificativa é obrigatória"}), 400
        evento.status = "INDEFERIDO"
        evento.justificativa_indeferimento = justificativa
        flash(f"Evento '{evento.titulo}' indeferido.", "info")
    else:
        return jsonify({"error": "Decisão inválida"}), 400

    evento.data_decisao = datetime.utcnow()
    evento.responsavel_decisao_id = session.get('user_id')

    try:
        db.session.commit()
        # Invalida cache ao aprovar/rejeitar
        cache.delete('dashboard_stats')
        return jsonify({"message": "Decisão processada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao processar decisão: {str(e)}")
        return jsonify({"error": "Erro interno ao salvar decisão"}), 500

