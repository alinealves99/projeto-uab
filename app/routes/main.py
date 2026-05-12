from flask import Blueprint, render_template, redirect, url_for, session
from app.utils.auth_utils import login_required
from app.services.relatorio_service import gerar_estatisticas_dashboard

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    stats = gerar_estatisticas_dashboard()
    return render_template('dashboard.html', **stats)
