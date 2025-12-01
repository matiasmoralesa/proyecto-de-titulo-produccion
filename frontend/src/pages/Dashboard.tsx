/**
 * Dashboard page component
 */
import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import MainLayout from '../components/layout/MainLayout';
import { FiCheckCircle, FiUser, FiTruck, FiActivity, FiAlertTriangle, FiClock, FiTool } from 'react-icons/fi';
import { FaRobot } from 'react-icons/fa';
import api from '../services/api';
import toast from 'react-hot-toast';

interface DashboardStats {
  total_assets: number;
  operational_assets: number;
  maintenance_assets: number;
  stopped_assets: number;
  total_work_orders: number;
  pending_work_orders: number;
  in_progress_work_orders: number;
  completed_work_orders: number;
  high_risk_predictions: number;
  total_predictions: number;
  kpis?: {
    availability_rate: number;
    completion_rate: number;
    avg_duration_days: number;
    preventive_ratio: number;
    maintenance_backlog: number;
    critical_assets_count: number;
    work_orders_this_month: number;
    prediction_accuracy: number;
  };
}

export default function Dashboard() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await api.get('/dashboard/stats/');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      toast.error('Error al cargar estadísticas');
      // Set default values if API fails
      setStats({
        total_assets: 0,
        operational_assets: 0,
        maintenance_assets: 0,
        stopped_assets: 0,
        total_work_orders: 0,
        pending_work_orders: 0,
        in_progress_work_orders: 0,
        completed_work_orders: 0,
        high_risk_predictions: 0,
        total_predictions: 0,
      });
    } finally {
      setLoading(false);
    }
  };

  // Helper function to check user role
  // Validates: Requirements 10.1, 10.2, 10.3
  const hasRole = (roles: string[]) => {
    if (!user || !user.role) return false;
    return roles.includes(user.role.name);
  };

  const isOperador = hasRole(['OPERADOR']);
  const isSupervisor = hasRole(['SUPERVISOR']);
  const isAdmin = hasRole(['ADMIN']);

  if (loading) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg shadow-lg p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            ¡Bienvenido, {user?.first_name || user?.username}!
          </h1>
          <p className="text-blue-100">
            Sistema de Gestión de Mantenimiento Computarizado (CMMS)
          </p>
        </div>

        {/* Assets Stats - Visible to all roles */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            {isOperador ? 'Mis Activos' : 'Estado de Activos'}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    {isOperador ? 'Mis Activos' : 'Activos Totales'}
                  </p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stats?.total_assets || 0}</p>
                </div>
                <div className="bg-blue-500 p-3 rounded-lg">
                  <FiTruck className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">En Operación</p>
                  <p className="text-3xl font-bold text-green-600 mt-2">{stats?.operational_assets || 0}</p>
                </div>
                <div className="bg-green-500 p-3 rounded-lg">
                  <FiCheckCircle className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">En Mantenimiento</p>
                  <p className="text-3xl font-bold text-yellow-600 mt-2">{stats?.maintenance_assets || 0}</p>
                </div>
                <div className="bg-yellow-500 p-3 rounded-lg">
                  <FiTool className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Detenidos</p>
                  <p className="text-3xl font-bold text-red-600 mt-2">{stats?.stopped_assets || 0}</p>
                </div>
                <div className="bg-red-500 p-3 rounded-lg">
                  <FiAlertTriangle className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Work Orders Stats - Visible to all roles */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            {isOperador ? 'Mis Órdenes de Trabajo' : isSupervisor ? 'Órdenes del Equipo' : 'Órdenes de Trabajo'}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stats?.total_work_orders || 0}</p>
                </div>
                <div className="bg-purple-500 p-3 rounded-lg">
                  <FiActivity className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Pendientes</p>
                  <p className="text-3xl font-bold text-orange-600 mt-2">{stats?.pending_work_orders || 0}</p>
                </div>
                <div className="bg-orange-500 p-3 rounded-lg">
                  <FiClock className="w-6 h-6 text-white" />
                </div>
              </div>
              {isOperador && stats && stats.pending_work_orders > 0 && (
                <p className="text-xs text-orange-600 mt-2 font-medium">
                  ¡Tienes órdenes pendientes!
                </p>
              )}
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">En Progreso</p>
                  <p className="text-3xl font-bold text-blue-600 mt-2">{stats?.in_progress_work_orders || 0}</p>
                </div>
                <div className="bg-blue-500 p-3 rounded-lg">
                  <FiActivity className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Completadas</p>
                  <p className="text-3xl font-bold text-green-600 mt-2">{stats?.completed_work_orders || 0}</p>
                </div>
                <div className="bg-green-500 p-3 rounded-lg">
                  <FiCheckCircle className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* ML Predictions Stats - Only for Supervisors and Admins */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        {(isSupervisor || isAdmin) && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Predicciones ML</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Predicciones</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats?.total_predictions || 0}</p>
                  </div>
                  <div className="bg-indigo-500 p-3 rounded-lg">
                    <FaRobot className="w-6 h-6 text-white" />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Alto Riesgo</p>
                    <p className="text-3xl font-bold text-red-600 mt-2">{stats?.high_risk_predictions || 0}</p>
                  </div>
                  <div className="bg-red-500 p-3 rounded-lg">
                    <FiAlertTriangle className="w-6 h-6 text-white" />
                  </div>
                </div>
                {stats && stats.high_risk_predictions > 0 && (
                  <p className="text-xs text-red-600 mt-2 font-medium">
                    ¡Requiere atención inmediata!
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* KPIs Section - Only for Supervisors and Admins */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        {(isSupervisor || isAdmin) && stats?.kpis && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              {isSupervisor ? 'KPIs del Equipo' : 'Indicadores Clave de Desempeño (KPIs)'}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Availability Rate */}
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-600">Disponibilidad</p>
                  <FiCheckCircle className="text-green-500" />
                </div>
                <p className="text-3xl font-bold text-gray-900">{stats.kpis.availability_rate}%</p>
                <p className="text-xs text-gray-500 mt-1">Activos operacionales</p>
              </div>

              {/* Completion Rate */}
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-600">Tasa de Completitud</p>
                  <FiActivity className="text-blue-500" />
                </div>
                <p className="text-3xl font-bold text-gray-900">{stats.kpis.completion_rate}%</p>
                <p className="text-xs text-gray-500 mt-1">Órdenes completadas</p>
              </div>

              {/* Average Duration */}
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-600">Tiempo Promedio</p>
                  <FiClock className="text-purple-500" />
                </div>
                <p className="text-3xl font-bold text-gray-900">{stats.kpis.avg_duration_days}</p>
                <p className="text-xs text-gray-500 mt-1">Días por orden</p>
              </div>

              {/* Preventive Ratio */}
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-indigo-500">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-600">Mantenimiento Preventivo</p>
                  <FiTool className="text-indigo-500" />
                </div>
                <p className="text-3xl font-bold text-gray-900">{stats.kpis.preventive_ratio}%</p>
                <p className="text-xs text-gray-500 mt-1">vs Correctivo</p>
              </div>

              {/* Maintenance Backlog */}
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-600">Backlog</p>
                  <FiAlertTriangle className="text-orange-500" />
                </div>
                <p className="text-3xl font-bold text-gray-900">{stats.kpis.maintenance_backlog}</p>
                <p className="text-xs text-gray-500 mt-1">Órdenes pendientes</p>
              </div>

              {/* Critical Assets */}
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-600">Activos Críticos</p>
                  <FiAlertTriangle className="text-red-500" />
                </div>
                <p className="text-3xl font-bold text-gray-900">{stats.kpis.critical_assets_count}</p>
                <p className="text-xs text-gray-500 mt-1">Alto riesgo</p>
              </div>

              {/* Work Orders This Month */}
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-teal-500">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-600">OT Este Mes</p>
                  <FiActivity className="text-teal-500" />
                </div>
                <p className="text-3xl font-bold text-gray-900">{stats.kpis.work_orders_this_month}</p>
                <p className="text-xs text-gray-500 mt-1">Nuevas órdenes</p>
              </div>

              {/* Prediction Accuracy */}
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-pink-500">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-600">Precisión ML</p>
                  <FaRobot className="text-pink-500" />
                </div>
                <p className="text-3xl font-bold text-gray-900">{stats.kpis.prediction_accuracy}%</p>
                <p className="text-xs text-gray-500 mt-1">Predicciones acertadas</p>
              </div>
            </div>
          </div>
        )}

        {/* Role-specific Info Cards */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Operador-specific card */}
          {isOperador && (
            <div className="bg-gradient-to-br from-orange-50 to-orange-100 border border-orange-200 rounded-lg p-6">
              <div className="flex items-start space-x-3">
                <FiActivity className="w-6 h-6 text-orange-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-semibold text-orange-900 mb-2">Tus Tareas</h3>
                  <p className="text-sm text-orange-700">
                    Tienes acceso a tus órdenes de trabajo asignadas y los activos relacionados.
                    Mantén tus órdenes actualizadas para un mejor seguimiento.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Supervisor-specific card */}
          {isSupervisor && (
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-lg p-6">
              <div className="flex items-start space-x-3">
                <FiUsers className="w-6 h-6 text-purple-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-semibold text-purple-900 mb-2">Gestión de Equipo</h3>
                  <p className="text-sm text-purple-700">
                    Puedes ver y gestionar todas las órdenes de trabajo de tu equipo.
                    Accede a reportes y predicciones ML para mejor planificación.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Admin-specific card */}
          {isAdmin && (
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-lg p-6">
              <div className="flex items-start space-x-3">
                <FiSettings className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-semibold text-blue-900 mb-2">Control Total</h3>
                  <p className="text-sm text-blue-700">
                    Tienes acceso completo al sistema. Puedes gestionar usuarios, configuración,
                    y ver todas las estadísticas globales del CMMS.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* User Profile Card - All roles */}
          <div className="bg-gradient-to-br from-green-50 to-green-100 border border-green-200 rounded-lg p-6">
            <div className="flex items-start space-x-3">
              <FiUser className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-green-900 mb-2">Tu Perfil</h3>
                <div className="text-sm text-green-700 space-y-1">
                  <p><strong>Usuario:</strong> {user?.username}</p>
                  <p><strong>Email:</strong> {user?.email}</p>
                  <p><strong>Rol:</strong> {user?.role_display}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions - Role-based */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* All roles can view assets */}
            <button
              onClick={() => (window.location.href = '/assets')}
              className="flex items-center space-x-3 p-4 border-2 border-primary-200 rounded-lg hover:border-primary-400 hover:bg-primary-50 transition-colors"
            >
              <FiTruck className="w-6 h-6 text-primary-600" />
              <span className="font-medium text-gray-900">
                {isOperador ? 'Mis Activos' : 'Ver Activos'}
              </span>
            </button>
            
            {/* All roles can view work orders */}
            <button
              onClick={() => (window.location.href = '/work-orders')}
              className="flex items-center space-x-3 p-4 border-2 border-primary-200 rounded-lg hover:border-primary-400 hover:bg-primary-50 transition-colors"
            >
              <FiActivity className="w-6 h-6 text-primary-600" />
              <span className="font-medium text-gray-900">
                {isOperador ? 'Mis Órdenes' : 'Ver Órdenes'}
              </span>
            </button>

            {/* Supervisors and Admins can view reports */}
            {(isSupervisor || isAdmin) && (
              <button
                onClick={() => (window.location.href = '/reports')}
                className="flex items-center space-x-3 p-4 border-2 border-primary-200 rounded-lg hover:border-primary-400 hover:bg-primary-50 transition-colors"
              >
                <FiBarChart2 className="w-6 h-6 text-primary-600" />
                <span className="font-medium text-gray-900">Ver Reportes</span>
              </button>
            )}

            {/* Admins can access configuration */}
            {isAdmin && (
              <button
                onClick={() => (window.location.href = '/configuration')}
                className="flex items-center space-x-3 p-4 border-2 border-primary-200 rounded-lg hover:border-primary-400 hover:bg-primary-50 transition-colors"
              >
                <FiSettings className="w-6 h-6 text-primary-600" />
                <span className="font-medium text-gray-900">Configuración</span>
              </button>
            )}

            {/* Placeholder for future features */}
            <button className="flex items-center space-x-3 p-4 border-2 border-gray-200 rounded-lg hover:border-gray-400 hover:bg-gray-50 transition-colors opacity-50 cursor-not-allowed">
              <FiCheckCircle className="w-6 h-6 text-gray-400" />
              <span className="font-medium text-gray-500">Nuevo Checklist</span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
