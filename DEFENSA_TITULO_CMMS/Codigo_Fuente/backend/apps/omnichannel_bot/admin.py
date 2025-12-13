"""
Admin para el bot omnicanal
"""
from django.contrib import admin
from .models import ChannelConfig, UserChannelPreference, MessageLog


@admin.register(ChannelConfig)
class ChannelConfigAdmin(admin.ModelAdmin):
    list_display = ['channel_type', 'is_enabled', 'messages_sent', 'messages_failed', 'last_used']
    list_filter = ['channel_type', 'is_enabled']
    search_fields = ['channel_type']
    readonly_fields = ['messages_sent', 'messages_failed', 'last_used', 'created_at', 'updated_at']


@admin.register(UserChannelPreference)
class UserChannelPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'channel_type', 'is_enabled', 'channel_user_id', 'notify_critical_only']
    list_filter = ['channel_type', 'is_enabled', 'notify_critical_only']
    search_fields = ['user__username', 'user__email', 'channel_user_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'channel_type', 'title', 'status', 'message_type', 'created_at']
    list_filter = ['channel_type', 'status', 'message_type', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at', 'sent_at', 'delivered_at', 'read_at']
    date_hierarchy = 'created_at'
