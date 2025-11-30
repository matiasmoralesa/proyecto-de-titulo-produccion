from apps.omnichannel_bot.models import MessageLog

logs = MessageLog.objects.filter(channel_type='TELEGRAM').order_by('-created_at')[:10]

print(f'\n📱 Mensajes enviados por Telegram: {logs.count()}\n')

for i, log in enumerate(logs, 1):
    status_icon = '✓' if log.status == 'SENT' else '✗'
    print(f'{i}. {status_icon} {log.title}')
    print(f'   Usuario: {log.user.username}')
    print(f'   Estado: {log.status}')
    print(f'   Hora: {log.created_at.strftime("%H:%M:%S")}')
    print()
