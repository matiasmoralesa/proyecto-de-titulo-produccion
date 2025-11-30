import React, { useState, useEffect } from 'react';
import MainLayout from '../components/layout/MainLayout';
import StatusHistoryViewer from '../components/machine-status/StatusHistoryViewer';
import assetService from '../services/assetService';

const StatusHistoryPage: React.FC = () => {
  const [assets, setAssets] = useState<any[]>([]);
  const [selectedAsset, setSelectedAsset] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    try {
      setLoading(true);
      const response = await assetService.getAssets();
      const assetsList = response.results || response;
      setAssets(assetsList);
    } catch (error) {
      console.error('Error loading assets:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Historial de Estados</h1>
          <p className="text-gray-600 mt-1">
            Visualiza el historial completo de cambios de estado de los activos
          </p>
        </div>

        {/* Asset Filter */}
        {!loading && (
          <div className="bg-white p-4 rounded-lg shadow">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filtrar por Activo
            </label>
            <select
              value={selectedAsset}
              onChange={(e) => setSelectedAsset(e.target.value)}
              className="w-full md:w-1/3 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos los activos</option>
              {assets.map((asset) => (
                <option key={asset.id} value={asset.id}>
                  {asset.name} - {asset.vehicle_type}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* History Viewer */}
        <StatusHistoryViewer assetId={selectedAsset || undefined} />
      </div>
    </MainLayout>
  );
};

export default StatusHistoryPage;
