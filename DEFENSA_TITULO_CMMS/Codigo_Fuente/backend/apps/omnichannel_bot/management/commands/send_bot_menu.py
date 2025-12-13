"""
Comando para enviar el menú principal del bot a un usuario
"""
from django.core.management.base import BaseCommand
from apps.omnichannel_bot.models import ChannelConfig, UserChannelPreference
from apps.omnichannel_bot.channels.telegram import TelegramChannel
from apps.omnichannel_bot.bot_commands import BotCommandHandler
from apps.authentication.models import User


class Command(BaseCommand):
    help = 'Envía el menú principal del bot a un usuario'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username del usuario'
        )
        parser.add_argument(
            '--chat-id',
            type=str,
            help='Chat ID directo'
        )
    
    def handle(self, *args, **options):
        username = options.get('username')
        chat_id = options.get('chat_id')
        
        if not username and not chat_id:
            self.stdout.write(
                self.style.ERROR('Debes proporcionar --username o --chat-id')
            )
            return
        
        try:
            config = ChannelConfig.objects.get(channel_type='TELEGRAM', is_enabled=True)
            telegram = TelegramChannel(config.config)
            
            if not telegram.is_configured:
                self.stdout.write(
                    self.style.ERROR('❌ Bot de Telegram no configurado correctamente')
                )
                return
            
            # Obtener chat_id
            if username:
                try:
                    user = User.objects.get(username=username)
                    preference = UserChannelPreference.objects.get(
                        user=user,
                        channel_type='TELEGRAM'
                    )
                    chat_id = preference.channel_user_id
                    self.stdout.write(f'\n👤 Usuario: {user.get_full_name() or user.username}')
                except (User.DoesNotExist, UserChannelPreference.DoesNotExist):
                    self.stdout.write(
                        self.style.ERROR(f'❌ Usuario "{username}" no encontrado o no configurado para Telegram')
                    )
                    return
            
            self.stdout.write(f'📤 Enviando menú a chat_id: {chat_id}\n')
            
            # Generar menú
            handler = BotCommandHandler()
            response = handler.cmd_start(user if username else None)
            
            # Enviar mensaje
            result = telegram.send_message(
                chat_id=chat_id,
                title='',
                message=response['text'],
                reply_markup={'inline_keyboard': response.get('buttons', [])} if response.get('buttons') else None
            )
            
            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Menú enviado exitosamente!\n'
                        f'  Message ID: {result.get("message_id")}\n'
                    )
                )
                self.stdout.write(
                    '\n💡 El usuario puede ahora:\n'
                    '   • Usar los botones del menú\n'
                    '   • Enviar comandos como /help, /status, /workorders\n'
                    '   • Interactuar con el bot\n'
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error: {result.get("error")}\n')
                )
        
        except ChannelConfig.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Canal de Telegram no configurado')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
