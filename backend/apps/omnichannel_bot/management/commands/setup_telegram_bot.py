"""
Comando para configurar el bot de Telegram
"""
from django.core.management.base import BaseCommand
from apps.omnichannel_bot.models import ChannelConfig
from decouple import config


class Command(BaseCommand):
    help = 'Configura el bot de Telegram'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--token',
            type=str,
            help='Token del bot de Telegram (opcional, se puede usar variable de entorno TELEGRAM_BOT_TOKEN)'
        )
        parser.add_argument(
            '--enable',
            action='store_true',
            help='Habilitar el canal de Telegram'
        )
    
    def handle(self, *args, **options):
        token = options.get('token') or config('TELEGRAM_BOT_TOKEN', default='')
        
        if not token:
            self.stdout.write(
                self.style.ERROR(
                    '\n❌ No se proporcionó token del bot de Telegram.\n\n'
                    'Opciones:\n'
                    '1. Usar --token: python manage.py setup_telegram_bot --token YOUR_TOKEN\n'
                    '2. Agregar TELEGRAM_BOT_TOKEN en .env\n\n'
                    'Para crear un bot:\n'
                    '1. Habla con @BotFather en Telegram\n'
                    '2. Envía /newbot\n'
                    '3. Sigue las instrucciones\n'
                    '4. Copia el token que te da\n'
                )
            )
            return
        
        self.stdout.write('\n🤖 Configurando bot de Telegram...\n')
        
        # Crear o actualizar configuración
        channel_config, created = ChannelConfig.objects.update_or_create(
            channel_type='TELEGRAM',
            defaults={
                'config': {'bot_token': token},
                'is_enabled': options.get('enable', False)
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Configuración de Telegram creada'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Configuración de Telegram actualizada'))
        
        # Validar conexión
        from apps.omnichannel_bot.channels.telegram import TelegramChannel
        
        telegram = TelegramChannel(channel_config.config)
        
        if telegram.is_configured:
            self.stdout.write(
                self.style.SUCCESS(
                    '\n✓ Bot de Telegram configurado correctamente!\n'
                )
            )
            
            if options.get('enable'):
                self.stdout.write(
                    self.style.SUCCESS('✓ Canal de Telegram HABILITADO\n')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        '⚠️  Canal de Telegram configurado pero NO habilitado.\n'
                        '   Para habilitarlo: python manage.py setup_telegram_bot --enable\n'
                    )
                )
            
            self.stdout.write(
                '\n📝 Próximos pasos:\n'
                '1. Los usuarios deben iniciar chat con el bot en Telegram\n'
                '2. Configurar preferencias de usuario en Django Admin\n'
                '3. Agregar chat_id de Telegram en UserChannelPreference\n\n'
                '💡 Para obtener el chat_id de un usuario:\n'
                '   - El usuario envía /start al bot\n'
                '   - Usa: python manage.py test_telegram_bot\n'
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    '\n❌ Error al validar el bot de Telegram.\n'
                    '   Verifica que el token sea correcto.\n'
                )
            )
