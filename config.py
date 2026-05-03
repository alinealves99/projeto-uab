import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG_MODE", "True") == "True"
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@instituicao.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "senha_inicial")
