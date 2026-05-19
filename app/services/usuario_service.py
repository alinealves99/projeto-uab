from app.models.usuario import Usuario
from app.extensions import db
from flask import session

class UsuarioService:
    @staticmethod
    def listar_todos():
        return Usuario.query.all()

    @staticmethod
    def buscar_por_id(usuario_id):
        return db.session.get(Usuario, usuario_id)

    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def criar_usuario(dados):
        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')
        role = dados.get('role')

        if UsuarioService.buscar_por_email(email):
            return None, "Email já cadastrado."

        novo_usuario = Usuario(nome=nome, email=email, role=role)
        novo_usuario.set_password(senha)
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return novo_usuario, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def atualizar_usuario(usuario_id, dados):
        usuario = UsuarioService.buscar_por_id(usuario_id)
        if not usuario:
            return None, "Usuário não encontrado."

        usuario.nome = dados.get('nome', usuario.nome)
        usuario.role = dados.get('role', usuario.role)
        
        try:
            db.session.commit()
            return usuario, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def toggle_ativo(usuario_id, current_user_id):
        if usuario_id == current_user_id:
            return None, "Você não pode desativar a si mesmo."
        
        usuario = UsuarioService.buscar_por_id(usuario_id)
        if not usuario:
            return None, "Usuário não encontrado."

        usuario.ativo = not usuario.ativo
        try:
            db.session.commit()
            return usuario, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def redefinir_senha(usuario_id, nova_senha):
        usuario = UsuarioService.buscar_por_id(usuario_id)
        if not usuario:
            return None, "Usuário não encontrado."

        if not nova_senha:
            return None, "Senha não fornecida."

        usuario.set_password(nova_senha)
        try:
            db.session.commit()
            return usuario, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def autenticar(email, senha):
        usuario = UsuarioService.buscar_por_email(email)
        if usuario and usuario.check_password(senha):
            if not usuario.ativo:
                return None, "Sua conta está desativada. Entre em contato com o administrador."
            
            # Prepara dados da sessão
            session_data = {
                'user_id': usuario.id,
                'user_role': usuario.role,
                'user_nome': usuario.nome
            }
            return session_data, None
        
        return None, "Credenciais inválidas"
