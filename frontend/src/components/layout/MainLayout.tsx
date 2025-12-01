/**
 * Main layout component with sidebar navigation
 */
import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import {
  FiHome,
  FiTruck,
  FiClipboard,
  FiTool,
  FiPackage,
  FiCheckSquare,
  FiBell,
  FiBarChart2,
  FiSettings,
  FiMapPin,
  FiUsers,
  FiActivity,
  FiMenu,
  FiX,
  FiLogOut,
  FiUser,
} from 'react-icons/fi';
import { FaRobot, FaClock } from 'react-icons/fa';
import NotificationBell from '../notifications/NotificationBell';
import Breadcrumbs from '../common/Breadcrumbs';
import GlobalSearch from '../common/GlobalSearch';

interface MainLayoutProps {
  children: React.ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  // Menu items with role requirements
  // Validates: Requirements 10.4
  const allMenuItems = [
    { icon: FiHome, label: 'Dashboard', path: '/dashboard', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FiTruck, label: 'Activos', path: '/assets', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FiClipboard, label: 'Órdenes de Trabajo', path: '/work-orders', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FiTool, label: 'Mantenimiento', path: '/maintenance', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FiPackage, label: 'Inventario', path: '/inventory', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FiCheckSquare, label: 'Checklists', path: '/checklists', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FiActivity, label: 'Estado de Máquinas', path: '/machine-status', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FaRobot, label: 'Predicciones ML', path: '/ml-predictions', roles: ['ADMIN', 'SUPERVISOR'] },
    { icon: FaClock, label: 'Monitor Celery', path: '/celery-monitor', roles: ['ADMIN'] },
    { icon: FiBell, label: 'Notificaciones', path: '/notifications', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FiBarChart2, label: 'Reportes', path: '/reports', roles: ['ADMIN', 'SUPERVISOR', 'OPERADOR'] },
    { icon: FiMapPin, label: 'Ubicaciones', path: '/locations', roles: ['ADMIN', 'SUPERVISOR'] },
    { icon: FiUsers, label: 'Usuarios', path: '/users', roles: ['ADMIN', 'SUPERVISOR'] },
    { icon: FiSettings, label: 'Configuración', path: '/configuration', roles: ['ADMIN'] },
  ];

  // Filter menu items based on user role
  const menuItems = allMenuItems.filter(item => {
    if (!user || !user.role) return false;
    return item.roles.includes(user.role.name);
  });

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-gradient-to-b from-primary-800 to-primary-900 text-white transform transition-transform duration-300 ease-in-out ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Logo */}
        <div className="flex items-center justify-between h-16 px-6 bg-primary-900">
          <div className="flex items-center space-x-3">
            <FiTool className="w-8 h-8" />
            <span className="text-xl font-bold">CMMS</span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden text-white hover:text-gray-300"
          >
            <FiX className="w-6 h-6" />
          </button>
        </div>

        {/* User Info */}
        <div className="px-6 py-4 bg-primary-900/50 border-b border-primary-700">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center">
              <FiUser className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user?.username}</p>
              <p className="text-xs text-primary-300 truncate">{user?.role_display}</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);
            const disabled = false; // Todas las páginas están habilitadas

            return (
              <button
                key={item.path}
                onClick={() => !disabled && navigate(item.path)}
                disabled={disabled}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  active
                    ? 'bg-primary-700 text-white'
                    : disabled
                    ? 'text-primary-400 cursor-not-allowed opacity-50'
                    : 'text-primary-100 hover:bg-primary-700/50'
                }`}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                <span className="text-sm font-medium">{item.label}</span>
                {disabled && (
                  <span className="ml-auto text-xs bg-primary-700 px-2 py-1 rounded">
                    Próximo
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Logout Button */}
        <div className="p-4 border-t border-primary-700">
          <button
            onClick={handleLogout}
            className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-primary-100 hover:bg-red-600 transition-colors"
          >
            <FiLogOut className="w-5 h-5" />
            <span className="text-sm font-medium">Cerrar Sesión</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div
        className={`transition-all duration-300 ${
          sidebarOpen ? 'lg:ml-64' : 'ml-0'
        }`}
      >
        {/* Top Bar */}
        <header className="bg-white shadow-sm sticky top-0 z-40">
          <div className="flex items-center justify-between h-16 px-6">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-600 hover:text-gray-900"
            >
              <FiMenu className="w-6 h-6" />
            </button>

            <div className="flex items-center space-x-4">
              <GlobalSearch />
              <NotificationBell />
              <span className="hidden md:block text-sm text-gray-600">
                {new Date().toLocaleDateString('es-ES', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </span>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="p-6">
          <Breadcrumbs />
          {children}
        </main>
      </div>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
