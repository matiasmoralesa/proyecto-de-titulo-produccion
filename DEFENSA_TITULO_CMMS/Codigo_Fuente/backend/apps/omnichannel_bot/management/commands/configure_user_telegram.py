"""
Comando para configurar rápidamente un usuario para recibir notificaciones por Telegram
"""
from django.core.management.base import BaseCommand
from apps.omnichannel_bot.models import UserChannelPreference
from apps.authentication.models import User


class Command(BaseCommand):
    help = 'Configura un usuario para recibir notificaciones por Telegram'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help='Username del usuario en el sistema'
        )
        parser.add_argument(
            '--chat-id',
            type=str,
            required=True,
            help='Chat ID de Telegram del usuario'
        )
        parser.add_argument(
            '--critical-only',
            action='store_true',
            help='Solo enviar notificaciones críticas'
        )
    
    def handle(self, *args, **options):
        username = options['username']
        chat_id = options['chat_id']
        critical_only = options.get('critical_only', False)
        
        try:
            user = User.objects.get(username=username)
            
            # Crear o actualizar preferencia
            preference, created = UserChannelPreference.objects.update_or_create(
                user=user,
                channel_type='TELEGRAM',
                defaults={
                    'is_enabled': True,
                    'channel_user_id': chat_id,
                    'notify_work_orders': True,
                    'notify_predictions': True,
                    'notify_critical_only': critical_only
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Preferencia de Telegram creada para {user.username}\n'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Preferencia de Telegram actualizada para {user.username}\n'
                    )
                )
            
            self.stdout.write(f'   Usuario: {user.get_full_name() or user.username}')
            self.stdout.write(f'   Chat ID: {chat_id}')
            self.stdout.write(f'   Notificaciones de OT: ✓')
            self.stdout.write(f'   Notificaciones de predicciones: ✓')
            self.stdout.write(f'   Solo críticas: {"✓" if critical_only else "✗"}')
            
            # Enviar mensaje de prueba
            self.stdout.write('\n📤 Enviando mensaje de prueba...\n')
            
            from apps.omnichannel_bot.message_router import MessageRouter
            
            router = MessageRouter()
            results = router.send_to_user(
                user=user,
                title='🎉 Configuración Exitosa',
                message=(
                    f'¡Hola {user.get_full_name() or user.username}!\n\n'
                    '✅ Tu cuenta ha sido configurada correctamente.\n\n'
                    'Ahora recibirás notificaciones de:\n'
                    '📋 Órdenes de trabajo asignadas\n'
                    '⚠️ Predicciones de alto riesgo\n'
                    '🚨 Alertas críticas\n'
                    '🔧 Recordatorios de mantenimiento\n\n'
                    '¡El sistema CMMS está listo para mantenerte informado!'
                ),
                message_type='configuration',
                priority='normal'
            )
            
            if results.get('TELEGRAM'):
                self.stdout.write(
                    self.style.SUCCESS(
                        '✓ Mensaje de prueba enviado exitosamente!\n'
                        '  Revisa tu Telegram.\n'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        '✗ Error al enviar mensaje de prueba.\n'
                        '  Verifica el chat_id.\n'
                    )
                )
        
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Usuario "{username}" no encontrado\n')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error: {str(e)}\n')
            )
