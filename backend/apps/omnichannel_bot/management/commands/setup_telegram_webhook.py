"""
Comando para configurar el webhook de Telegram
"""
from django.core.management.base import BaseCommand
from apps.omnichannel_bot.models import ChannelConfig
import requests


class Command(BaseCommand):
    help = 'Configura el webhook de Telegram para recibir mensajes'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            required=True,
            help='URL pública del webhook (ej: https://tudominio.com/api/v1/bot/webhook/telegram/)'
        )
        parser.add_argument(
            '--remove',
            action='store_true',
            help='Eliminar el webhook'
        )
    
    def handle(self, *args, **options):
        webhook_url = options.get('url')
        remove = options.get('remove', False)
        
        try:
            config = ChannelConfig.objects.get(channel_type='TELEGRAM')
            bot_token = config.config.get('bot_token')
            
            if not bot_token:
                self.stdout.write(
                    self.style.ERROR('❌ Token del bot no configurado')
                )
                return
            
            api_url = f"https://api.telegram.org/bot{bot_token}"
            
            if remove:
                # Eliminar webhook
                self.stdout.write('\n🗑️  Eliminando webhook...\n')
                response = requests.post(f"{api_url}/deleteWebhook")
                
                if response.status_code == 200:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Webhook eliminado exitosamente\n')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error: {response.text}\n')
                    )
                return
            
            # Configurar webhook
            self.stdout.write(f'\n🔗 Configurando webhook: {webhook_url}\n')
            
            response = requests.post(
                f"{api_url}/setWebhook",
                json={'url': webhook_url}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('ok'):
                    self.stdout.write(
                        self.style.SUCCESS(
                            '✓ Webhook configurado exitosamente!\n'
                        )
                    )
                    
                    # Verificar webhook
                    info_response = requests.get(f"{api_url}/getWebhookInfo")
                    if info_response.status_code == 200:
                        info = info_response.json().get('result', {})
                        
                        self.stdout.write('\n📊 Información del Webhook:\n')
                        self.stdout.write(f"   URL: {info.get('url')}")
                        self.stdout.write(f"   Pending updates: {info.get('pending_update_count', 0)}")
                        
                        if info.get('last_error_message'):
                            self.stdout.write(
                                self.style.WARNING(
                                    f"   Último error: {info.get('last_error_message')}"
                                )
                            )
                    
                    self.stdout.write(
                        '\n💡 Ahora el bot puede recibir mensajes y responder a comandos.\n'
                        '   Prueba enviando /start al bot en Telegram.\n'
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Error al configurar webhook: {result.get("description")}\n'
                        )
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error HTTP: {response.status_code}\n')
                )
        
        except ChannelConfig.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Canal de Telegram no configurado.\n'
                    '   Ejecuta: python manage.py setup_telegram_bot --token TOKEN --enable\n'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}\n')
            )
