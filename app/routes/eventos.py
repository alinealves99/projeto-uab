from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from app.services.evento_service import EventoService
from app.services.upload_service import salvar_arquivo
from datetime import datetime
from app.utils.auth_utils import login_required, role_required

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
@role_required('ADMINISTRADOR')
def criar_evento():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        try:
            data_inicio = datetime.fromisoformat(request.form.get('data_inicio'))
            data_fim = datetime.fromisoformat(request.form.get('data_fim'))
        except (ValueError, TypeError):
            flash("Datas inválidas", "danger")
            return render_template('events/create.html')

        local = request.form.get('local')
        oficio = request.files.get('oficio')

        if not oficio:
            flash("Ofício é obrigatório", "danger")
            return render_template('events/create.html')

        if EventoService.verificar_conflito(data_inicio, data_fim, local):
            flash("Conflito de horário detectado", "danger")
            return render_template('events/create.html')

        oficio_path = salvar_arquivo(oficio)
        if not oficio_path:
            flash("Extensão de arquivo não permitida", "danger")
            return render_template('events/create.html')
        
        dados_evento = {
            "titulo": titulo,
            "descricao": descricao,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "local": local,
            "oficio_path": oficio_path
        }
        
        evento, erro = EventoService.criar_novo_evento(dados_evento, session.get('user_id'))
        
        if erro:
            flash("Erro crítico ao salvar no banco de dados.", "danger")
            return render_template('events/create.html')
        
        flash("Evento criado com sucesso e enviado para aprovação!", "success")
        return redirect(url_for('eventos.listar_eventos'))

    return render_template('events/create.html')

@eventos_bp.route('/api/events', methods=['GET'])
def api_eventos():
    eventos = EventoService.listar_eventos_deferidos()
    
    return jsonify([{
        "id": e.id,
        "title": e.titulo,
        "start": e.data_inicio.isoformat(),
        "end": e.data_fim.isoformat(),
        "color": "#198754", # Sempre DEFERIDO nesta query
        "url": url_for('eventos.detalhes_evento', id=e.id)
    } for e in eventos]), 200

@eventos_bp.route('/events', methods=['GET'])
def listar_eventos():
    eventos = EventoService.listar_eventos_por_perfil(session.get('user_role'))
    return render_template('events/list.html', eventos=eventos)

@eventos_bp.route('/events/indeferidos', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def listar_indeferidos():
    eventos = EventoService.listar_indeferidos()
    return render_template('events/indeferidos.html', eventos=eventos)

@eventos_bp.route('/events/<int:id>', methods=['GET'])
def detalhes_evento(id):
    evento = EventoService.buscar_por_id(id)
    if not evento:
        flash("Evento não encontrado", "danger")
        return redirect(url_for('eventos.listar_eventos'))
    return render_template('events/detail.html', evento=evento)

@eventos_bp.route('/events/delete/<int:id>', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR')
def excluir_evento(id):
    sucesso, erro = EventoService.excluir_evento(id)
    if sucesso:
        flash("Evento excluído com sucesso!", "success")
    else:
        flash(f"Erro ao excluir evento: {erro}", "danger")
    return redirect(url_for('eventos.listar_eventos'))
