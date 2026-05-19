from flask import Blueprint, request, jsonify, render_template, flash, session
from app.services.evento_service import EventoService
from app.utils.auth_utils import login_required, role_required

aprovacoes_bp = Blueprint('aprovacoes', __name__)

@aprovacoes_bp.route('/aprovacoes/pendentes')
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def listar_pendentes():
    eventos = EventoService.listar_pendentes()
    return render_template('events/approve.html', eventos=eventos)

@aprovacoes_bp.route('/aprovacoes/<int:id>/decisao', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def processar_decisao(id):
    data = request.get_json()
    decisao = data.get('decisao')
    justificativa = data.get('justificativa')

    evento, erro = EventoService.processar_decisao(
        id, decisao, justificativa, session.get('user_id')
    )

    if erro:
        status_code = 400
        if erro == "Evento não encontrado.":
            status_code = 404
        elif "Erro interno" in erro:
            status_code = 500
        return jsonify({"error": erro}), status_code

    if decisao == "DEFERIDO":
        flash(f"Evento '{evento.titulo}' deferido com sucesso!", "success")
    else:
        flash(f"Evento '{evento.titulo}' indeferido.", "info")

    return jsonify({"message": "Decisão processada com sucesso"}), 200

