"""
Comando para probar el bot de Telegram
"""
from django.core.management.base import BaseCommand
from apps.omnichannel_bot.message_router import MessageRouter
from apps.authentication.models import User


class Command(BaseCommand):
    help = 'Prueba el envío de mensajes por Telegram'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username del usuario para enviar mensaje de prueba'
        )
        parser.add_argument(
            '--chat-id',
            type=str,
            help='Chat ID de Telegram para enviar mensaje directo'
        )
    
    def handle(self, *args, **options):
        username = options.get('username')
        chat_id = options.get('chat_id')
        
        if not username and not chat_id:
            self.stdout.write(
                self.style.ERROR(
                    'Debes proporcionar --username o --chat-id'
                )
            )
            return
        
        router = MessageRouter()
        
        if not router.channels.get('TELEGRAM'):
            self.stdout.write(
                self.style.ERROR(
                    '❌ Canal de Telegram no está configurado o habilitado.\n'
                    '   Ejecuta: python manage.py setup_telegram_bot --enable'
                )
            )
            return
        
        # Envío directo con chat_id
        if chat_id:
            self.stdout.write(f'\n📤 Enviando mensaje de prueba a chat_id: {chat_id}...\n')
            
            telegram = router.channels['TELEGRAM']
            result = telegram.send_message(
                chat_id=chat_id,
                title='🤖 Prueba de Bot CMMS',
                message=(
                    '¡Hola! Este es un mensaje de prueba del sistema CMMS.\n\n'
                    '✅ El bot está funcionando correctamente.\n'
                    '📋 Ahora puedes recibir notificaciones de:\n'
                    '  • Órdenes de trabajo asignadas\n'
                    '  • Alertas de predicción ML\n'
                    '  • Recordatorios de mantenimiento\n'
                    '  • Notificaciones críticas'
                )
            )
            
            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Mensaje enviado exitosamente!\n'
                        f'  Message ID: {result.get("message_id")}\n'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'\n❌ Error al enviar mensaje: {result.get("error")}\n'
                    )
                )
            return
        
        # Envío a usuario
        try:
            user = User.objects.get(username=username)
            
            self.stdout.write(f'\n📤 Enviando mensaje de prueba a {user.username}...\n')
            
            results = router.send_to_user(
                user=user,
                title='🤖 Prueba de Bot CMMS',
                message=(
                    f'¡Hola {user.get_full_name() or user.username}!\n\n'
                    'Este es un mensaje de prueba del sistema CMMS.\n\n'
                    '✅ El bot está funcionando correctamente.\n'
                    '📋 Ahora puedes recibir notificaciones de:\n'
                    '  • Órdenes de trabajo asignadas\n'
                    '  • Alertas de predicción ML\n'
                    '  • Recordatorios de mantenimiento\n'
                    '  • Notificaciones críticas'
                ),
                message_type='test',
                priority='normal'
            )
            
            if results:
                for channel, success in results.items():
                    if success:
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Enviado por {channel}')
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'✗ Error en {channel}')
                        )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        '\n⚠️  No se enviaron mensajes.\n'
                        '   Verifica que el usuario tenga preferencias de canal configuradas.\n'
                    )
                )
        
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuario {username} no encontrado')
            )
