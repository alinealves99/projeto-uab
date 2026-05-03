from flask import Blueprint, render_template, redirect, url_for, session
from app.models.evento import Evento
from app.utils.auth_utils import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    total_eventos = Evento.query.count()
    pendentes = Evento.query.filter_by(status='PENDENTE').count()
    return render_template('dashboard.html', total_eventos=total_eventos, pendentes=pendentes)
