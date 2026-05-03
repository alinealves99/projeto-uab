from flask import Blueprint, request, session, jsonify, redirect, url_for, render_template, flash
from app.models.usuario import Usuario
from app.database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(senha):
            session['user_id'] = usuario.id
            session['user_role'] = usuario.role
            session['user_nome'] = usuario.nome
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        
        flash('Credenciais inválidas', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))
