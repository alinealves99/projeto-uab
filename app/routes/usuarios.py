from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.usuario_service import UsuarioService
from app.utils.auth_utils import login_required, role_required

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/users')
@login_required
@role_required('ADMINISTRADOR')
def listar_usuarios():
    usuarios = UsuarioService.listar_todos()
    return render_template('users/list.html', usuarios=usuarios)

@usuarios_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@role_required('ADMINISTRADOR')
def criar_usuario():
    if request.method == 'POST':
        usuario, erro = UsuarioService.criar_usuario(request.form)
        if erro:
            flash(erro, 'danger')
            return render_template('users/create.html')
        
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))

    return render_template('users/create.html')

@usuarios_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMINISTRADOR')
def editar_usuario(id):
    if request.method == 'POST':
        usuario, erro = UsuarioService.atualizar_usuario(id, request.form)
        if erro:
            flash(erro, 'danger')
        else:
            flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))

    usuario = UsuarioService.buscar_por_id(id)
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('usuarios.listar_usuarios'))
        
    return render_template('users/edit.html', usuario=usuario)

@usuarios_bp.route('/users/toggle/<int:id>', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR')
def toggle_usuario(id):
    usuario, erro = UsuarioService.toggle_ativo(id, session.get('user_id'))
    if erro:
        flash(erro, 'danger')
    else:
        status = "ativado" if usuario.ativo else "desativado"
        flash(f'Usuário {usuario.nome} {status} com sucesso!', 'info')
    
    return redirect(url_for('usuarios.listar_usuarios'))

@usuarios_bp.route('/users/reset-password/<int:id>', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR')
def reset_password(id):
    usuario, erro = UsuarioService.redefinir_senha(id, request.form.get('nova_senha'))
    if erro:
        flash(erro, 'danger')
    else:
        flash(f'Senha de {usuario.nome} redefinida.', 'success')
        
    return redirect(url_for('usuarios.listar_usuarios'))
