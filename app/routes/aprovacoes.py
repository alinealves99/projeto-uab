from flask import Blueprint, request, jsonify, render_template, flash
from app.models.evento import Evento
from app.database import db
from datetime import datetime
from app.utils.auth_utils import login_required, roles_required

aprovacoes_bp = Blueprint('aprovacoes', __name__)

@aprovacoes_bp.route('/events/approve', methods=['GET'])
@login_required
@roles_required('ADMINISTRADOR', 'SECRETARIO')
def listar_pendentes():
    eventos = Evento.query.filter_by(status="PENDENTE").all()
    return render_template('events/approve.html', eventos=eventos)

@aprovacoes_bp.route('/aprovacoes/<int:id>/decisao', methods=['POST'])
@login_required
@roles_required('ADMINISTRADOR', 'SECRETARIO')
def processar_decisao(id):
    data = request.get_json()
    decisao = data.get('decisao')
    justificativa = data.get('justificativa')
    
    evento = Evento.query.get_or_404(id)
    
    if evento.status != "PENDENTE":
        return jsonify({"error": "Evento já analisado"}), 400
    
    if decisao == "DEFERIDO":
        evento.status = "DEFERIDO"
    elif decisao == "INDEFERIDO":
        if not justificativa:
            return jsonify({"error": "Justificativa é obrigatória"}), 400
        evento.status = "INDEFERIDO"
        evento.justificativa_indeferimento = justificativa
    else:
        return jsonify({"error": "Decisão inválida"}), 400
        
    evento.data_decisao = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Decisão processada com sucesso"}), 200
