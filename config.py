import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        # Permite valor padrão APENAS em desenvolvimento local se DEBUG for True
        if os.environ.get("DEBUG_MODE", "True") == "True":
            SECRET_KEY = "dev-key-only-for-local-testing"
        else:
            raise RuntimeError("A variável SECRET_KEY não foi configurada no ambiente de produção.")
    # Força o uso da pasta instance com caminho absoluto para evitar erro de readonly/path
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG_MODE", "True") == "True"
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@instituicao.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "senha_inicial")
