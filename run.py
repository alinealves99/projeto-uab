from app import create_app
from app.database import db
from app.models.usuario import Usuario
from app.models.evento import Evento
from app.models.anexo import Anexo
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
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
