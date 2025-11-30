/**
 * Service for Notification API operations
 */
import api from './api';
import { Notification, NotificationPreference } from '../types/notification';

const NOTIFICATION_BASE_URL = '/notifications';

export const notificationService = {
  // Notification endpoints
  async getNotifications(filters?: { notification_type?: string; is_read?: boolean }): Promise<Notification[]> {
    const response = await api.get(`${NOTIFICATION_BASE_URL}/notifications/`, { params: filters });
    return response.data.results || response.data;
  },

  async getNotification(id: number): Promise<Notification> {
    const response = await api.get(`${NOTIFICATION_BASE_URL}/notifications/${id}/`);
    return response.data;
  },

  async markAsRead(id: number): Promise<Notification> {
    const response = await api.post(`${NOTIFICATION_BASE_URL}/notifications/${id}/mark_as_read/`);
    return response.data;
  },

  async markAllAsRead(): Promise<{ message: string; count: number }> {
    const response = await api.post(`${NOTIFICATION_BASE_URL}/notifications/mark_all_as_read/`);
    return response.data;
  },

  async getUnreadCount(): Promise<number> {
    const response = await api.get(`${NOTIFICATION_BASE_URL}/notifications/unread_count/`);
    return response.data.count;
  },

  // Preference endpoints
  async getPreferences(): Promise<NotificationPreference> {
    const response = await api.get(`${NOTIFICATION_BASE_URL}/preferences/`);
    return response.data;
  },

  async updatePreferences(preferences: Partial<NotificationPreference>): Promise<NotificationPreference> {
    const response = await api.patch(`${NOTIFICATION_BASE_URL}/preferences/`, preferences);
    return response.data;
  },
};
