"""
URLs para el bot omnicanal
"""
from django.urls import path
from . import views

app_name = 'omnichannel_bot'

urlpatterns = [
    path('webhook/telegram/', views.telegram_webhook, name='telegram_webhook'),
    path('status/', views.bot_status, name='bot_status'),
]
