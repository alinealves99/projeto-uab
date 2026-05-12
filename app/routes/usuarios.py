from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario
from app.extensions import db
from app.utils.auth_utils import login_required, role_required
from werkzeug.security import generate_password_hash

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/users')
@login_required
@role_required('ADMINISTRADOR')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('users/list.html', usuarios=usuarios)

@usuarios_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@role_required('ADMINISTRADOR')
def criar_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        role = request.form.get('role')

        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado.', 'danger')
            return render_template('users/create.html')

        novo_usuario = Usuario(nome=nome, email=email, role=role)
        novo_usuario.set_password(senha)
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário criado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar usuário: {str(e)}")
            flash('Erro ao salvar novo usuário no banco.', 'danger')
            return render_template('users/create.html')
        
        return redirect(url_for('usuarios.listar_usuarios'))

    return render_template('users/create.html')

@usuarios_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMINISTRADOR')
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.role = request.form.get('role')
        
        try:
            db.session.commit()
            flash('Usuário atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar usuário: {str(e)}")
            flash('Erro ao salvar alterações no banco.', 'danger')
        return redirect(url_for('usuarios.listar_usuarios'))

    return render_template('users/edit.html', usuario=usuario)

@usuarios_bp.route('/users/toggle/<int:id>', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR')
def toggle_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == session.get('user_id'):
        flash('Você não pode desativar a si mesmo.', 'danger')
    else:
        usuario.ativo = not usuario.ativo
        try:
            db.session.commit()
            status = "ativado" if usuario.ativo else "desativado"
            flash(f'Usuário {usuario.nome} {status} com sucesso!', 'info')
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao alternar status do usuário: {str(e)}")
            flash('Erro ao atualizar status no banco.', 'danger')
    
    return redirect(url_for('usuarios.listar_usuarios'))

@usuarios_bp.route('/users/reset-password/<int:id>', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR')
def reset_password(id):
    usuario = Usuario.query.get_or_404(id)
    nova_senha = request.form.get('nova_senha')
    
    if nova_senha:
        usuario.set_password(nova_senha)
        try:
            db.session.commit()
            flash(f'Senha de {usuario.nome} redefinida.', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao redefinir senha: {str(e)}")
            flash('Erro ao salvar nova senha no banco.', 'danger')
    else:
        flash('Senha não fornecida.', 'danger')
        
    return redirect(url_for('usuarios.listar_usuarios'))
