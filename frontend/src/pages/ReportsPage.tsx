/**
 * Reports and Analytics Dashboard Page
 */
import React, { useState, useEffect } from 'react';
import MainLayout from '../components/layout/MainLayout';
import { reportService } from '../services/reportService';
import {
  DashboardData,
  AssetDowntime,
  SparePartConsumption,
} from '../types/report';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { FiDownload, FiCalendar } from 'react-icons/fi';
import { 
  exportWorkOrdersToExcel, 
  exportAssetDowntimeToExcel,
  exportSparePartsToExcel 
} from '../utils/excelExport';

const ReportsPage: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [assetDowntime, setAssetDowntime] = useState<AssetDowntime[]>([]);
  const [sparePartConsumption, setSparePartConsumption] = useState<SparePartConsumption[]>([]);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState({
    start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
    end_date: new Date().toISOString(),
  });

  useEffect(() => {
    fetchData();
  }, [dateRange]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [dashboard, downtime, consumption] = await Promise.all([
        reportService.getDashboardData(dateRange),
        reportService.getAssetDowntime(dateRange),
        reportService.getSparePartConsumption(dateRange),
      ]);
      
      setDashboardData(dashboard);
      setAssetDowntime(downtime);
      setSparePartConsumption(consumption);
    } catch (error) {
      console.error('Error fetching report data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExportWorkOrders = async () => {
    try {
      // Obtener datos del resumen de órdenes de trabajo
      const summary = dashboardData?.work_order_summary;
      if (!summary) return;
      
      // Aquí deberías obtener los datos completos de las órdenes
      // Por ahora, exportaremos el resumen disponible
      const workOrdersData = [
        {
          work_order_number: 'Resumen',
          title: 'Total de Órdenes',
          asset_name: '',
          status: '',
          priority: '',
          work_order_type: '',
          assigned_to_name: '',
          created_at: '',
          completed_date: '',
          actual_hours: summary.total_hours_worked,
        }
      ];
      
      exportWorkOrdersToExcel(workOrdersData);
    } catch (error) {
      console.error('Error exporting work orders:', error);
    }
  };

  const handleExportAssetDowntime = async () => {
    try {
      exportAssetDowntimeToExcel(assetDowntime);
    } catch (error) {
      console.error('Error exporting asset downtime:', error);
    }
  };

  const handleExportSpareParts = () => {
    try {
      exportSparePartsToExcel(sparePartConsumption);
    } catch (error) {
      console.error('Error exporting spare parts:', error);
    }
  };

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  // Prepare chart data
  const statusChartData = dashboardData
    ? Object.entries(dashboardData.work_order_summary.by_status).map(([key, value]) => ({
        name: value.label,
        value: value.count,
      }))
    : [];

  const priorityChartData = dashboardData
    ? Object.entries(dashboardData.work_order_summary.by_priority).map(([key, value]) => ({
        name: value.label,
        value: value.count,
      }))
    : [];

  const downtimeChartData = assetDowntime.slice(0, 10).map((item) => ({
    name: item.asset__name,
    hours: item.total_downtime,
  }));

  const consumptionChartData = sparePartConsumption.slice(0, 10).map((item) => ({
    name: item.spare_part__name,
    quantity: item.total_quantity,
  }));

  if (loading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center h-screen">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Reportes y Analytics</h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Análisis de rendimiento y KPIs del sistema
              </p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={handleExportWorkOrders}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
              >
                <FiDownload />
                <span>Exportar OT (Excel)</span>
              </button>
              <button
                onClick={handleExportAssetDowntime}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
              >
                <FiDownload />
                <span>Exportar Inactividad (Excel)</span>
              </button>
            </div>
          </div>

          {/* Date Range Selector */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 dark:border dark:border-gray-700">
            <div className="flex items-center space-x-4">
              <FiCalendar className="text-gray-500 dark:text-gray-400" />
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Desde:</label>
                <input
                  type="date"
                  value={dateRange.start_date.split('T')[0]}
                  onChange={(e) =>
                    setDateRange({ ...dateRange, start_date: new Date(e.target.value).toISOString() })
                  }
                  className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                />
              </div>
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Hasta:</label>
                <input
                  type="date"
                  value={dateRange.end_date.split('T')[0]}
                  onChange={(e) =>
                    setDateRange({ ...dateRange, end_date: new Date(e.target.value).toISOString() })
                  }
                  className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                />
              </div>
            </div>
          </div>
        </div>

        {/* KPI Cards */}
        {dashboardData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            {/* MTBF Card */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">MTBF</h3>
                <span className="text-2xl">⏱️</span>
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {dashboardData.mtbf ? `${dashboardData.mtbf}h` : 'N/A'}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Tiempo entre fallas</p>
            </div>

            {/* MTTR Card */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">MTTR</h3>
                <span className="text-2xl">🔧</span>
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{dashboardData.mttr}h</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Tiempo de reparación</p>
            </div>

            {/* OEE Card */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">OEE</h3>
                <span className="text-2xl">📊</span>
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{dashboardData.oee}%</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Efectividad del equipo</p>
            </div>

            {/* Compliance Card */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Cumplimiento</h3>
                <span className="text-2xl">✅</span>
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {dashboardData.maintenance_compliance.compliance_rate}%
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Mantenimiento al día</p>
            </div>
          </div>
        )}

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Work Orders by Status */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Órdenes de Trabajo por Estado
            </h3>
            {statusChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={statusChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {statusChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[300px] text-gray-500 dark:text-gray-400">
                <div className="text-center">
                  <p className="text-4xl mb-2">📊</p>
                  <p>No hay datos disponibles</p>
                </div>
              </div>
            )}
          </div>

          {/* Work Orders by Priority */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Órdenes de Trabajo por Prioridad
            </h3>
            {priorityChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={priorityChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {priorityChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[300px] text-gray-500 dark:text-gray-400">
                <div className="text-center">
                  <p className="text-4xl mb-2">📊</p>
                  <p>No hay datos disponibles</p>
                </div>
              </div>
            )}
          </div>

          {/* Asset Downtime */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Inactividad por Activo (Top 10)
            </h3>
            {downtimeChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={downtimeChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis label={{ value: 'Horas', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="hours" fill="#ef4444" name="Horas de Inactividad" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[300px] text-gray-500 dark:text-gray-400">
                <div className="text-center">
                  <p className="text-4xl mb-2">📊</p>
                  <p>No hay datos disponibles</p>
                </div>
              </div>
            )}
          </div>

          {/* Spare Part Consumption */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Consumo de Repuestos (Top 10)
              </h3>
              <button
                onClick={handleExportSpareParts}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
                disabled={sparePartConsumption.length === 0}
              >
                <FiDownload />
                <span>Exportar Excel</span>
              </button>
            </div>
            {consumptionChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={consumptionChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis label={{ value: 'Cantidad', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="quantity" fill="#10b981" name="Cantidad Consumida" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[300px] text-gray-500 dark:text-gray-400">
                <div className="text-center">
                  <p className="text-4xl mb-2">📊</p>
                  <p>No hay datos disponibles</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Summary Stats */}
        {dashboardData && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Resumen de Órdenes de Trabajo
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Total:</span>
                  <span className="font-semibold dark:text-white">{dashboardData.work_order_summary.total}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Horas Trabajadas:</span>
                  <span className="font-semibold dark:text-white">
                    {dashboardData.work_order_summary.total_hours_worked}h
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Tiempo Promedio:</span>
                  <span className="font-semibold dark:text-white">
                    {dashboardData.work_order_summary.avg_completion_time}h
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Cumplimiento de Mantenimiento
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Total Planes:</span>
                  <span className="font-semibold dark:text-white">
                    {dashboardData.maintenance_compliance.total_plans}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Al Día:</span>
                  <span className="font-semibold text-green-600 dark:text-green-500">
                    {dashboardData.maintenance_compliance.on_schedule}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Vencidos:</span>
                  <span className="font-semibold text-red-600 dark:text-red-500">
                    {dashboardData.maintenance_compliance.overdue_plans}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Próximos (7 días):</span>
                  <span className="font-semibold text-yellow-600 dark:text-yellow-500">
                    {dashboardData.maintenance_compliance.upcoming_plans}
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Activos con Mayor Inactividad</h3>
              <div className="space-y-2">
                {assetDowntime.slice(0, 5).map((item, index) => (
                  <div key={index} className="flex justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400 truncate">{item.asset__name}</span>
                    <span className="font-semibold dark:text-white">{item.total_downtime}h</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default ReportsPage;
