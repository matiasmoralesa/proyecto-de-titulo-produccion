/**
 * Notifications page - Full list of notifications
 */
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MainLayout from '../components/layout/MainLayout';
import { useNotificationStore } from '../stores/notificationStore';
import { Notification } from '../types/notification';
import api from '../services/api';
import toast from 'react-hot-toast';

const NotificationsPage: React.FC = () => {
  const navigate = useNavigate();
  const [filter, setFilter] = useState<'all' | 'unread'>('all');
  
  const {
    notifications,
    loading,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
  } = useNotificationStore();

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  const filteredNotifications = filter === 'unread'
    ? notifications.filter(n => !n.is_read)
    : notifications;

  const getNotificationIcon = (type: string) => {
    const icons: Record<string, string> = {
      work_order_created: '📋',
      work_order_assigned: '👤',
      work_order_updated: '🔄',
      work_order_completed: '✅',
      asset_status_changed: '🚛',
      maintenance_due: '⚠️',
      low_stock: '📦',
      system: '🔔',
    };
    return icons[type] || '🔔';
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleNotificationClick = async (notification: Notification) => {
    // Mark as read first
    markAsRead(notification.id);
    
    // If no related object, just return
    if (!notification.related_object_type || !notification.related_object_id) {
      return;
    }

    try {
      // Navigate to the appropriate page
      if (notification.related_object_type === 'work_order') {
        // Navigate to work orders page - the user can find the specific order there
        navigate('/work-orders');
      } else if (notification.related_object_type === 'asset') {
        // Navigate to asset detail page
        await api.get(`/assets/assets/${notification.related_object_id}/`);
        navigate(`/assets/${notification.related_object_id}`);
      } else if (notification.related_object_type === 'prediction') {
        // Navigate to ML predictions page
        navigate('/ml-predictions');
      } else {
        // For other types, stay on notifications page
        return;
      }
    } catch (error: any) {
      // Object doesn't exist or API error
      console.error('Error navigating from notification:', error);
      
      if (error.response?.status === 404) {
        toast.error('El objeto relacionado ya no existe');
        // Navigate to the general page anyway
        if (notification.related_object_type === 'work_order') {
          navigate('/work-orders');
        } else if (notification.related_object_type === 'asset') {
          navigate('/assets');
        }
      } else {
        toast.error('Error al cargar el objeto relacionado');
      }
    }
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;

  return (
    <MainLayout>
      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Notificaciones</h1>
              <p className="text-sm text-gray-600 mt-1">
                {unreadCount > 0 ? `${unreadCount} sin leer` : 'Todas leídas'}
              </p>
            </div>
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Marcar todas como leídas
              </button>
            )}
          </div>

          {/* Filters */}
          <div className="flex space-x-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                filter === 'all'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              Todas ({notifications.length})
            </button>
            <button
              onClick={() => setFilter('unread')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                filter === 'unread'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              Sin leer ({unreadCount})
            </button>
          </div>
        </div>

        {/* Notifications List */}
        {loading ? (
          <div className="flex justify-center items-center p-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : filteredNotifications.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <div className="text-6xl mb-4">🔔</div>
            <p className="text-gray-500 text-lg">
              {filter === 'unread' ? 'No hay notificaciones sin leer' : 'No hay notificaciones'}
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {filteredNotifications.map((notification) => (
              <div
                key={notification.id}
                onClick={() => handleNotificationClick(notification)}
                className={`bg-white rounded-lg shadow hover:shadow-md transition-all cursor-pointer ${
                  !notification.is_read ? 'border-l-4 border-blue-600' : ''
                }`}
              >
                <div className="p-6">
                  <div className="flex items-start space-x-4">
                    <span className="text-3xl flex-shrink-0">
                      {getNotificationIcon(notification.notification_type)}
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className={`text-lg ${!notification.is_read ? 'font-semibold' : 'font-medium'} text-gray-900`}>
                          {notification.title}
                        </h3>
                        {!notification.is_read && (
                          <span className="ml-2 w-3 h-3 bg-blue-600 rounded-full flex-shrink-0"></span>
                        )}
                      </div>
                      <p className="text-gray-700 mb-3">
                        {notification.message}
                      </p>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>{formatDate(notification.created_at)}</span>
                        {notification.related_object_type && (
                          <span className="px-2 py-1 bg-gray-100 rounded text-xs">
                            {notification.related_object_type}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default NotificationsPage;
