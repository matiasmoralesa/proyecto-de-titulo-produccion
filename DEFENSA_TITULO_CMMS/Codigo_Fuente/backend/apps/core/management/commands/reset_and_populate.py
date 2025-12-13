"""
Django management command para limpiar datos de producción y crear datos de muestra.
"""
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Limpia todos los datos y crea datos de muestra nuevos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='No solicitar confirmación',
        )

    def handle(self, *args, **options):
        # Obtener la ruta del script
        # __file__ está en backend/apps/core/management/commands/reset_and_populate.py
        # Necesitamos ir a backend/scripts/reset_and_populate_data.py
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        script_path = os.path.join(backend_dir, 'scripts', 'reset_and_populate_data.py')
        
        if not os.path.exists(script_path):
            self.stdout.write(self.style.ERROR(f"Script no encontrado: {script_path}"))
            return
        
        # Leer y ejecutar el script
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # Reemplazar la llamada a input() si es --no-input
            if options['no_input']:
                script_content = script_content.replace(
                    'response = input("⚠️  ADVERTENCIA: Este script eliminará TODOS los datos existentes.\\n¿Desea continuar? (escriba \'SI\' para confirmar): ")',
                    'response = "SI"'
                )
            
            # Crear un contexto con __file__ definido
            script_globals = {
                '__name__': '__main__',
                '__file__': script_path,
            }
            
            # Ejecutar el script en el contexto
            exec(script_content, script_globals)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error ejecutando el script: {e}"))
            import traceback
            traceback.print_exc()
            raise
