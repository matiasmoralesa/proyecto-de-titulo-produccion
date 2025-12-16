"""
Services for checklists app.
"""
import os
from datetime import datetime
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


def generate_checklist_pdf(checklist_response):
    """
    Generate a PDF for a completed checklist response.
    
    Args:
        checklist_response: ChecklistResponse instance
    
    Returns:
        File path to the generated PDF
    """
    try:
        buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6
    )
    
    # Title
    title = Paragraph(
        f"<b>{checklist_response.template.name}</b>",
        title_style
    )
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Header Information Table
    header_data = [
        ['Código:', checklist_response.template.code, 'Fecha:', checklist_response.created_at.strftime('%d/%m/%Y %H:%M')],
        ['Activo:', checklist_response.asset.name, 'Patente:', checklist_response.asset.license_plate or 'N/A'],
        ['Operador:', checklist_response.completed_by.get_full_name() if checklist_response.completed_by else 'N/A', 
         'Estado:', checklist_response.get_status_display()],
        ['Puntuación:', f"{checklist_response.score}%" if checklist_response.score else 'N/A', 
         'Mínimo Requerido:', f"{checklist_response.template.passing_score}%"],
    ]
    
    header_table = Table(header_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Checklist Items by Section
    item_responses = checklist_response.item_responses.select_related('template_item').order_by('template_item__order')
    
    current_section = None
    section_items = []
    
    for item_response in item_responses:
        template_item = item_response.template_item
        
        # Add section header if new section
        if current_section != template_item.section:
            # Add previous section table if exists
            if section_items:
                _add_section_table(elements, section_items)
                section_items = []
            
            current_section = template_item.section
            section_heading = Paragraph(f"<b>{current_section}</b>", heading_style)
            elements.append(section_heading)
        
        # Add item to section
        response_display = _format_response_value(item_response.response_value)
        observations = item_response.observations or '-'
        
        section_items.append([
            str(template_item.order),
            template_item.question,
            response_display,
            observations[:50] + '...' if len(observations) > 50 else observations
        ])
    
    # Add last section table
    if section_items:
        _add_section_table(elements, section_items)
    
    # Signature Section
    if checklist_response.signature_data:
        elements.append(Spacer(1, 0.3*inch))
        signature_heading = Paragraph("<b>Firma Digital</b>", heading_style)
        elements.append(signature_heading)
        elements.append(Spacer(1, 0.1*inch))
        
        try:
            # signature_data is a base64 image string (data:image/png;base64,...)
            import base64
            from PIL import Image as PILImage
            
            # Extract base64 data
            if ',' in checklist_response.signature_data:
                base64_data = checklist_response.signature_data.split(',')[1]
            else:
                base64_data = checklist_response.signature_data
            
            # Decode base64 to image
            image_data = base64.b64decode(base64_data)
            image_buffer = BytesIO(image_data)
            
            # Load image with PIL to check dimensions
            pil_img = PILImage.open(BytesIO(image_data))
            img_width, img_height = pil_img.size
            
            # Only show image if it's larger than 10x10 (not a placeholder)
            if img_width > 10 and img_height > 10:
                # Reset buffer position
                image_buffer.seek(0)
                
                # Calculate aspect ratio
                aspect = img_width / img_height
                display_height = 1*inch
                display_width = display_height * aspect
                
                # Limit width to 3 inches
                if display_width > 3*inch:
                    display_width = 3*inch
                    display_height = display_width / aspect
                
                # Create image for PDF
                signature_img = Image(image_buffer, width=display_width, height=display_height)
                
                # Create signature table
                signature_data = [
                    ['Firma del Operador:'],
                    [signature_img],
                    [checklist_response.completed_by.get_full_name() if checklist_response.completed_by else 'N/A']
                ]
                
                signature_table = Table(signature_data, colWidths=[4*inch])
                signature_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (0, 0), 10),
                    ('FONTSIZE', (0, 2), (0, 2), 9),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LINEABOVE', (0, 2), (0, 2), 1, colors.black),
                ]))
                
                elements.append(signature_table)
            else:
                # Placeholder signature - show text instead
                signature_text = Paragraph(
                    f"<b>Firmado digitalmente por:</b><br/>{checklist_response.completed_by.get_full_name() if checklist_response.completed_by else 'N/A'}",
                    normal_style
                )
                elements.append(signature_text)
            
        except Exception as e:
            # Fallback if signature image cannot be processed
            signature_text = Paragraph(
                f"<b>Firmado digitalmente por:</b><br/>{checklist_response.completed_by.get_full_name() if checklist_response.completed_by else 'N/A'}",
                normal_style
            )
            elements.append(signature_text)
    
    # Footer with generation date
    elements.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer_text = Paragraph(
        f"Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema CMMS",
        footer_style
    )
    elements.append(footer_text)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    
        # Save PDF to file
        filename = f"checklist_{checklist_response.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_file = ContentFile(pdf_content, name=filename)
        
        return pdf_file
        
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error generating PDF for checklist {checklist_response.id}: {str(e)}")
        
        # Re-raise the exception so it can be handled by the caller
        raise Exception(f"Error generando PDF: {str(e)}")


def _add_section_table(elements, section_items):
    """Helper function to add a section table to elements."""
    # Add header row
    table_data = [['#', 'Pregunta', 'Respuesta', 'Observaciones']]
    table_data.extend(section_items)
    
    # Create table
    col_widths = [0.4*inch, 3.5*inch, 1*inch, 2.5*inch]
    section_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Style the table
    table_style = TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ])
    
    section_table.setStyle(table_style)
    elements.append(section_table)
    elements.append(Spacer(1, 0.2*inch))


def _format_response_value(response_value):
    """Format response value for display in PDF."""
    if not response_value:
        return '-'
    
    response_map = {
        'yes': '✓ Sí',
        'no': '✗ No',
        'na': '○ N/A'
    }
    
    return response_map.get(response_value.lower(), response_value)
