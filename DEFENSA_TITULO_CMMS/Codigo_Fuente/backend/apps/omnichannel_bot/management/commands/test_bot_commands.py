"""
Comando para probar los comandos del bot localmente
"""
from django.core.management.base import BaseCommand
from apps.omnichannel_bot.bot_commands import BotCommandHandler
from apps.authentication.models import User


class Command(BaseCommand):
    help = 'Prueba los comandos del bot localmente'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--command',
            type=str,
            default='/help',
            help='Comando a probar (ej: /help, /status, /workorders)'
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username del usuario para probar comandos personalizados'
        )
    
    def handle(self, *args, **options):
        command = options['command']
        username = options.get('username')
        
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(f'\n👤 Usuario: {user.get_full_name() or user.username}\n')
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Usuario "{username}" no encontrado\n')
                )
                return
        
        self.stdout.write(f'🤖 Probando comando: {command}\n')
        self.stdout.write('─' * 60 + '\n')
        
        handler = BotCommandHandler()
        response = handler.handle_command(command, user)
        
        # Mostrar respuesta
        self.stdout.write(response['text'])
        
        # Mostrar botones si existen
        if response.get('buttons'):
            self.stdout.write('\n\n🔘 Botones disponibles:')
            for row in response['buttons']:
                for button in row:
                    self.stdout.write(f"   [{button['text']}] -> {button['callback_data']}")
        
        self.stdout.write('\n' + '─' * 60 + '\n')
        
        # Sugerencias
        self.stdout.write(
            '\n💡 Otros comandos para probar:\n'
            '   /start, /help, /status, /workorders, /predictions, /assets, /myinfo\n'
        )
