import { useState, useEffect } from 'react';
import { FaRobot, FaExclamationTriangle, FaCheckCircle, FaChartLine } from 'react-icons/fa';
import toast from 'react-hot-toast';
import MainLayout from '../components/layout/MainLayout';
import api from '../services/api';

interface Prediction {
  id: string;
  asset: {
    id: string;
    name: string;
    vehicle_type: string;
  };
  failure_probability: number;
  risk_level: string;
  estimated_days_to_failure: number;
  prediction_date: string;
  recommended_action: string;
  work_order_created: any;
  features_snapshot?: Record<string, any>;
}

interface ErrorState {
  hasError: boolean;
  errorMessage: string;
  errorType: 'network' | 'server' | 'model' | 'unknown';
}

const MLPredictionsPage = () => {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');
  const [selectedPrediction, setSelectedPrediction] = useState<Prediction | null>(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [error, setError] = useState<ErrorState>({
    hasError: false,
    errorMessage: '',
    errorType: 'unknown'
  });
  const [stats, setStats] = useState({
    total: 0,
    high_risk: 0,
    medium_risk: 0,
    low_risk: 0,
  });

  useEffect(() => {
    fetchPredictions();
  }, [filter]);

  const fetchPredictions = async () => {
    try {
      setLoading(true);
      
      let url = '/ml-predictions/predictions/';
      if (filter === 'high_risk') {
        url = '/ml-predictions/predictions/high_risk/';
      }

      const response = await api.get(url);

      setPredictions(response.data.results || response.data);
      calculateStats(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching predictions:', error);
      toast.error('Error al cargar predicciones');
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (data: Prediction[]) => {
    const stats = {
      total: data.length,
      high_risk: data.filter(p => ['HIGH', 'CRITICAL'].includes(p.risk_level)).length,
      medium_risk: data.filter(p => p.risk_level === 'MEDIUM').length,
      low_risk: data.filter(p => p.risk_level === 'LOW').length,
    };
    setStats(stats);
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'HIGH':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'LOW':
        return 'bg-green-100 text-green-800 border-green-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getRiskIcon = (level: string) => {
    switch (level) {
      case 'CRITICAL':
      case 'HIGH':
        return <FaExclamationTriangle className="text-red-500" />;
      case 'MEDIUM':
        return <FaExclamationTriangle className="text-yellow-500" />;
      case 'LOW':
        return <FaCheckCircle className="text-green-500" />;
      default:
        return null;
    }
  };

  const openDetailModal = (prediction: Prediction) => {
    setSelectedPrediction(prediction);
    setShowDetailModal(true);
  };

  const closeDetailModal = () => {
    setShowDetailModal(false);
    setSelectedPrediction(null);
  };

  const handlePredictionError = (error: any) => {
    if (error.response) {
      // Server responded with error
      const status = error.response.status;
      const data = error.response.data;
      
      if (status === 503) {
        setError({
          hasError: true,
          errorMessage: data.error || 'El modelo ML no está disponible. Por favor contacte al administrador.',
          errorType: 'model'
        });
        toast.error('Modelo ML no disponible', { id: 'predictions' });
      } else if (status === 500) {
        setError({
          hasError: true,
          errorMessage: data.error || 'Error interno del servidor',
          errorType: 'server'
        });
        toast.error('Error del servidor', { id: 'predictions' });
      } else {
        setError({
          hasError: true,
          errorMessage: data.error || 'Error desconocido',
          errorType: 'unknown'
        });
        toast.error('Error al ejecutar predicciones', { id: 'predictions' });
      }
    } else if (error.request) {
      // Network error
      setError({
        hasError: true,
        errorMessage: 'Error de conexión. Verifique su conexión a internet.',
        errorType: 'network'
      });
      toast.error('Error de conexión', { id: 'predictions' });
    } else {
      setError({
        hasError: true,
        errorMessage: error.message || 'Error desconocido',
        errorType: 'unknown'
      });
      toast.error('Error inesperado', { id: 'predictions' });
    }
  };

  const runPredictions = async () => {
    try {
      setLoading(true);
      setError({ hasError: false, errorMessage: '', errorType: 'unknown' });
      
      toast.loading('Ejecutando predicciones...', { id: 'predictions' });
      await api.post('/ml-predictions/predictions/run_predictions/');
      toast.success('Predicciones iniciadas. Se ejecutarán en segundo plano.', { id: 'predictions' });
      
      // Recargar después de 5 segundos
      setTimeout(() => {
        fetchPredictions();
      }, 5000);
    } catch (error) {
      console.error('Error running predictions:', error);
      handlePredictionError(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <FaRobot className="text-3xl text-blue-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-800">Predicciones ML</h1>
                <p className="text-gray-600 text-sm">
                  Sistema de predicción de fallos basado en Machine Learning
                </p>
              </div>
            </div>
            <button
              onClick={runPredictions}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2 transition-colors"
            >
              <FaRobot />
              Ejecutar Predicciones
            </button>
          </div>
        </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Predicciones</p>
              <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
            </div>
            <FaChartLine className="text-3xl text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Alto Riesgo</p>
              <p className="text-2xl font-bold text-red-600">{stats.high_risk}</p>
            </div>
            <FaExclamationTriangle className="text-3xl text-red-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Riesgo Medio</p>
              <p className="text-2xl font-bold text-yellow-600">{stats.medium_risk}</p>
            </div>
            <FaExclamationTriangle className="text-3xl text-yellow-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Bajo Riesgo</p>
              <p className="text-2xl font-bold text-green-600">{stats.low_risk}</p>
            </div>
            <FaCheckCircle className="text-3xl text-green-500" />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg ${
              filter === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Todas
          </button>
          <button
            onClick={() => setFilter('high_risk')}
            className={`px-4 py-2 rounded-lg ${
              filter === 'high_risk'
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Alto Riesgo
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error.hasError && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6 rounded">
          <div className="flex items-start">
            <FaExclamationTriangle className="text-red-600 mt-1 mr-3" />
            <div>
              <p className="font-semibold text-red-800">Error</p>
              <p className="text-red-700 mt-1">{error.errorMessage}</p>
              {error.errorType === 'model' && (
                <p className="text-red-600 text-sm mt-2">
                  El modelo de Machine Learning necesita ser entrenado. Contacte al administrador del sistema.
                </p>
              )}
              {error.errorType === 'network' && (
                <p className="text-red-600 text-sm mt-2">
                  Verifique su conexión a internet e intente nuevamente.
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Predictions List */}
      <div className="bg-white rounded-lg shadow">
        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Cargando predicciones...</p>
          </div>
        ) : predictions.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <FaRobot className="text-6xl mx-auto mb-4 text-gray-300" />
            <p>No hay predicciones disponibles</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Activo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Riesgo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Probabilidad
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Días Estimados
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    OT Creada
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acción Recomendada
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {predictions.map((prediction) => (
                  <tr 
                    key={prediction.id} 
                    className="hover:bg-gray-50 cursor-pointer"
                    onClick={() => openDetailModal(prediction)}
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {prediction.asset.name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {prediction.asset.vehicle_type}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium border ${getRiskColor(
                          prediction.risk_level
                        )}`}
                      >
                        {getRiskIcon(prediction.risk_level)}
                        {prediction.risk_level}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-full bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className={`h-2 rounded-full ${
                              prediction.failure_probability >= 0.7
                                ? 'bg-red-600'
                                : prediction.failure_probability >= 0.4
                                ? 'bg-yellow-600'
                                : 'bg-green-600'
                            }`}
                            style={{
                              width: `${prediction.failure_probability * 100}%`,
                            }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-gray-700">
                          {(prediction.failure_probability * 100).toFixed(1)}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {prediction.estimated_days_to_failure} días
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(prediction.prediction_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {prediction.work_order_created ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          ✓ Sí
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          No
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {prediction.recommended_action}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal de Detalles */}
      {showDetailModal && selectedPrediction && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-t-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold">{selectedPrediction.asset.name}</h2>
                  <p className="text-blue-100 mt-1">{selectedPrediction.asset.vehicle_type}</p>
                </div>
                <button
                  onClick={closeDetailModal}
                  className="text-white hover:text-gray-200 text-2xl"
                >
                  ×
                </button>
              </div>
            </div>

            {/* Content */}
            <div className="p-6 space-y-6">
              {/* Risk Level */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="text-sm text-gray-600">Nivel de Riesgo</p>
                  <div className="flex items-center gap-2 mt-1">
                    {getRiskIcon(selectedPrediction.risk_level)}
                    <span className={`text-2xl font-bold ${
                      selectedPrediction.risk_level === 'CRITICAL' ? 'text-red-600' :
                      selectedPrediction.risk_level === 'HIGH' ? 'text-orange-600' :
                      selectedPrediction.risk_level === 'MEDIUM' ? 'text-yellow-600' :
                      'text-green-600'
                    }`}>
                      {selectedPrediction.risk_level}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600">Probabilidad de Fallo</p>
                  <p className="text-3xl font-bold text-blue-600">
                    {(selectedPrediction.failure_probability * 100).toFixed(1)}%
                  </p>
                </div>
              </div>

              {/* Progress Bar */}
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Probabilidad de Fallo</span>
                  <span className="font-medium">{(selectedPrediction.failure_probability * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div
                    className={`h-4 rounded-full ${
                      selectedPrediction.failure_probability >= 0.7 ? 'bg-red-600' :
                      selectedPrediction.failure_probability >= 0.4 ? 'bg-yellow-600' :
                      'bg-green-600'
                    }`}
                    style={{ width: `${selectedPrediction.failure_probability * 100}%` }}
                  ></div>
                </div>
              </div>

              {/* Details Grid */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm text-gray-600">Días Estimados hasta Fallo</p>
                  <p className="text-2xl font-bold text-blue-600 mt-1">
                    {selectedPrediction.estimated_days_to_failure} días
                  </p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <p className="text-sm text-gray-600">Fecha de Predicción</p>
                  <p className="text-lg font-semibold text-purple-600 mt-1">
                    {new Date(selectedPrediction.prediction_date).toLocaleDateString('es-ES', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </p>
                </div>
              </div>

              {/* Recommended Action */}
              <div className="p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                <div className="flex items-start">
                  <FaExclamationTriangle className="text-yellow-600 mt-1 mr-3" />
                  <div>
                    <p className="font-semibold text-yellow-800">Acción Recomendada</p>
                    <p className="text-yellow-700 mt-1">{selectedPrediction.recommended_action}</p>
                  </div>
                </div>
              </div>

              {/* Work Order Status */}
              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-2">Estado de Orden de Trabajo</p>
                {selectedPrediction.work_order_created ? (
                  <div className="flex items-center gap-2 text-green-600">
                    <FaCheckCircle />
                    <span className="font-semibold">Orden de trabajo creada automáticamente</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 text-gray-500">
                    <span>No se ha creado orden de trabajo</span>
                  </div>
                )}
              </div>

              {/* Features Snapshot */}
              {selectedPrediction.features_snapshot && Object.keys(selectedPrediction.features_snapshot).length > 0 && (
                <div>
                  <h3 className="font-semibold text-gray-800 mb-3">Datos del Análisis</h3>
                  <div className="grid grid-cols-2 gap-3">
                    {Object.entries(selectedPrediction.features_snapshot).map(([key, value]) => (
                      <div key={key} className="p-3 bg-gray-50 rounded">
                        <p className="text-xs text-gray-500 capitalize">{key.replace(/_/g, ' ')}</p>
                        <p className="font-medium text-gray-800">{String(value)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="bg-gray-50 px-6 py-4 rounded-b-lg flex justify-end gap-3">
              <button
                onClick={closeDetailModal}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                Cerrar
              </button>
              {selectedPrediction.work_order_created && (
                <button
                  onClick={() => {
                    // Navegar a la orden de trabajo
                    window.location.href = '/work-orders';
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Ver Orden de Trabajo
                </button>
              )}
            </div>
          </div>
        </div>
      )}
      </div>
    </MainLayout>
  );
};

export default MLPredictionsPage;
