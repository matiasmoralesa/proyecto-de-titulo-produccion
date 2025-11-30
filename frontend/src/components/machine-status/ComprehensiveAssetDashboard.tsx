import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import machineStatusService, { AssetStatus } from '../../services/machineStatusService';
import assetService, { Asset } from '../../services/assetService';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

interface AssetWithStatus extends Asset {
  current_status?: AssetStatus;
}

const ComprehensiveAssetDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [assets, setAssets] = useState<AssetWithStatus[]>([]);
  const [statuses, setStatuses] = useState<AssetStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [filterVehicleType, setFilterVehicleType] = useState<string>('');
  const [filterLocation, setFilterLocation] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [assetsResponse, statusesResponse] = await Promise.all([
        assetService.getAssets(),
        machineStatusService.getStatuses()
      ]);

      const assetsList = assetsResponse.results || assetsResponse;
      const statusList = statusesResponse.results || statusesResponse;

      // Merge assets with their current status
      const assetsWithStatus = assetsList.map((asset: Asset) => {
        const status = statusList.find((s: AssetStatus) => s.asset === asset.id);
        return {
          ...asset,
          current_status: status
        };
      });

      setAssets(assetsWithStatus);
      setStatuses(statusList);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Filter assets
  const filteredAssets = assets.filter(asset => {
    const matchesSearch = !searchTerm || 
      asset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      asset.serial_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      asset.license_plate?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = !filterStatus || asset.current_status?.status_type === filterStatus;
    const matchesVehicleType = !filterVehicleType || asset.vehicle_type === filterVehicleType;
    const matchesLocation = !filterLocation || asset.location_name === filterLocation;

    return matchesSearch && matchesStatus && matchesVehicleType && matchesLocation;
  });

  // Status distribution data
  const getStatusDistribution = () => {
    const statusCounts = {
      OPERANDO: 0,
      DETENIDA: 0,
      EN_MANTENIMIENTO: 0,
      FUERA_DE_SERVICIO: 0,
    };

    statuses.forEach((status) => {
      statusCounts[status.status_type as keyof typeof statusCounts]++;
    });

    return {
      labels: ['Operando', 'Detenida', 'En Mantenimiento', 'Fuera de Servicio'],
      datasets: [
        {
          data: [
            statusCounts.OPERANDO,
            statusCounts.DETENIDA,
            statusCounts.EN_MANTENIMIENTO,
            statusCounts.FUERA_DE_SERVICIO,
          ],
          backgroundColor: [
            '#10B981', // Green
            '#F59E0B', // Yellow
            '#3B82F6', // Blue
            '#EF4444', // Red
          ],
          borderColor: [
            '#059669',
            '#D97706',
            '#2563EB',
            '#DC2626',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  // Fuel level distribution
  const getFuelLevelData = () => {
    const fuelRanges = {
      'Crítico (0-25%)': 0,
      'Bajo (26-50%)': 0,
      'Medio (51-75%)': 0,
      'Alto (76-100%)': 0,
    };

    statuses.forEach((status) => {
      if (status.fuel_level !== null) {
        if (status.fuel_level <= 25) fuelRanges['Crítico (0-25%)']++;
        else if (status.fuel_level <= 50) fuelRanges['Bajo (26-50%)']++;
        else if (status.fuel_level <= 75) fuelRanges['Medio (51-75%)']++;
        else fuelRanges['Alto (76-100%)']++;
      }
    });

    return {
      labels: Object.keys(fuelRanges),
      datasets: [
        {
          label: 'Número de Activos',
          data: Object.values(fuelRanges),
          backgroundColor: [
            '#EF4444', // Red for critical
            '#F59E0B', // Yellow for low
            '#3B82F6', // Blue for medium
            '#10B981', // Green for high
          ],
          borderColor: [
            '#DC2626',
            '#D97706',
            '#2563EB',
            '#059669',
          ],
          borderWidth: 1,
        },
      ],
    };
  };

  // Vehicle type distribution
  const getVehicleTypeDistribution = () => {
    const typeCounts: Record<string, number> = {};
    
    assets.forEach(asset => {
      typeCounts[asset.vehicle_type] = (typeCounts[asset.vehicle_type] || 0) + 1;
    });

    return {
      labels: Object.keys(typeCounts),
      datasets: [
        {
          label: 'Cantidad',
          data: Object.values(typeCounts),
          backgroundColor: '#3B82F6',
          borderColor: '#2563EB',
          borderWidth: 1,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
    },
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
    },
  };

  const getStatusColor = (statusType: string) => {
    switch (statusType) {
      case 'OPERANDO':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'DETENIDA':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'EN_MANTENIMIENTO':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'FUERA_DE_SERVICIO':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  // Get unique values for filters
  const uniqueVehicleTypes = Array.from(new Set(assets.map(a => a.vehicle_type)));
  const uniqueLocations = Array.from(new Set(assets.map(a => a.location_name)));
  const statusTypes = ['OPERANDO', 'DETENIDA', 'EN_MANTENIMIENTO', 'FUERA_DE_SERVICIO'];

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="text-blue-600 font-bold text-xl">📦</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Activos</p>
              <p className="text-2xl font-bold text-gray-900">{assets.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <span className="text-green-600 font-bold text-xl">✓</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Operando</p>
              <p className="text-2xl font-bold text-gray-900">
                {statuses.filter(s => s.status_type === 'OPERANDO').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="text-blue-600 font-bold text-xl">🔧</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Mantenimiento</p>
              <p className="text-2xl font-bold text-gray-900">
                {statuses.filter(s => s.status_type === 'EN_MANTENIMIENTO').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                <span className="text-red-600 font-bold text-xl">⚠</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Fuera Servicio</p>
              <p className="text-2xl font-bold text-gray-900">
                {statuses.filter(s => s.status_type === 'FUERA_DE_SERVICIO').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Status Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Distribución de Estados
          </h3>
          <div className="h-64">
            <Doughnut data={getStatusDistribution()} options={doughnutOptions} />
          </div>
        </div>

        {/* Fuel Level Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Niveles de Combustible
          </h3>
          <div className="h-64">
            <Bar data={getFuelLevelData()} options={chartOptions} />
          </div>
        </div>

        {/* Vehicle Type Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Tipos de Vehículos
          </h3>
          <div className="h-64">
            <Bar data={getVehicleTypeDistribution()} options={chartOptions} />
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Filtros y Búsqueda</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Buscar por nombre, serial, placa..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
          
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Todos los estados</option>
            {statusTypes.map(type => (
              <option key={type} value={type}>{type.replace('_', ' ')}</option>
            ))}
          </select>

          <select
            value={filterVehicleType}
            onChange={(e) => setFilterVehicleType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Todos los tipos</option>
            {uniqueVehicleTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>

          <select
            value={filterLocation}
            onChange={(e) => setFilterLocation(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Todas las ubicaciones</option>
            {uniqueLocations.map(location => (
              <option key={location} value={location}>{location}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Assets Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Todos los Activos ({filteredAssets.length})
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Activo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tipo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Serial / Placa
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ubicación
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Combustible
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Odómetro
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredAssets.map((asset) => (
                <tr key={asset.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{asset.name}</div>
                    <div className="text-sm text-gray-500">{asset.model}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {asset.vehicle_type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{asset.serial_number}</div>
                    <div className="text-sm text-gray-500">{asset.license_plate || 'N/A'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {asset.location_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {asset.current_status ? (
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full border ${getStatusColor(asset.current_status.status_type)}`}>
                        {asset.current_status.status_type_display}
                      </span>
                    ) : (
                      <span className="text-sm text-gray-500">Sin estado</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {asset.current_status?.fuel_level !== null ? (
                      <div className="flex items-center">
                        <div className="flex-1 mr-2">
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${
                                (asset.current_status?.fuel_level || 0) > 50
                                  ? 'bg-green-500'
                                  : (asset.current_status?.fuel_level || 0) > 25
                                  ? 'bg-yellow-500'
                                  : 'bg-red-500'
                              }`}
                              style={{ width: `${asset.current_status?.fuel_level || 0}%` }}
                            ></div>
                          </div>
                        </div>
                        <span className="text-sm text-gray-900 font-medium">
                          {asset.current_status?.fuel_level}%
                        </span>
                      </div>
                    ) : (
                      <span className="text-sm text-gray-500">N/A</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {asset.current_status?.odometer_reading || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => navigate(`/assets/${asset.id}`)}
                      className="text-blue-600 hover:text-blue-900 hover:underline"
                    >
                      Ver Detalle
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ComprehensiveAssetDashboard;
