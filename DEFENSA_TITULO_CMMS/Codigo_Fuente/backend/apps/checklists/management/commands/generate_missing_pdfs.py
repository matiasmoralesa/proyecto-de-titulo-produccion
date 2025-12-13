from django.core.management.base import BaseCommand
from apps.checklists.models import ChecklistResponse
from apps.checklists.services import generate_checklist_pdf


class Command(BaseCommand):
    help = 'Generate PDFs for checklists that are missing them'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Generando PDFs faltantes...")
        self.stdout.write("=" * 60)
        
        # Get all completed checklists without PDFs
        checklists_without_pdf = ChecklistResponse.objects.filter(
            pdf_file=''
        ).exclude(status='IN_PROGRESS')
        
        total = checklists_without_pdf.count()
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS("✅ Todos los checklists ya tienen PDF"))
            return
        
        self.stdout.write(f"📋 Encontrados {total} checklists sin PDF")
        self.stdout.write("")
        
        generated = 0
        failed = 0
        
        for checklist in checklists_without_pdf:
            try:
                # Generate PDF
                pdf_file = generate_checklist_pdf(checklist)
                checklist.pdf_file = pdf_file
                checklist.save()
                
                self.stdout.write(self.style.SUCCESS(
                    f"✅ PDF generado para checklist #{checklist.id} - {checklist.template.code}"
                ))
                generated += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"❌ Error generando PDF para checklist #{checklist.id}: {str(e)}"
                ))
                failed += 1
        
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS(f"🎉 PDFs generados: {generated}"))
        
        if failed > 0:
            self.stdout.write(self.style.WARNING(f"⚠️  Fallos: {failed}"))
        
        self.stdout.write(f"\n📊 Total procesados: {generated + failed}/{total}")
