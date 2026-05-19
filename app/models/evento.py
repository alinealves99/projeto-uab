from app.extensions import db
from datetime import datetime, timezone

class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    local = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum("PENDENTE", "DEFERIDO", "INDEFERIDO", name="event_status"), default="PENDENTE")
    oficio_path = db.Column(db.String(255), nullable=True)
    justificativa_indeferimento = db.Column(db.Text, nullable=True)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    data_decisao = db.Column(db.DateTime, nullable=True)
    responsavel_decisao_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    anexos = db.relationship('Anexo', backref='evento', lazy=True)
    solicitante = db.relationship('Usuario', foreign_keys=[solicitante_id], backref='eventos_solicitados')
    responsavel_decisao = db.relationship('Usuario', foreign_keys=[responsavel_decisao_id], backref='eventos_decididos')
