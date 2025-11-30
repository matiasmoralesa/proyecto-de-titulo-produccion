/**
 * Work Orders page component
 */
import { useState, useEffect } from 'react';
import MainLayout from '../components/layout/MainLayout';
import { FiClipboard, FiClock, FiUser, FiAlertCircle, FiFilter } from 'react-icons/fi';
import { WorkOrder, WorkOrderDetail } from '../types/workOrder.types';
import { workOrderService } from '../services/workOrderService';
import WorkOrderForm from '../components/workOrders/WorkOrderForm';
import WorkOrderDetailComponent from '../components/workOrders/WorkOrderDetail';

export default function WorkOrders() {
  const [workOrders, setWorkOrders] = useState<WorkOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showDetail, setShowDetail] = useState(false);
  const [selectedWorkOrder, setSelectedWorkOrder] = useState<WorkOrderDetail | null>(null);
  const [selectedWorkOrderId, setSelectedWorkOrderId] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: '',
  });

  useEffect(() => {
    loadWorkOrders();
  }, [filters]);

  const loadWorkOrders = async () => {
    try {
      setLoading(true);
      const data = await workOrderService.getAll(filters);
      setWorkOrders(data.results || []);
    } catch (error) {
      console.error('Error loading work orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNew = () => {
    setSelectedWorkOrder(null);
    setShowForm(true);
  };

  const handleEdit = (workOrder: WorkOrderDetail) => {
    setSelectedWorkOrder(workOrder);
    setShowDetail(false);
    setShowForm(true);
  };

  const handleViewDetail = (workOrderId: string) => {
    setSelectedWorkOrderId(workOrderId);
    setShowDetail(true);
  };

  const handleDelete = async () => {
    if (!selectedWorkOrderId) return;

    if (window.confirm('¿Estás seguro de que deseas eliminar esta orden de trabajo?')) {
      try {
        await workOrderService.delete(selectedWorkOrderId);
        setShowDetail(false);
        loadWorkOrders();
      } catch (error) {
        console.error('Error deleting work order:', error);
        alert('Error al eliminar la orden de trabajo');
      }
    }
  };

  const handleFormSuccess = () => {
    loadWorkOrders();
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      Pendiente: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'En Progreso': 'bg-blue-100 text-blue-800 border-blue-200',
      Completada: 'bg-green-100 text-green-800 border-green-200',
      Cancelada: 'bg-gray-100 text-gray-800 border-gray-200',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      Baja: 'text-gray-600',
      Media: 'text-blue-600',
      Alta: 'text-orange-600',
      Urgente: 'text-red-600',
    };
    return colors[priority] || 'text-gray-600';
  };

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
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Órdenes de Trabajo</h1>
            <p className="text-gray-600 mt-1">Gestión de tareas de mantenimiento</p>
          </div>
          <button
            onClick={handleCreateNew}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium"
          >
            + Nueva Orden
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
                <option value="Pendiente">Pendiente</option>
                <option value="En Progreso">En Progreso</option>
                <option value="Completada">Completada</option>
                <option value="Cancelada">Cancelada</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Prioridad</label>
              <select
                value={filters.priority}
                onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Todas</option>
                <option value="Baja">Baja</option>
                <option value="Media">Media</option>
                <option value="Alta">Alta</option>
                <option value="Urgente">Urgente</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
              <input
                type="text"
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                placeholder="Buscar por título..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
        </div>

        {workOrders.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <FiClipboard className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No hay órdenes de trabajo registradas</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {workOrders.map((wo) => (
              <div
                key={wo.id}
                className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="text-sm font-mono text-gray-500">
                          {wo.work_order_number}
                        </span>
                        <span className={`text-sm font-semibold ${getPriorityColor(wo.priority)}`}>
                          {wo.priority}
                        </span>
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900">{wo.title}</h3>
                    </div>
                    <span
                      className={`px-3 py-1 text-xs font-semibold rounded-full border ${getStatusColor(
                        wo.status
                      )}`}
                    >
                      {wo.status}
                    </span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <FiClipboard className="w-4 h-4" />
                      <span>Activo: {wo.asset_name}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <FiUser className="w-4 h-4" />
                      <span>Asignado a: {wo.assigned_to_name}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <FiClock className="w-4 h-4" />
                      <span>
                        Programada: {new Date(wo.scheduled_date).toLocaleDateString('es-ES')}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="px-6 py-3 bg-gray-50 border-t border-gray-100">
                  <button
                    onClick={() => handleViewDetail(wo.id)}
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
        <WorkOrderForm
          workOrder={selectedWorkOrder || undefined}
          onClose={() => setShowForm(false)}
          onSuccess={handleFormSuccess}
        />
      )}

      {showDetail && selectedWorkOrderId && (
        <WorkOrderDetailComponent
          workOrderId={selectedWorkOrderId}
          onClose={() => setShowDetail(false)}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onUpdate={loadWorkOrders}
        />
      )}
    </MainLayout>
  );
}
