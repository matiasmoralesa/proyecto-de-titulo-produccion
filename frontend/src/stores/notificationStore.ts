/**
 * Notification store using Zustand
 */
import { create } from 'zustand';
import { Notification } from '../types/notification';
import { notificationService } from '../services/notificationService';

interface NotificationStore {
  notifications: Notification[];
  unreadCount: number;
  loading: boolean;
  error: string | null;
  
  // Actions
  fetchNotifications: () => Promise<void>;
  fetchUnreadCount: () => Promise<void>;
  markAsRead: (id: number) => Promise<void>;
  markAllAsRead: () => Promise<void>;
  startPolling: () => void;
  stopPolling: () => void;
}

let pollingInterval: NodeJS.Timeout | null = null;

export const useNotificationStore = create<NotificationStore>((set, get) => ({
  notifications: [],
  unreadCount: 0,
  loading: false,
  error: null,

  fetchNotifications: async () => {
    try {
      set({ loading: true, error: null });
      const notifications = await notificationService.getNotifications();
      set({ notifications, loading: false });
    } catch (error: any) {
      set({ error: error.message || 'Error fetching notifications', loading: false });
    }
  },

  fetchUnreadCount: async () => {
    try {
      const count = await notificationService.getUnreadCount();
      set({ unreadCount: count });
    } catch (error: any) {
      console.error('Error fetching unread count:', error);
    }
  },

  markAsRead: async (id: number) => {
    try {
      await notificationService.markAsRead(id);
      
      // Update local state
      set((state) => ({
        notifications: state.notifications.map((n) =>
          n.id === id ? { ...n, is_read: true } : n
        ),
        unreadCount: Math.max(0, state.unreadCount - 1),
      }));
    } catch (error: any) {
      console.error('Error marking notification as read:', error);
    }
  },

  markAllAsRead: async () => {
    try {
      await notificationService.markAllAsRead();
      
      // Update local state
      set((state) => ({
        notifications: state.notifications.map((n) => ({ ...n, is_read: true })),
        unreadCount: 0,
      }));
    } catch (error: any) {
      console.error('Error marking all notifications as read:', error);
    }
  },

  startPolling: () => {
    // Fetch immediately
    get().fetchUnreadCount();
    
    // Then poll every 30 seconds
    if (!pollingInterval) {
      pollingInterval = setInterval(() => {
        get().fetchUnreadCount();
      }, 30000); // 30 seconds
    }
  },

  stopPolling: () => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
  },
}));
