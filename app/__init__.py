from flask import Flask
from config import Config
from app.extensions import db, migrate, cache, scheduler

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure Cache
    app.config['CACHE_TYPE'] = 'FileSystemCache'
    app.config['CACHE_DIR'] = 'instance/cache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    
    if not scheduler.running:
        scheduler.init_app(app)
        scheduler.start()

    from app.jobs import register_jobs
    register_jobs(app)

    # Import models to register them with SQLAlchemy
    from app.models import usuario, evento, anexo

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
