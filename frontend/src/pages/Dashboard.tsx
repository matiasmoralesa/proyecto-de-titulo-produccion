/**
 * Dashboard page component - Enhanced with charts and improved KPIs
 */
import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import MainLayout from '../components/layout/MainLayout';
import { 
  FiCheckCircle, FiUser, FiTruck, FiActivity, FiAlertTriangle, 
  FiClock, FiTool, FiSettings, FiBarChart2, FiTrendingUp, 
  FiTrendingDown, FiUsers 
} from 'react-icons/fi';
import { FaRobot } from 'react-icons/fa';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  AreaChart, Area
} from 'recharts';
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
  charts?: {
    work_orders_trend?: Array<{ month: string; completed: number; pending: number }>;
    asset_status_distribution?: Array<{ name: string; value: number }>;
    maintenance_types?: Array<{ type: string; count: number }>;
    predictions_timeline?: Array<{ date: string; high_risk: number; medium_risk: number; low_risk: number }>;
  };
}

// Chart colors
const COLORS = {
  primary: '#3B82F6',
  success: '#10B981',
  warning: '#F59E0B',
  danger: '#EF4444',
  purple: '#8B5CF6',
  indigo: '#6366F1',
  pink: '#EC4899',
  teal: '#14B8A6',
};

const PIE_COLORS = [COLORS.success, COLORS.warning, COLORS.danger, COLORS.primary];

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

  // Chart data from API (real data)
  const workOrdersTrend = stats?.charts?.work_orders_trend || [];
  const assetStatusData = stats?.charts?.asset_status_distribution || [];
  const maintenanceTypes = stats?.charts?.maintenance_types || [];
  const predictionsTimeline = stats?.charts?.predictions_timeline || [];

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Enhanced Welcome Section with Quick Stats */}
        <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 rounded-xl shadow-xl p-8 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -mr-32 -mt-32"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-white opacity-5 rounded-full -ml-24 -mb-24"></div>
          
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-4xl font-bold mb-2">
                  ¡Bienvenido, {user?.first_name || user?.username}!
                </h1>
                <p className="text-blue-100 text-lg">
                  Sistema de Gestión de Mantenimiento Computarizado (CMMS)
                </p>
              </div>
              <div className="hidden md:flex items-center space-x-2 bg-white bg-opacity-20 px-4 py-2 rounded-lg backdrop-blur-sm">
                <FiUser className="w-5 h-5" />
                <span className="font-medium">{user?.role_display}</span>
              </div>
            </div>
            
            {/* Quick Stats Row */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
              <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded-lg p-4 border border-white border-opacity-20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-100 text-sm">Activos</p>
                    <p className="text-3xl font-bold mt-1">{stats?.total_assets || 0}</p>
                  </div>
                  <FiTruck className="w-8 h-8 text-blue-200" />
                </div>
              </div>
              
              <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded-lg p-4 border border-white border-opacity-20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-100 text-sm">OT Activas</p>
                    <p className="text-3xl font-bold mt-1">{(stats?.pending_work_orders || 0) + (stats?.in_progress_work_orders || 0)}</p>
                  </div>
                  <FiActivity className="w-8 h-8 text-blue-200" />
                </div>
              </div>
              
              <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded-lg p-4 border border-white border-opacity-20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-100 text-sm">Disponibilidad</p>
                    <p className="text-3xl font-bold mt-1">{stats?.kpis?.availability_rate || 0}%</p>
                  </div>
                  <FiCheckCircle className="w-8 h-8 text-green-300" />
                </div>
              </div>
              
              <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded-lg p-4 border border-white border-opacity-20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-100 text-sm">Alto Riesgo</p>
                    <p className="text-3xl font-bold mt-1">{stats?.high_risk_predictions || 0}</p>
                  </div>
                  <FiAlertTriangle className="w-8 h-8 text-red-300" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced KPIs Grid - Visible to all roles */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-900">
              {isOperador ? 'Mis Activos' : 'Estado de Activos'}
            </h2>
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center">
              Ver detalles <FiTrendingUp className="ml-1" />
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Total Assets Card */}
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl shadow-lg p-6 border border-blue-200 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <div className="bg-blue-500 p-3 rounded-xl shadow-md">
                  <FiTruck className="w-7 h-7 text-white" />
                </div>
                <span className="text-xs font-semibold text-blue-600 bg-blue-200 px-2 py-1 rounded-full">
                  Total
                </span>
              </div>
              <p className="text-sm font-medium text-blue-700 mb-1">
                {isOperador ? 'Mis Activos' : 'Activos Totales'}
              </p>
              <p className="text-4xl font-bold text-blue-900">{stats?.total_assets || 0}</p>
              <div className="mt-3 flex items-center text-xs text-blue-600">
                <FiTrendingUp className="mr-1" />
                <span>100% del inventario</span>
              </div>
            </div>

            {/* Operational Assets Card */}
            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl shadow-lg p-6 border border-green-200 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <div className="bg-green-500 p-3 rounded-xl shadow-md">
                  <FiCheckCircle className="w-7 h-7 text-white" />
                </div>
                <span className="text-xs font-semibold text-green-600 bg-green-200 px-2 py-1 rounded-full">
                  Activo
                </span>
              </div>
              <p className="text-sm font-medium text-green-700 mb-1">En Operación</p>
              <p className="text-4xl font-bold text-green-900">{stats?.operational_assets || 0}</p>
              <div className="mt-3 flex items-center text-xs text-green-600">
                <FiTrendingUp className="mr-1" />
                <span>{stats?.total_assets ? Math.round((stats.operational_assets / stats.total_assets) * 100) : 0}% disponible</span>
              </div>
            </div>

            {/* Maintenance Assets Card */}
            <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-xl shadow-lg p-6 border border-yellow-200 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <div className="bg-yellow-500 p-3 rounded-xl shadow-md">
                  <FiTool className="w-7 h-7 text-white" />
                </div>
                <span className="text-xs font-semibold text-yellow-600 bg-yellow-200 px-2 py-1 rounded-full">
                  Proceso
                </span>
              </div>
              <p className="text-sm font-medium text-yellow-700 mb-1">En Mantenimiento</p>
              <p className="text-4xl font-bold text-yellow-900">{stats?.maintenance_assets || 0}</p>
              <div className="mt-3 flex items-center text-xs text-yellow-600">
                <FiClock className="mr-1" />
                <span>En proceso</span>
              </div>
            </div>

            {/* Stopped Assets Card */}
            <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-xl shadow-lg p-6 border border-red-200 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <div className="bg-red-500 p-3 rounded-xl shadow-md">
                  <FiAlertTriangle className="w-7 h-7 text-white" />
                </div>
                <span className="text-xs font-semibold text-red-600 bg-red-200 px-2 py-1 rounded-full">
                  Crítico
                </span>
              </div>
              <p className="text-sm font-medium text-red-700 mb-1">Detenidos</p>
              <p className="text-4xl font-bold text-red-900">{stats?.stopped_assets || 0}</p>
              <div className="mt-3 flex items-center text-xs text-red-600">
                {stats?.stopped_assets && stats.stopped_assets > 0 ? (
                  <>
                    <FiAlertTriangle className="mr-1" />
                    <span>Requiere atención</span>
                  </>
                ) : (
                  <>
                    <FiCheckCircle className="mr-1" />
                    <span>Todo operativo</span>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Work Orders Stats with Progress Bars - Visible to all roles */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-900">
              {isOperador ? 'Mis Órdenes de Trabajo' : isSupervisor ? 'Órdenes del Equipo' : 'Órdenes de Trabajo'}
            </h2>
            <button className="text-sm text-purple-600 hover:text-purple-700 font-medium flex items-center">
              Ver todas <FiActivity className="ml-1" />
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Total Work Orders */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-500 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="bg-purple-100 p-3 rounded-lg">
                  <FiActivity className="w-6 h-6 text-purple-600" />
                </div>
                <span className="text-2xl font-bold text-purple-600">{stats?.total_work_orders || 0}</span>
              </div>
              <p className="text-sm font-semibold text-gray-700 mb-2">Total</p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: '100%' }}></div>
              </div>
            </div>

            {/* Pending Work Orders */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-orange-500 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="bg-orange-100 p-3 rounded-lg">
                  <FiClock className="w-6 h-6 text-orange-600" />
                </div>
                <span className="text-2xl font-bold text-orange-600">{stats?.pending_work_orders || 0}</span>
              </div>
              <p className="text-sm font-semibold text-gray-700 mb-2">Pendientes</p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-orange-500 h-2 rounded-full" 
                  style={{ width: `${stats?.total_work_orders ? (stats.pending_work_orders / stats.total_work_orders) * 100 : 0}%` }}
                ></div>
              </div>
              {isOperador && stats && stats.pending_work_orders > 0 && (
                <p className="text-xs text-orange-600 mt-2 font-medium flex items-center">
                  <FiAlertTriangle className="mr-1" />
                  ¡Tienes órdenes pendientes!
                </p>
              )}
            </div>

            {/* In Progress Work Orders */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <FiActivity className="w-6 h-6 text-blue-600" />
                </div>
                <span className="text-2xl font-bold text-blue-600">{stats?.in_progress_work_orders || 0}</span>
              </div>
              <p className="text-sm font-semibold text-gray-700 mb-2">En Progreso</p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full animate-pulse" 
                  style={{ width: `${stats?.total_work_orders ? (stats.in_progress_work_orders / stats.total_work_orders) * 100 : 0}%` }}
                ></div>
              </div>
            </div>

            {/* Completed Work Orders */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="bg-green-100 p-3 rounded-lg">
                  <FiCheckCircle className="w-6 h-6 text-green-600" />
                </div>
                <span className="text-2xl font-bold text-green-600">{stats?.completed_work_orders || 0}</span>
              </div>
              <p className="text-sm font-semibold text-gray-700 mb-2">Completadas</p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-green-500 h-2 rounded-full" 
                  style={{ width: `${stats?.total_work_orders ? (stats.completed_work_orders / stats.total_work_orders) * 100 : 0}%` }}
                ></div>
              </div>
              <p className="text-xs text-green-600 mt-2 font-medium">
                {stats?.kpis?.completion_rate || 0}% tasa de completitud
              </p>
            </div>
          </div>
        </div>

        {/* Charts Section - Only for Supervisors and Admins */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        {(isSupervisor || isAdmin) && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Work Orders Trend Chart */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-gray-900">Tendencia de Órdenes de Trabajo</h3>
                <FiBarChart2 className="text-gray-400" />
              </div>
              {workOrdersTrend.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={workOrdersTrend}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="month" stroke="#6b7280" style={{ fontSize: '12px' }} />
                    <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#fff', 
                        border: '1px solid #e5e7eb', 
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                      }} 
                    />
                    <Legend />
                    <Bar dataKey="completed" fill={COLORS.success} name="Completadas" radius={[8, 8, 0, 0]} />
                    <Bar dataKey="pending" fill={COLORS.warning} name="Pendientes" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[300px] text-gray-400">
                  <div className="text-center">
                    <FiBarChart2 className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">No hay datos disponibles</p>
                  </div>
                </div>
              )}
            </div>

            {/* Asset Status Distribution Pie Chart */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-gray-900">Distribución de Estado de Activos</h3>
                <FiActivity className="text-gray-400" />
              </div>
              {assetStatusData.length > 0 && assetStatusData.some(item => item.value > 0) ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={assetStatusData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {assetStatusData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[300px] text-gray-400">
                  <div className="text-center">
                    <FiActivity className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">No hay datos disponibles</p>
                  </div>
                </div>
              )}
            </div>

            {/* Maintenance Types Bar Chart */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-gray-900">Tipos de Mantenimiento</h3>
                <FiTool className="text-gray-400" />
              </div>
              {maintenanceTypes.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={maintenanceTypes} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis type="number" stroke="#6b7280" style={{ fontSize: '12px' }} />
                    <YAxis dataKey="type" type="category" stroke="#6b7280" style={{ fontSize: '12px' }} width={100} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#fff', 
                        border: '1px solid #e5e7eb', 
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                      }} 
                    />
                    <Bar dataKey="count" fill={COLORS.indigo} name="Cantidad" radius={[0, 8, 8, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[300px] text-gray-400">
                  <div className="text-center">
                    <FiTool className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">No hay datos disponibles</p>
                  </div>
                </div>
              )}
            </div>

            {/* Predictions Timeline Area Chart */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-gray-900">Línea de Tiempo de Predicciones</h3>
                <FaRobot className="text-gray-400" />
              </div>
              {predictionsTimeline.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={predictionsTimeline}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="date" stroke="#6b7280" style={{ fontSize: '12px' }} />
                    <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#fff', 
                        border: '1px solid #e5e7eb', 
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                      }} 
                    />
                    <Legend />
                    <Area type="monotone" dataKey="high_risk" stackId="1" stroke={COLORS.danger} fill={COLORS.danger} name="Alto Riesgo" />
                    <Area type="monotone" dataKey="medium_risk" stackId="1" stroke={COLORS.warning} fill={COLORS.warning} name="Riesgo Medio" />
                    <Area type="monotone" dataKey="low_risk" stackId="1" stroke={COLORS.success} fill={COLORS.success} name="Bajo Riesgo" />
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[300px] text-gray-400">
                  <div className="text-center">
                    <FaRobot className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">No hay datos disponibles</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

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

        {/* Enhanced KPIs Section - Only for Supervisors and Admins */}
        {/* Validates: Requirements 10.1, 10.2, 10.3 */}
        {(isSupervisor || isAdmin) && stats?.kpis && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-900">
                {isSupervisor ? 'KPIs del Equipo' : 'Indicadores Clave de Desempeño'}
              </h2>
              <button className="text-sm text-indigo-600 hover:text-indigo-700 font-medium flex items-center">
                Ver análisis completo <FiBarChart2 className="ml-1" />
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Availability Rate */}
              <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white hover:shadow-2xl transition-all transform hover:-translate-y-1">
                <div className="flex items-center justify-between mb-3">
                  <div className="bg-white bg-opacity-30 p-3 rounded-lg backdrop-blur-sm">
                    <FiCheckCircle className="w-6 h-6" />
                  </div>
                  <span className="text-xs font-bold bg-white bg-opacity-30 px-3 py-1 rounded-full">
                    Excelente
                  </span>
                </div>
                <p className="text-sm font-medium opacity-90 mb-1">Disponibilidad</p>
                <p className="text-4xl font-bold mb-2">{stats.kpis.availability_rate}%</p>
                <div className="w-full bg-white bg-opacity-30 rounded-full h-2 mb-2">
                  <div 
                    className="bg-white h-2 rounded-full" 
                    style={{ width: `${stats.kpis.availability_rate}%` }}
                  ></div>
                </div>
                <p className="text-xs opacity-80">Activos operacionales</p>
              </div>

              {/* Completion Rate */}
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white hover:shadow-2xl transition-all transform hover:-translate-y-1">
                <div className="flex items-center justify-between mb-3">
                  <div className="bg-white bg-opacity-30 p-3 rounded-lg backdrop-blur-sm">
                    <FiActivity className="w-6 h-6" />
                  </div>
                  <FiTrendingUp className="w-5 h-5" />
                </div>
                <p className="text-sm font-medium opacity-90 mb-1">Tasa de Completitud</p>
                <p className="text-4xl font-bold mb-2">{stats.kpis.completion_rate}%</p>
                <div className="w-full bg-white bg-opacity-30 rounded-full h-2 mb-2">
                  <div 
                    className="bg-white h-2 rounded-full" 
                    style={{ width: `${stats.kpis.completion_rate}%` }}
                  ></div>
                </div>
                <p className="text-xs opacity-80">Órdenes completadas</p>
              </div>

              {/* Average Duration */}
              <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white hover:shadow-2xl transition-all transform hover:-translate-y-1">
                <div className="flex items-center justify-between mb-3">
                  <div className="bg-white bg-opacity-30 p-3 rounded-lg backdrop-blur-sm">
                    <FiClock className="w-6 h-6" />
                  </div>
                  <span className="text-xs font-bold bg-white bg-opacity-30 px-3 py-1 rounded-full">
                    Días
                  </span>
                </div>
                <p className="text-sm font-medium opacity-90 mb-1">Tiempo Promedio</p>
                <p className="text-4xl font-bold mb-2">{stats.kpis.avg_duration_days}</p>
                <p className="text-xs opacity-80">Días por orden de trabajo</p>
              </div>

              {/* Preventive Ratio */}
              <div className="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl shadow-lg p-6 text-white hover:shadow-2xl transition-all transform hover:-translate-y-1">
                <div className="flex items-center justify-between mb-3">
                  <div className="bg-white bg-opacity-30 p-3 rounded-lg backdrop-blur-sm">
                    <FiTool className="w-6 h-6" />
                  </div>
                  <FiTrendingUp className="w-5 h-5" />
                </div>
                <p className="text-sm font-medium opacity-90 mb-1">Mantenimiento Preventivo</p>
                <p className="text-4xl font-bold mb-2">{stats.kpis.preventive_ratio}%</p>
                <div className="w-full bg-white bg-opacity-30 rounded-full h-2 mb-2">
                  <div 
                    className="bg-white h-2 rounded-full" 
                    style={{ width: `${stats.kpis.preventive_ratio}%` }}
                  ></div>
                </div>
                <p className="text-xs opacity-80">vs Correctivo</p>
              </div>

              {/* Maintenance Backlog */}
              <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-orange-200 hover:shadow-xl transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="bg-orange-100 p-3 rounded-lg">
                    <FiAlertTriangle className="w-6 h-6 text-orange-600" />
                  </div>
                  {stats.kpis.maintenance_backlog > 10 ? (
                    <span className="text-xs font-bold text-orange-600 bg-orange-100 px-3 py-1 rounded-full">
                      Alto
                    </span>
                  ) : (
                    <span className="text-xs font-bold text-green-600 bg-green-100 px-3 py-1 rounded-full">
                      Normal
                    </span>
                  )}
                </div>
                <p className="text-sm font-medium text-gray-600 mb-1">Backlog</p>
                <p className="text-4xl font-bold text-gray-900 mb-2">{stats.kpis.maintenance_backlog}</p>
                <p className="text-xs text-gray-500">Órdenes pendientes</p>
              </div>

              {/* Critical Assets */}
              <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-red-200 hover:shadow-xl transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="bg-red-100 p-3 rounded-lg">
                    <FiAlertTriangle className="w-6 h-6 text-red-600" />
                  </div>
                  {stats.kpis.critical_assets_count > 0 && (
                    <span className="text-xs font-bold text-red-600 bg-red-100 px-3 py-1 rounded-full animate-pulse">
                      Crítico
                    </span>
                  )}
                </div>
                <p className="text-sm font-medium text-gray-600 mb-1">Activos Críticos</p>
                <p className="text-4xl font-bold text-gray-900 mb-2">{stats.kpis.critical_assets_count}</p>
                <p className="text-xs text-gray-500">Alto riesgo de fallo</p>
              </div>

              {/* Work Orders This Month */}
              <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-teal-200 hover:shadow-xl transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="bg-teal-100 p-3 rounded-lg">
                    <FiActivity className="w-6 h-6 text-teal-600" />
                  </div>
                  <FiTrendingUp className="w-5 h-5 text-teal-600" />
                </div>
                <p className="text-sm font-medium text-gray-600 mb-1">OT Este Mes</p>
                <p className="text-4xl font-bold text-gray-900 mb-2">{stats.kpis.work_orders_this_month}</p>
                <p className="text-xs text-gray-500">Nuevas órdenes creadas</p>
              </div>

              {/* Prediction Accuracy */}
              <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl shadow-lg p-6 text-white hover:shadow-2xl transition-all transform hover:-translate-y-1">
                <div className="flex items-center justify-between mb-3">
                  <div className="bg-white bg-opacity-30 p-3 rounded-lg backdrop-blur-sm">
                    <FaRobot className="w-6 h-6" />
                  </div>
                  <span className="text-xs font-bold bg-white bg-opacity-30 px-3 py-1 rounded-full">
                    ML
                  </span>
                </div>
                <p className="text-sm font-medium opacity-90 mb-1">Precisión ML</p>
                <p className="text-4xl font-bold mb-2">{stats.kpis.prediction_accuracy}%</p>
                <div className="w-full bg-white bg-opacity-30 rounded-full h-2 mb-2">
                  <div 
                    className="bg-white h-2 rounded-full" 
                    style={{ width: `${stats.kpis.prediction_accuracy}%` }}
                  ></div>
                </div>
                <p className="text-xs opacity-80">Predicciones acertadas</p>
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
