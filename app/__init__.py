from flask import Flask
from config import Config
from app.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.eventos import eventos_bp
    from app.routes.aprovacoes import aprovacoes_bp
    from app.routes.relatorios import relatorios_bp
    from app.routes.main import main_bp
    from app.routes.usuarios import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(eventos_bp)
    app.register_blueprint(aprovacoes_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)

    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.utcnow()}

    return app
