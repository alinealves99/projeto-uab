from flask import Blueprint, render_template, request, send_file, Response
from app.services.relatorio_service import obter_dados_dashboard, filtrar_query_eventos
from app.utils.auth_utils import login_required, role_required
from app.services.usuario_service import UsuarioService
from app.extensions import db
from datetime import datetime
import csv
import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def relatorio_dashboard():
    filtros = {
        'data_inicio': request.args.get('data_inicio'),
        'data_fim': request.args.get('data_fim'),
        'status': request.args.get('status'),
        'local': request.args.get('local'),
        'usuario_id': request.args.get('usuario_id'),
        'mes': request.args.get('mes'),
        'ano': request.args.get('ano')
    }
    
    # Remover filtros vazios
    filtros = {k: v for k, v in filtros.items() if v}
    
    dados = obter_dados_dashboard(filtros)
    usuarios = UsuarioService.listar_todos()
    
    return render_template('relatorios/dashboard.html', 
                           dados=dados, 
                           usuarios=usuarios, 
                           filtros=filtros)

@relatorios_bp.route('/relatorios/exportar/csv', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def exportar_csv():
    filtros = {
        'data_inicio': request.args.get('data_inicio'),
        'data_fim': request.args.get('data_fim'),
        'status': request.args.get('status'),
        'local': request.args.get('local'),
        'usuario_id': request.args.get('usuario_id'),
        'mes': request.args.get('mes'),
        'ano': request.args.get('ano')
    }
    filtros = {k: v for k, v in filtros.items() if v}
    
    stmt = filtrar_query_eventos(filtros)
    eventos = db.session.execute(stmt).scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Titulo', 'Local', 'Data Inicio', 'Data Fim', 'Status', 'Solicitante'])
    
    for e in eventos:
        writer.writerow([
            e.id, 
            e.titulo, 
            e.local, 
            e.data_inicio.strftime('%Y-%m-%d %H:%M'), 
            e.data_fim.strftime('%Y-%m-%d %H:%M'), 
            e.status,
            e.solicitante.nome if e.solicitante else 'N/A'
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=relatorio_eventos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
    )

@relatorios_bp.route('/relatorios/exportar/pdf', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SECRETARIO')
def exportar_pdf():
    filtros = {
        'data_inicio': request.args.get('data_inicio'),
        'data_fim': request.args.get('data_fim'),
        'status': request.args.get('status'),
        'local': request.args.get('local'),
        'usuario_id': request.args.get('usuario_id'),
        'mes': request.args.get('mes'),
        'ano': request.args.get('ano')
    }
    filtros = {k: v for k, v in filtros.items() if v}
    
    stmt = filtrar_query_eventos(filtros)
    eventos = db.session.execute(stmt).scalars().all()
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Relatório de Eventos - UAB", styles['Title']))
    elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))
    
    data = [['ID', 'Título', 'Local', 'Data Início', 'Status', 'Solicitante']]
    for e in eventos:
        data.append([
            e.id,
            e.titulo[:30] + '...' if len(e.titulo) > 30 else e.titulo,
            e.local[:20] + '...' if len(e.local) > 20 else e.local,
            e.data_inicio.strftime('%d/%m/%Y'),
            e.status,
            e.solicitante.nome if e.solicitante else 'N/A'
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"relatorio_eventos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mimetype='application/pdf'
    )
