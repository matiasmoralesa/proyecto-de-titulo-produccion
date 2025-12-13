import { useState, useEffect } from 'react';
import { FaClock, FaCheckCircle, FaExclamationCircle, FaSpinner, FaPlay } from 'react-icons/fa';
import toast from 'react-hot-toast';
import MainLayout from '../components/layout/MainLayout';
import api from '../services/api';

interface TaskResult {
  id: string;
  task_name: string;
  status: string;
  result: any;
  date_created: string;
  date_done: string;
  traceback: string | null;
}

interface PeriodicTask {
  id: number;
  name: string;
  task: string;
  enabled: boolean;
  last_run_at: string | null;
  total_run_count: number;
  crontab: {
    minute: string;
    hour: string;
    day_of_week: string;
    day_of_month: string;
    month_of_year: string;
  } | null;
}

const CeleryMonitorPage = () => {
  const [taskResults, setTaskResults] = useState<TaskResult[]>([]);
  const [periodicTasks, setPeriodicTasks] = useState<PeriodicTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'results' | 'scheduled'>('results');
  const [selectedTask, setSelectedTask] = useState<TaskResult | null>(null);
  const [showTaskDetail, setShowTaskDetail] = useState(false);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Actualizar cada 10 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      // Fetch task results
      const resultsResponse = await api.get('/celery/task-results/');
      setTaskResults(resultsResponse.data.results || resultsResponse.data);

      // Fetch periodic tasks
      const tasksResponse = await api.get('/celery/periodic-tasks/');
      setPeriodicTasks(tasksResponse.data.results || tasksResponse.data);
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching Celery data:', error);
      toast.error('Error al cargar datos de Celery');
      setTaskResults([]);
      setPeriodicTasks([]);
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'SUCCESS':
        return <FaCheckCircle className="text-green-500" />;
      case 'FAILURE':
        return <FaExclamationCircle className="text-red-500" />;
      case 'PENDING':
      case 'STARTED':
        return <FaSpinner className="text-blue-500 animate-spin" />;
      default:
        return <FaClock className="text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'SUCCESS':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'FAILURE':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'PENDING':
      case 'STARTED':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const formatCrontab = (crontab: any) => {
    if (!crontab) return 'N/A';
    return `${crontab.minute} ${crontab.hour} ${crontab.day_of_month} ${crontab.month_of_year} ${crontab.day_of_week}`;
  };

  const getTaskStats = () => {
    const total = taskResults.length;
    const success = taskResults.filter(t => t.status === 'SUCCESS').length;
    const failure = taskResults.filter(t => t.status === 'FAILURE').length;
    const pending = taskResults.filter(t => ['PENDING', 'STARTED'].includes(t.status)).length;
    
    return { total, success, failure, pending };
  };

  const openTaskDetail = (task: TaskResult) => {
    setSelectedTask(task);
    setShowTaskDetail(true);
  };

  const closeTaskDetail = () => {
    setShowTaskDetail(false);
    setSelectedTask(null);
  };

  const stats = getTaskStats();

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <FaClock className="text-3xl text-purple-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-800">Monitor de Celery</h1>
                <p className="text-gray-600 text-sm">
                  Monitoreo de tareas automáticas y programadas
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={fetchData}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 flex items-center gap-2 transition-colors"
              >
                <FaSpinner className="animate-spin" />
                Actualizar
              </button>
            </div>
          </div>
        </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Tareas</p>
              <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
            </div>
            <FaClock className="text-3xl text-purple-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Exitosas</p>
              <p className="text-2xl font-bold text-green-600">{stats.success}</p>
            </div>
            <FaCheckCircle className="text-3xl text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Fallidas</p>
              <p className="text-2xl font-bold text-red-600">{stats.failure}</p>
            </div>
            <FaExclamationCircle className="text-3xl text-red-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">En Proceso</p>
              <p className="text-2xl font-bold text-blue-600">{stats.pending}</p>
            </div>
            <FaSpinner className="text-3xl text-blue-500" />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('results')}
              className={`px-6 py-3 text-sm font-medium ${
                activeTab === 'results'
                  ? 'border-b-2 border-purple-600 text-purple-600'
                  : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Resultados de Tareas
            </button>
            <button
              onClick={() => setActiveTab('scheduled')}
              className={`px-6 py-3 text-sm font-medium ${
                activeTab === 'scheduled'
                  ? 'border-b-2 border-purple-600 text-purple-600'
                  : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Tareas Programadas
            </button>
          </nav>
        </div>

        <div className="p-6">
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Cargando datos...</p>
            </div>
          ) : activeTab === 'results' ? (
            /* Task Results */
            <div className="overflow-x-auto">
              {taskResults.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <FaClock className="text-6xl mx-auto mb-4 text-gray-300" />
                  <p>No hay resultados de tareas disponibles</p>
                  <p className="text-sm mt-2">Las tareas ejecutadas aparecerán aquí</p>
                </div>
              ) : (
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Tarea
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Estado
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Fecha Inicio
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Fecha Fin
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Resultado
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {taskResults.map((task) => (
                      <tr 
                        key={task.id} 
                        className="hover:bg-gray-50 cursor-pointer"
                        onClick={() => openTaskDetail(task)}
                      >
                        <td className="px-6 py-4">
                          <div className="text-sm font-medium text-gray-900">
                            {task.task_name.split('.').pop()}
                          </div>
                          <div className="text-xs text-gray-500">{task.task_name}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span
                            className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(
                              task.status
                            )}`}
                          >
                            {getStatusIcon(task.status)}
                            {task.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(task.date_created).toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {task.date_done ? new Date(task.date_done).toLocaleString() : '-'}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {task.status === 'SUCCESS' && task.result ? (
                            <pre className="text-xs bg-gray-50 p-2 rounded max-w-md overflow-auto">
                              {JSON.stringify(task.result, null, 2)}
                            </pre>
                          ) : task.status === 'FAILURE' && task.traceback ? (
                            <span className="text-red-600">Error</span>
                          ) : (
                            '-'
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          ) : (
            /* Periodic Tasks */
            <div className="overflow-x-auto">
              {periodicTasks.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <FaClock className="text-6xl mx-auto mb-4 text-gray-300" />
                  <p>No hay tareas programadas</p>
                  <p className="text-sm mt-2">Las tareas programadas aparecerán aquí</p>
                </div>
              ) : (
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Nombre
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Tarea
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Estado
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Horario (Crontab)
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Última Ejecución
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Total Ejecuciones
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {periodicTasks.map((task) => (
                      <tr key={task.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div className="text-sm font-medium text-gray-900">{task.name}</div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-sm text-gray-500">{task.task}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {task.enabled ? (
                            <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                              <FaPlay className="text-xs" />
                              Activa
                            </span>
                          ) : (
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
                              Inactiva
                            </span>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                          {formatCrontab(task.crontab)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {task.last_run_at
                            ? new Date(task.last_run_at).toLocaleString()
                            : 'Nunca'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {task.total_run_count}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Modal de Detalles de Tarea */}
      {showTaskDetail && selectedTask && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-purple-700 text-white p-6 rounded-t-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold">{selectedTask.task_name.split('.').pop()}</h2>
                  <p className="text-purple-100 mt-1 text-sm">{selectedTask.task_name}</p>
                </div>
                <button
                  onClick={closeTaskDetail}
                  className="text-white hover:text-gray-200 text-2xl"
                >
                  ×
                </button>
              </div>
            </div>

            {/* Content */}
            <div className="p-6 space-y-6">
              {/* Status */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="text-sm text-gray-600">Estado</p>
                  <div className="flex items-center gap-2 mt-1">
                    {getStatusIcon(selectedTask.status)}
                    <span className={`text-2xl font-bold ${
                      selectedTask.status === 'SUCCESS' ? 'text-green-600' :
                      selectedTask.status === 'FAILURE' ? 'text-red-600' :
                      'text-blue-600'
                    }`}>
                      {selectedTask.status}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600">ID de Tarea</p>
                  <p className="text-xs font-mono text-gray-500 mt-1">{selectedTask.id}</p>
                </div>
              </div>

              {/* Timestamps */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm text-gray-600">Fecha de Inicio</p>
                  <p className="text-lg font-semibold text-blue-600 mt-1">
                    {new Date(selectedTask.date_created).toLocaleString('es-ES')}
                  </p>
                </div>
                {selectedTask.date_done && (
                  <div className="p-4 bg-green-50 rounded-lg">
                    <p className="text-sm text-gray-600">Fecha de Finalización</p>
                    <p className="text-lg font-semibold text-green-600 mt-1">
                      {new Date(selectedTask.date_done).toLocaleString('es-ES')}
                    </p>
                  </div>
                )}
              </div>

              {/* Result */}
              {selectedTask.status === 'SUCCESS' && selectedTask.result && (
                <div>
                  <h3 className="font-semibold text-gray-800 mb-3">Resultado</h3>
                  <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
                    {JSON.stringify(selectedTask.result, null, 2)}
                  </pre>
                </div>
              )}

              {/* Error */}
              {selectedTask.status === 'FAILURE' && selectedTask.traceback && (
                <div>
                  <h3 className="font-semibold text-red-600 mb-3">Error</h3>
                  <pre className="bg-red-50 p-4 rounded-lg overflow-x-auto text-sm text-red-800 max-h-64">
                    {selectedTask.traceback}
                  </pre>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="bg-gray-50 px-6 py-4 rounded-b-lg flex justify-end">
              <button
                onClick={closeTaskDetail}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
      </div>
    </MainLayout>
  );
};

export default CeleryMonitorPage;
