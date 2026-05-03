from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from app.models.evento import Evento
from app.models.anexo import Anexo
from app.services.evento_service import verificar_conflito
from app.services.upload_service import salvar_arquivo
from app.database import db
from datetime import datetime
from app.utils.auth_utils import login_required, roles_required

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
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

        if verificar_conflito(data_inicio, data_fim, local):
            flash("Conflito de horário detectado", "danger")
            return render_template('events/create.html')

        oficio_path = salvar_arquivo(oficio)
        
        novo_evento = Evento(
            titulo=titulo,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            local=local,
            oficio_path=oficio_path,
            status="PENDENTE"
        )
        
        db.session.add(novo_evento)
        db.session.commit()
        
        flash("Evento criado com sucesso e enviado para aprovação!", "success")
        return redirect(url_for('eventos.listar_eventos'))

    return render_template('events/create.html')

@eventos_bp.route('/api/events', methods=['GET'])
def api_eventos():
    start = request.args.get('start')
    end = request.args.get('end')
    
    query = Evento.query.filter_by(status="DEFERIDO")
    
    # Simple date filtering if parameters provided
    if start and end:
        # FullCalendar sends ISO dates
        pass 
        
    eventos = query.all()
    
    return jsonify([{
        "id": e.id,
        "title": e.titulo,
        "start": e.data_inicio.isoformat(),
        "end": e.data_fim.isoformat(),
        "color": "#198754" if e.status == "DEFERIDO" else "#ffc107",
        "url": url_for('eventos.detalhes_evento', id=e.id)
    } for e in eventos]), 200

@eventos_bp.route('/events', methods=['GET'])
def listar_eventos():
    # Se logado como administrador, vê todos, caso contrário apenas deferidos
    if session.get('user_role') == 'ADMINISTRADOR':
        eventos = Evento.query.order_by(Evento.data_inicio.desc()).all()
    else:
        eventos = Evento.query.filter_by(status="DEFERIDO").order_by(Evento.data_inicio.desc()).all()
    
    return render_template('events/list.html', eventos=eventos)

@eventos_bp.route('/events/<int:id>', methods=['GET'])
def detalhes_evento(id):
    evento = Evento.query.get_or_404(id)
    return render_template('events/detail.html', evento=evento)

@eventos_bp.route('/events/delete/<int:id>', methods=['POST'])
@login_required
@roles_required('ADMINISTRADOR')
def excluir_evento(id):
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    flash("Evento excluído com sucesso!", "success")
    return redirect(url_for('eventos.listar_eventos'))
