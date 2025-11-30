"""
Comando para obtener actualizaciones del bot de Telegram (chat_ids)
"""
from django.core.management.base import BaseCommand
from apps.omnichannel_bot.models import ChannelConfig
import requests


class Command(BaseCommand):
    help = 'Obtiene las últimas actualizaciones del bot de Telegram para ver chat_ids'
    
    def handle(self, *args, **options):
        try:
            config = ChannelConfig.objects.get(channel_type='TELEGRAM')
            
            if not config.is_enabled:
                self.stdout.write(
                    self.style.WARNING('⚠️  El canal de Telegram no está habilitado')
                )
                return
            
            bot_token = config.config.get('bot_token')
            api_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
            
            self.stdout.write('\n📥 Obteniendo actualizaciones del bot...\n')
            
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                updates = data.get('result', [])
                
                if not updates:
                    self.stdout.write(
                        self.style.WARNING(
                            '⚠️  No hay mensajes nuevos.\n'
                            '   Asegúrate de haber enviado /start al bot en Telegram.\n'
                        )
                    )
                    return
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Se encontraron {len(updates)} actualizaciones\n')
                )
                
                # Mostrar información de cada usuario que ha contactado al bot
                users_seen = set()
                
                for update in updates:
                    message = update.get('message', {})
                    from_user = message.get('from', {})
                    chat = message.get('chat', {})
                    
                    chat_id = chat.get('id')
                    username = from_user.get('username', 'Sin username')
                    first_name = from_user.get('first_name', '')
                    last_name = from_user.get('last_name', '')
                    full_name = f"{first_name} {last_name}".strip()
                    text = message.get('text', '')
                    
                    if chat_id and chat_id not in users_seen:
                        users_seen.add(chat_id)
                        
                        self.stdout.write('─' * 60)
                        self.stdout.write(
                            self.style.SUCCESS(f'\n👤 Usuario: {full_name}')
                        )
                        self.stdout.write(f'   Username: @{username}')
                        self.stdout.write(
                            self.style.WARNING(f'   Chat ID: {chat_id}')
                        )
                        self.stdout.write(f'   Último mensaje: "{text}"')
                        self.stdout.write('')
                
                self.stdout.write('─' * 60)
                self.stdout.write(
                    '\n📝 Para configurar un usuario:\n'
                    '1. Ve a Django Admin > Omnichannel Bot > User Channel Preferences\n'
                    '2. Crea nueva preferencia:\n'
                    '   - User: Selecciona el usuario del sistema\n'
                    '   - Channel type: TELEGRAM\n'
                    '   - Is enabled: ✓\n'
                    '   - Channel user id: Pega el Chat ID de arriba\n'
                    '   - Notify work orders: ✓\n'
                    '   - Notify predictions: ✓\n'
                )
                
                self.stdout.write(
                    '\n💡 O prueba enviar un mensaje directo:\n'
                    f'   python manage.py test_telegram_bot --chat-id {list(users_seen)[0] if users_seen else "CHAT_ID"}\n'
                )
            
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Error al obtener actualizaciones: {response.text}'
                    )
                )
        
        except ChannelConfig.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Canal de Telegram no configurado.\n'
                    '   Ejecuta: python manage.py setup_telegram_bot --token TOKEN --enable'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
