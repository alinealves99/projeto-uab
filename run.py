from app import create_app
from app.extensions import db
from app.models.usuario import Usuario
from flask_migrate import upgrade
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Garante que o banco de dados está atualizado com as migrations
        upgrade()
        
        # Criar usuário ADMINISTRADOR inicial se não existir
        admin_email = app.config.get('ADMIN_EMAIL')
        if not Usuario.query.filter_by(email=admin_email).first():
            admin = Usuario(
                nome="Administrador Inicial",
                email=admin_email,
                role="ADMINISTRADOR"
            )
            admin.set_password(app.config.get('ADMIN_PASSWORD'))
            db.session.add(admin)
            db.session.commit()
            print(f"Usuário administrador criado: {admin_email}")

    app.run(host='0.0.0.0', port=5000)
