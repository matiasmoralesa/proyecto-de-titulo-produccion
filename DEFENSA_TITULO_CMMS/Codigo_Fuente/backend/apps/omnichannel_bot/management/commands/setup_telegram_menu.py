"""
Comando para configurar el menú de comandos del bot de Telegram
"""
from django.core.management.base import BaseCommand
import requests
from apps.omnichannel_bot.models import ChannelConfig


class Command(BaseCommand):
    help = 'Configura el menú de comandos del bot de Telegram'
    
    def handle(self, *args, **options):
        try:
            # Obtener configuración del bot
            config = ChannelConfig.objects.get(channel_type='TELEGRAM', is_enabled=True)
            bot_token = config.config.get('bot_token', '')
            
            if not bot_token:
                self.stdout.write(
                    self.style.ERROR('❌ Bot token no configurado')
                )
                return
            
            # Definir comandos del menú
            commands = [
                {"command": "start", "description": "🏠 Iniciar el bot"},
                {"command": "workorders", "description": "📋 Ver mis órdenes de trabajo"},
                {"command": "predictions", "description": "⚠️ Ver predicciones de alto riesgo"},
                {"command": "assets", "description": "🔧 Ver estado de activos"},
                {"command": "status", "description": "📊 Estado general del sistema"},
                {"command": "myinfo", "description": "👤 Ver mi información"},
                {"command": "help", "description": "❓ Ver ayuda y comandos"},
            ]
            
            self.stdout.write('\n📋 Configurando menú de comandos del bot...\n')
            
            # Enviar comandos a Telegram
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/setMyCommands",
                json={"commands": commands},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    self.stdout.write(
                        self.style.SUCCESS('\n✅ Menú de comandos configurado exitosamente!\n')
                    )
                    self.stdout.write('\n📱 Comandos disponibles:\n')
                    for cmd in commands:
                        self.stdout.write(f"   /{cmd['command']} - {cmd['description']}")
                    
                    self.stdout.write(
                        '\n\n💡 Los usuarios ahora verán estos comandos al escribir "/" en el chat.\n'
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"\n❌ Error: {result.get('description', 'Unknown error')}\n")
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f'\n❌ Error HTTP {response.status_code}: {response.text}\n')
                )
        
        except ChannelConfig.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    '\n❌ Canal de Telegram no configurado.\n'
                    '   Ejecuta: python manage.py setup_telegram_bot --token TOKEN --enable\n'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error: {str(e)}\n')
            )
