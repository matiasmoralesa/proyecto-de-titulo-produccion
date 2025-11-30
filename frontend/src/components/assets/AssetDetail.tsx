/**
 * Asset Detail Component
 */
import { useState, useEffect } from 'react';
import {
  FiX,
  FiTruck,
  FiMapPin,
  FiHash,
  FiCreditCard,
  FiCalendar,
  FiEdit,
  FiTrash2,
  FiFileText,
} from 'react-icons/fi';
import { Asset } from '../../types/asset.types';
import assetService from '../../services/assetService';

interface AssetDetailProps {
  assetId: string;
  onClose: () => void;
  onEdit: (asset: Asset) => void;
  onDelete: () => void;
}

export default function AssetDetail({ assetId, onClose, onEdit, onDelete }: AssetDetailProps) {
  const [asset, setAsset] = useState<Asset | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAsset();
  }, [assetId]);

  const loadAsset = async () => {
    try {
      const data = await assetService.getAsset(assetId);
      setAsset(data);
    } catch (error) {
      console.error('Error loading asset:', error);
    } finally {
      setLoading(false);
    }
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

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      </div>
    );
  }

  if (!asset) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <h2 className="text-xl font-bold text-gray-900">{asset.name}</h2>
              <span
                className={`px-3 py-1 text-xs font-semibold rounded-full border ${getStatusColor(
                  asset.status
                )}`}
              >
                {asset.status}
              </span>
            </div>
            <p className="text-gray-600">{asset.asset_number}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <FiX className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Basic Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Información Básica</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-start space-x-3">
                <FiTruck className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500">Tipo de Vehículo</p>
                  <p className="font-semibold text-gray-900">{asset.vehicle_type}</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <FiMapPin className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500">Ubicación</p>
                  <p className="font-semibold text-gray-900">{asset.location_name}</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <FiHash className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500">Número de Serie</p>
                  <p className="font-mono text-gray-900">{asset.serial_number}</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <FiCreditCard className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500">Placa</p>
                  <p className="font-mono text-gray-900">{asset.license_plate || 'N/A'}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Vehicle Details */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Detalles del Vehículo</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Fabricante</p>
                <p className="font-semibold text-gray-900">{asset.manufacturer || 'N/A'}</p>
              </div>

              <div>
                <p className="text-sm text-gray-500">Modelo</p>
                <p className="font-semibold text-gray-900">{asset.model || 'N/A'}</p>
              </div>

              <div>
                <p className="text-sm text-gray-500">Año</p>
                <p className="font-semibold text-gray-900">{asset.year || 'N/A'}</p>
              </div>

              <div className="flex items-start space-x-3">
                <FiCalendar className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500">Fecha de Registro</p>
                  <p className="font-semibold text-gray-900">
                    {new Date(asset.created_at).toLocaleDateString('es-ES')}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Description */}
          {asset.description && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Descripción</h3>
              <p className="text-gray-600 whitespace-pre-wrap">{asset.description}</p>
            </div>
          )}

          {/* Documents Section */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">Documentos</h3>
              <button className="text-sm text-primary-600 hover:text-primary-700 font-medium">
                + Subir Documento
              </button>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center">
              <FiFileText className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-500">No hay documentos adjuntos</p>
            </div>
          </div>

          {/* Statistics */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">Estadísticas</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-900">0</p>
                <p className="text-sm text-blue-700">Órdenes de Trabajo</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-900">0</p>
                <p className="text-sm text-blue-700">Mantenimientos</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-900">0</p>
                <p className="text-sm text-blue-700">Horas de Uso</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-900">0</p>
                <p className="text-sm text-blue-700">Documentos</p>
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={() => onEdit(asset)}
            className="flex items-center space-x-2 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg font-medium transition-colors"
          >
            <FiEdit className="w-4 h-4" />
            <span>Editar</span>
          </button>
          <button
            onClick={onDelete}
            className="flex items-center space-x-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors"
          >
            <FiTrash2 className="w-4 h-4" />
            <span>Eliminar</span>
          </button>
        </div>
      </div>
    </div>
  );
}
