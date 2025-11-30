/**
 * Maintenance Plans page component
 */
import { useState, useEffect } from 'react';
import MainLayout from '../components/layout/MainLayout';
import {
  FiTool,
  FiClock,
  FiAlertCircle,
  FiFilter,
  FiCalendar,
  FiPause,
  FiPlay,
} from 'react-icons/fi';
import { MaintenancePlan } from '../types/maintenance.types';
import { maintenanceService } from '../services/maintenanceService';
import MaintenancePlanForm from '../components/maintenance/MaintenancePlanForm';
import MaintenancePlanDetail from '../components/maintenance/MaintenancePlanDetail';

export default function MaintenancePlans() {
  const [plans, setPlans] = useState<MaintenancePlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showDetail, setShowDetail] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<MaintenancePlan | null>(null);
  const [selectedPlanId, setSelectedPlanId] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    status: '',
    recurrence_type: '',
    search: '',
  });

  useEffect(() => {
    loadPlans();
  }, [filters]);

  const loadPlans = async () => {
    try {
      setLoading(true);
      const data = await maintenanceService.getAll(filters);
      setPlans(data.results || []);
    } catch (error) {
      console.error('Error loading maintenance plans:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNew = () => {
    setSelectedPlan(null);
    setShowForm(true);
  };

  const handleEdit = (plan: MaintenancePlan) => {
    setSelectedPlan(plan);
    setShowDetail(false);
    setShowForm(true);
  };

  const handleViewDetail = (planId: string) => {
    setSelectedPlanId(planId);
    setShowDetail(true);
  };

  const handleDelete = async () => {
    if (!selectedPlanId) return;

    if (window.confirm('¿Estás seguro de que deseas eliminar este plan de mantenimiento?')) {
      try {
        await maintenanceService.delete(selectedPlanId);
        setShowDetail(false);
        loadPlans();
      } catch (error) {
        console.error('Error deleting maintenance plan:', error);
        alert('Error al eliminar el plan de mantenimiento');
      }
    }
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    loadPlans();
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      Activo: 'bg-green-100 text-green-800 border-green-200',
      Pausado: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      Completado: 'bg-blue-100 text-blue-800 border-blue-200',
      Cancelado: 'bg-gray-100 text-gray-800 border-gray-200',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getDueStatusColor = (plan: MaintenancePlan) => {
    if (plan.is_overdue) return 'text-red-600';
    if (plan.is_due) return 'text-orange-600';
    return 'text-gray-600';
  };

  const getDueStatusText = (plan: MaintenancePlan) => {
    if (plan.is_overdue) return 'Vencido';
    if (plan.is_due) return 'Por vencer';
    if (plan.days_until_due !== null) {
      return `${plan.days_until_due} días`;
    }
    if (plan.usage_until_due !== null) {
      return `${plan.usage_until_due} ${
        plan.recurrence_type === 'Por Horas' ? 'hrs' : 'km'
      } restantes`;
    }
    return 'N/A';
  };

  const recurrenceTypes = [
    'Diario',
    'Semanal',
    'Mensual',
    'Trimestral',
    'Anual',
    'Por Horas',
    'Por Kilómetros',
  ];

  const statusOptions = ['Activo', 'Pausado', 'Completado', 'Cancelado'];

  if (loading) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Planes de Mantenimiento</h1>
            <p className="text-gray-600 mt-1">Gestión de mantenimiento preventivo</p>
          </div>
          <button
            onClick={handleCreateNew}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium"
          >
            + Nuevo Plan
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="flex items-center space-x-2 mb-3">
            <FiFilter className="w-5 h-5 text-gray-400" />
            <h3 className="font-medium text-gray-900">Filtros</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Todos</option>
                {statusOptions.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tipo de Recurrencia
              </label>
              <select
                value={filters.recurrence_type}
                onChange={(e) => setFilters({ ...filters, recurrence_type: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Todos</option>
                {recurrenceTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
              <input
                type="text"
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                placeholder="Buscar por nombre..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
        </div>

        {/* Plans Grid */}
        {plans.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <FiTool className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No hay planes de mantenimiento registrados</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {plans.map((plan) => (
              <div
                key={plan.id}
                className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <h3 className="text-lg font-semibold text-gray-900">{plan.name}</h3>
                        {plan.is_paused && (
                          <span className="px-2 py-1 text-xs font-semibold bg-yellow-100 text-yellow-800 rounded">
                            <FiPause className="w-3 h-3 inline mr-1" />
                            Pausado
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600">{plan.asset_name}</p>
                    </div>
                    <span
                      className={`px-3 py-1 text-xs font-semibold rounded-full border ${getStatusColor(
                        plan.status
                      )}`}
                    >
                      {plan.status}
                    </span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <FiCalendar className="w-4 h-4" />
                      <span>
                        {plan.recurrence_type} (cada {plan.recurrence_interval}{' '}
                        {plan.recurrence_interval === 1 ? 'vez' : 'veces'})
                      </span>
                    </div>

                    {plan.next_due_date && (
                      <div className="flex items-center space-x-2 text-sm">
                        <FiClock className="w-4 h-4 text-gray-400" />
                        <span className="text-gray-600">Próximo:</span>
                        <span className={`font-medium ${getDueStatusColor(plan)}`}>
                          {new Date(plan.next_due_date).toLocaleDateString('es-ES')}
                        </span>
                      </div>
                    )}

                    <div className="flex items-center space-x-2 text-sm">
                      <FiAlertCircle className={`w-4 h-4 ${getDueStatusColor(plan)}`} />
                      <span className={`font-medium ${getDueStatusColor(plan)}`}>
                        {getDueStatusText(plan)}
                      </span>
                    </div>

                    {plan.assigned_to_name && (
                      <div className="flex items-center space-x-2 text-sm text-gray-600">
                        <span>Asignado a: {plan.assigned_to_name}</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="px-6 py-3 bg-gray-50 border-t border-gray-100">
                  <button
                    onClick={() => handleViewDetail(plan.id)}
                    className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                  >
                    Ver detalles →
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modals */}
      {showForm && (
        <MaintenancePlanForm
          plan={selectedPlan || undefined}
          onClose={() => setShowForm(false)}
          onSuccess={handleFormSuccess}
        />
      )}

      {showDetail && selectedPlanId && (
        <MaintenancePlanDetail
          planId={selectedPlanId}
          onClose={() => setShowDetail(false)}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onUpdate={loadPlans}
        />
      )}
    </MainLayout>
  );
}
