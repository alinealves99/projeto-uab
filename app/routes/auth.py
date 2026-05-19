from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from app.services.usuario_service import UsuarioService
from app.extensions import limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        session_data, erro = UsuarioService.autenticar(email, senha)
        if session_data:
            # Session Fixation Protection: Regenerate session
            session.clear()
            session.update(session_data)
            session.permanent = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        
        flash(erro, 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))
