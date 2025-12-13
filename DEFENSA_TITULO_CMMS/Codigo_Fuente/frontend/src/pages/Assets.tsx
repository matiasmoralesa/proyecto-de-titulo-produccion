/**
 * Assets page component
 */
import { useState, useEffect } from 'react';
import assetService from '../services/assetService';
import { Asset } from '../types/asset.types';
import MainLayout from '../components/layout/MainLayout';
import { FiTruck, FiMapPin, FiHash, FiCreditCard, FiFilter } from 'react-icons/fi';
import AssetForm from '../components/assets/AssetForm';
import AssetDetail from '../components/assets/AssetDetail';

export default function Assets() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [showDetail, setShowDetail] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [selectedAssetId, setSelectedAssetId] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    vehicle_type: '',
    status: '',
    search: '',
  });

  useEffect(() => {
    loadAssets();
  }, [filters]);

  const loadAssets = async () => {
    try {
      setLoading(true);
      const response = await assetService.getAssets(filters);
      setAssets(response.results);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al cargar activos');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNew = () => {
    setSelectedAsset(null);
    setShowForm(true);
  };

  const handleEdit = (asset: Asset) => {
    setSelectedAsset(asset);
    setShowDetail(false);
    setShowForm(true);
  };

  const handleViewDetail = (assetId: string) => {
    setSelectedAssetId(assetId);
    setShowDetail(true);
  };

  const handleDelete = async () => {
    if (!selectedAssetId) return;

    if (window.confirm('¿Estás seguro de que deseas eliminar este activo?')) {
      try {
        await assetService.deleteAsset(selectedAssetId);
        setShowDetail(false);
        loadAssets();
      } catch (error) {
        console.error('Error deleting asset:', error);
        alert('Error al eliminar el activo');
      }
    }
  };

  const handleFormSuccess = () => {
    loadAssets();
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      Operando: 'bg-green-100 text-green-800 border-green-200',
      Detenida: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'En Mantenimiento': 'bg-blue-100 text-blue-800 border-blue-200',
      'Fuera de Servicio': 'bg-red-100 text-red-800 border-red-200',
    };
    return colors[status] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getVehicleIcon = (type: string) => {
    return <FiTruck className="w-5 h-5" />;
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">Cargando activos...</p>
          </div>
        </div>
      </MainLayout>
    );
  }

  const vehicleTypes = [
    'Camión Supersucker',
    'Camioneta MDO',
    'Retroexcavadora MDO',
    'Cargador Frontal MDO',
    'Minicargador MDO',
  ];

  const statusOptions = ['Operando', 'Detenida', 'En Mantenimiento', 'Fuera de Servicio'];

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Gestión de Activos</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Vehículos y equipos del sistema</p>
          </div>
          <button
            onClick={handleCreateNew}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
          >
            + Nuevo Activo
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Filters */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
          <div className="flex items-center space-x-2 mb-3">
            <FiFilter className="w-5 h-5 text-gray-400 dark:text-gray-500" />
            <h3 className="font-medium text-gray-900 dark:text-white">Filtros</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Tipo de Vehículo
              </label>
              <select
                value={filters.vehicle_type}
                onChange={(e) => setFilters({ ...filters, vehicle_type: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">Todos</option>
                {vehicleTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Estado</label>
              <select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
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
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Buscar</label>
              <input
                type="text"
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                placeholder="Buscar por nombre, placa..."
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
              />
            </div>
          </div>
        </div>

        {/* Assets Grid */}
        {assets.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-12 text-center">
            <FiTruck className="w-16 h-16 text-gray-400 dark:text-gray-600 mx-auto mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No hay activos registrados</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {assets.map((asset) => (
              <div
                key={asset.id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200 dark:border-gray-700 overflow-hidden"
              >
                {/* Card Header */}
                <div className="bg-gradient-to-r from-primary-600 to-primary-700 p-4 text-white">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      {getVehicleIcon(asset.vehicle_type)}
                      <div>
                        <h3 className="font-semibold text-lg">{asset.name}</h3>
                        <p className="text-sm text-primary-100">{asset.model}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Card Body */}
                <div className="p-4 space-y-3">
                  <div className="flex items-center space-x-2 text-sm">
                    <FiTruck className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                    <span className="text-gray-600 dark:text-gray-400">Tipo:</span>
                    <span className="font-medium text-gray-900 dark:text-white">{asset.vehicle_type}</span>
                  </div>

                  <div className="flex items-center space-x-2 text-sm">
                    <FiHash className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                    <span className="text-gray-600 dark:text-gray-400">Serial:</span>
                    <span className="font-mono text-gray-900 dark:text-white">{asset.serial_number}</span>
                  </div>

                  <div className="flex items-center space-x-2 text-sm">
                    <FiCreditCard className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                    <span className="text-gray-600 dark:text-gray-400">Placa:</span>
                    <span className="font-mono text-gray-900 dark:text-white">
                      {asset.license_plate || 'N/A'}
                    </span>
                  </div>

                  <div className="flex items-center space-x-2 text-sm">
                    <FiMapPin className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                    <span className="text-gray-600 dark:text-gray-400">Ubicación:</span>
                    <span className="text-gray-900 dark:text-white">{asset.location_name}</span>
                  </div>

                  {/* Status Badge */}
                  <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                    <span
                      className={`px-3 py-1 inline-flex text-xs font-semibold rounded-full border ${getStatusColor(
                        asset.status
                      )}`}
                    >
                      {asset.status}
                    </span>
                  </div>
                </div>

                {/* Card Footer */}
                <div className="px-4 py-3 bg-gray-50 dark:bg-gray-700/50 border-t border-gray-100 dark:border-gray-700">
                  <button
                    onClick={() => handleViewDetail(asset.id)}
                    className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
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
        <AssetForm
          asset={selectedAsset || undefined}
          onClose={() => setShowForm(false)}
          onSuccess={handleFormSuccess}
        />
      )}

      {showDetail && selectedAssetId && (
        <AssetDetail
          assetId={selectedAssetId}
          onClose={() => setShowDetail(false)}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}
    </MainLayout>
  );
}
