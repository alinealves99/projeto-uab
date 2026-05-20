import os
import time
from app.extensions import scheduler, db
from app.models.anexo import Anexo

def cleanup_orphan_files(app):
    """
    Remove arquivos na pasta de uploads que não possuem registro no banco de dados.
    """
    with app.app_context():
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        upload_folder = os.path.join(base_dir, 'private_uploads')
        if not os.path.exists(upload_folder):
            return

        # Lista arquivos no banco
        files_in_db = {a.caminho for a in Anexo.query.all()}
        # Adiciona ofícios dos eventos (caso estejam salvos diretamente na tabela evento)
        from app.models.evento import Evento
        files_in_db.update({e.oficio_path for e in Evento.query.all() if e.oficio_path})

        # Lista arquivos em disco
        files_on_disk = os.listdir(upload_folder)

        for filename in files_on_disk:
            if filename == '.gitkeep':
                continue
            if filename not in files_in_db:
                file_path = os.path.join(upload_folder, filename)
                try:
                    # Verifica se o arquivo tem mais de 24 horas para evitar deletar uploads em andamento
                    if os.path.getmtime(file_path) < time.time() - 86400:
                        os.remove(file_path)
                        print(f"Job: Arquivo órfão removido: {filename}")
                except Exception as e:
                    print(f"Job: Erro ao remover {filename}: {e}")

def register_jobs(app):
    @scheduler.task('interval', id='cleanup_orphans', hours=24)
    def scheduled_cleanup():
        cleanup_orphan_files(app)
