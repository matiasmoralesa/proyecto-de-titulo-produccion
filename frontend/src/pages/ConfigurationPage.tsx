/**
 * Configuration and Master Data Management Page (Admin Only)
 */
import React, { useState, useEffect } from 'react';
import MainLayout from '../components/layout/MainLayout';
import { configurationService } from '../services/configurationService';
import {
  AssetCategory,
  Priority,
  WorkOrderType,
  SystemParameter,
  AuditLog,
} from '../types/configuration';
import { FiEdit2, FiTrash2, FiPlus } from 'react-icons/fi';
import toast from 'react-hot-toast';
import CategoryForm from '../components/configuration/CategoryForm';
import PriorityForm from '../components/configuration/PriorityForm';
import WorkOrderTypeForm from '../components/configuration/WorkOrderTypeForm';
import ParameterForm from '../components/configuration/ParameterForm';

type TabType = 'categories' | 'priorities' | 'types' | 'parameters' | 'audit';

const ConfigurationPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('categories');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  // Data states
  const [categories, setCategories] = useState<AssetCategory[]>([]);
  const [priorities, setPriorities] = useState<Priority[]>([]);
  const [workOrderTypes, setWorkOrderTypes] = useState<WorkOrderType[]>([]);
  const [parameters, setParameters] = useState<SystemParameter[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);

  // Modal states
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<any>(null);

  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      switch (activeTab) {
        case 'categories':
          const cats = await configurationService.getAssetCategories();
          setCategories(cats);
          break;
        case 'priorities':
          const prios = await configurationService.getPriorities();
          setPriorities(prios);
          break;
        case 'types':
          const types = await configurationService.getWorkOrderTypes();
          setWorkOrderTypes(types);
          break;
        case 'parameters':
          const params = await configurationService.getSystemParameters();
          setParameters(params);
          break;
        case 'audit':
          const logs = await configurationService.getAuditLogs();
          setAuditLogs(logs);
          break;
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (type: string, id: number) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
      return;
    }

    try {
      switch (type) {
        case 'category':
          await configurationService.deleteAssetCategory(id);
          toast.success('Categoría eliminada exitosamente');
          break;
        case 'priority':
          await configurationService.deletePriority(id);
          toast.success('Prioridad eliminada exitosamente');
          break;
        case 'type':
          await configurationService.deleteWorkOrderType(id);
          toast.success('Tipo eliminado exitosamente');
          break;
        case 'parameter':
          await configurationService.deleteSystemParameter(id);
          toast.success('Parámetro eliminado exitosamente');
          break;
      }
      fetchData();
    } catch (error: any) {
      const message = error.response?.data?.detail || error.response?.data?.message || 'Error al eliminar el elemento';
      toast.error(message);
    }
  };

  const handleEdit = (item: any) => {
    setEditingItem(item);
    setShowModal(true);
  };

  const handleCreate = () => {
    setEditingItem(null);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingItem(null);
  };

  const handleSave = async (data: any) => {
    setSaving(true);
    try {
      switch (activeTab) {
        case 'categories':
          if (editingItem) {
            await configurationService.updateAssetCategory(editingItem.id, data);
            toast.success('Categoría actualizada exitosamente');
          } else {
            await configurationService.createAssetCategory(data);
            toast.success('Categoría creada exitosamente');
          }
          break;
        case 'priorities':
          if (editingItem) {
            await configurationService.updatePriority(editingItem.id, data);
            toast.success('Prioridad actualizada exitosamente');
          } else {
            await configurationService.createPriority(data);
            toast.success('Prioridad creada exitosamente');
          }
          break;
        case 'types':
          if (editingItem) {
            await configurationService.updateWorkOrderType(editingItem.id, data);
            toast.success('Tipo actualizado exitosamente');
          } else {
            await configurationService.createWorkOrderType(data);
            toast.success('Tipo creado exitosamente');
          }
          break;
        case 'parameters':
          if (editingItem) {
            await configurationService.updateSystemParameter(editingItem.id, data);
            toast.success('Parámetro actualizado exitosamente');
          }
          break;
      }
      handleCloseModal();
      fetchData();
    } catch (error: any) {
      console.error('Error saving:', error);
      const message = error.response?.data?.detail || 
                     error.response?.data?.message ||
                     Object.values(error.response?.data || {}).flat().join(', ') ||
                     'Error al guardar';
      toast.error(message);
      // Don't close modal on error
    } finally {
      setSaving(false);
    }
  };

  return (
    <MainLayout>
      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Configuración del Sistema</h1>
          <p className="text-sm text-gray-600 mt-1">
            Gestión de datos maestros y parámetros del sistema (Solo Administradores)
          </p>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {[
              { key: 'categories', label: '📁 Categorías' },
              { key: 'priorities', label: '⚡ Prioridades' },
              { key: 'types', label: '📋 Tipos de OT' },
              { key: 'parameters', label: '⚙️ Parámetros' },
              { key: 'audit', label: '📜 Auditoría' },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as TabType)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.key
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        {loading ? (
          <div className="flex justify-center items-center p-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            {/* Asset Categories */}
            {activeTab === 'categories' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-semibold">Categorías de Activos</h2>
                  <button 
                    onClick={handleCreate}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center space-x-2"
                  >
                    <FiPlus />
                    <span>Nueva Categoría</span>
                  </button>
                </div>
                <div className="bg-white rounded-lg shadow overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Código</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descripción</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {categories.map((category) => (
                        <tr key={category.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{category.code}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{category.name}</td>
                          <td className="px-6 py-4 text-sm text-gray-500">{category.description}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 text-xs rounded-full ${category.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                              {category.is_active ? 'Activo' : 'Inactivo'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm">
                            <button 
                              onClick={() => handleEdit(category)}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                              title="Editar"
                            >
                              <FiEdit2 />
                            </button>
                            {category.can_delete && (
                              <button
                                onClick={() => handleDelete('category', category.id)}
                                className="text-red-600 hover:text-red-900"
                                title="Eliminar"
                              >
                                <FiTrash2 />
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Priorities */}
            {activeTab === 'priorities' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-semibold">Prioridades</h2>
                  <button 
                    onClick={handleCreate}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center space-x-2"
                  >
                    <FiPlus />
                    <span>Nueva Prioridad</span>
                  </button>
                </div>
                <div className="bg-white rounded-lg shadow overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nivel</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Color</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {priorities.map((priority) => (
                        <tr key={priority.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{priority.level}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{priority.name}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center space-x-2">
                              <div
                                className="w-6 h-6 rounded"
                                style={{ backgroundColor: priority.color_code }}
                              ></div>
                              <span className="text-sm text-gray-500">{priority.color_code}</span>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 text-xs rounded-full ${priority.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                              {priority.is_active ? 'Activo' : 'Inactivo'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm">
                            <button 
                              onClick={() => handleEdit(priority)}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                              title="Editar"
                            >
                              <FiEdit2 />
                            </button>
                            {priority.can_delete && (
                              <button
                                onClick={() => handleDelete('priority', priority.id)}
                                className="text-red-600 hover:text-red-900"
                                title="Eliminar"
                              >
                                <FiTrash2 />
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Work Order Types */}
            {activeTab === 'types' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-semibold">Tipos de Órdenes de Trabajo</h2>
                  <button 
                    onClick={handleCreate}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center space-x-2"
                  >
                    <FiPlus />
                    <span>Nuevo Tipo</span>
                  </button>
                </div>
                <div className="bg-white rounded-lg shadow overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Código</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descripción</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {workOrderTypes.map((type) => (
                        <tr key={type.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{type.code}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{type.name}</td>
                          <td className="px-6 py-4 text-sm text-gray-500">{type.description}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 text-xs rounded-full ${type.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                              {type.is_active ? 'Activo' : 'Inactivo'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm">
                            <button 
                              onClick={() => handleEdit(type)}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                              title="Editar"
                            >
                              <FiEdit2 />
                            </button>
                            {type.can_delete && (
                              <button
                                onClick={() => handleDelete('type', type.id)}
                                className="text-red-600 hover:text-red-900"
                                title="Eliminar"
                              >
                                <FiTrash2 />
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* System Parameters */}
            {activeTab === 'parameters' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-semibold">Parámetros del Sistema</h2>
                </div>
                <div className="bg-white rounded-lg shadow overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Clave</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Valor</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descripción</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Editable</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {parameters.map((param) => (
                        <tr key={param.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{param.key}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{param.value}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{param.data_type}</td>
                          <td className="px-6 py-4 text-sm text-gray-500">{param.description}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 text-xs rounded-full ${param.is_editable ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                              {param.is_editable ? 'Sí' : 'No'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm">
                            <button 
                              onClick={() => handleEdit(param)}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                              title={param.is_editable ? 'Editar' : 'Ver'}
                            >
                              <FiEdit2 />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Audit Logs */}
            {activeTab === 'audit' && (
              <div>
                <h2 className="text-lg font-semibold mb-4">Registro de Auditoría</h2>
                <div className="bg-white rounded-lg shadow overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Usuario</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acción</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Modelo</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Objeto</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {auditLogs.map((log) => (
                        <tr key={log.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {new Date(log.timestamp).toLocaleString('es-ES')}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{log.user_name}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              log.action === 'CREATE' ? 'bg-green-100 text-green-800' :
                              log.action === 'UPDATE' ? 'bg-blue-100 text-blue-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {log.action_display}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{log.model_name}</td>
                          <td className="px-6 py-4 text-sm text-gray-500">{log.object_repr}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
        )}

        {/* Edit/Create Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
              <h3 className="text-lg font-semibold mb-4">
                {editingItem ? 'Editar' : 'Crear'} {
                  activeTab === 'categories' ? 'Categoría' :
                  activeTab === 'priorities' ? 'Prioridad' :
                  activeTab === 'types' ? 'Tipo de OT' :
                  'Parámetro'
                }
              </h3>
              
              {activeTab === 'categories' && (
                <CategoryForm
                  category={editingItem}
                  onSubmit={handleSave}
                  onCancel={handleCloseModal}
                  loading={saving}
                />
              )}
              
              {activeTab === 'priorities' && (
                <PriorityForm
                  priority={editingItem}
                  onSubmit={handleSave}
                  onCancel={handleCloseModal}
                  loading={saving}
                />
              )}
              
              {activeTab === 'types' && (
                <WorkOrderTypeForm
                  workOrderType={editingItem}
                  onSubmit={handleSave}
                  onCancel={handleCloseModal}
                  loading={saving}
                />
              )}
              
              {activeTab === 'parameters' && editingItem && (
                <ParameterForm
                  parameter={editingItem}
                  onSubmit={handleSave}
                  onCancel={handleCloseModal}
                  loading={saving}
                />
              )}
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default ConfigurationPage;
