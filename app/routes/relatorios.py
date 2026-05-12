from flask import Blueprint, jsonify
from app.services.relatorio_service import gerar_relatorio_detalhado
from app.utils.auth_utils import login_required, role_required

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def relatorio_dashboard():
    dados = gerar_relatorio_detalhado()
    return jsonify(dados), 200
