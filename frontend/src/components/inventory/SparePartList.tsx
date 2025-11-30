/**
 * SparePartList component - Display list of spare parts
 */
import { useState } from 'react';
import { FaEdit, FaTrash, FaHistory, FaExclamationTriangle, FaCheckCircle } from 'react-icons/fa';
import type { SparePart } from '../../types/inventory.types';
import StockAdjustmentModal from './StockAdjustmentModal';
import StockHistoryModal from './StockHistoryModal';
import { formatCurrency } from '../../utils/formatters';

interface SparePartListProps {
  spareParts: SparePart[];
  loading: boolean;
  onEdit: (part: SparePart) => void;
  onDelete: (id: number) => void;
  onRefresh: () => void;
}

const SparePartList = ({
  spareParts,
  loading,
  onEdit,
  onDelete,
  onRefresh,
}: SparePartListProps) => {
  const [selectedPart, setSelectedPart] = useState<SparePart | null>(null);
  const [showAdjustment, setShowAdjustment] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  const handleAdjustStock = (part: SparePart) => {
    setSelectedPart(part);
    setShowAdjustment(true);
  };

  const handleViewHistory = (part: SparePart) => {
    setSelectedPart(part);
    setShowHistory(true);
  };

  const handleAdjustmentSuccess = () => {
    setShowAdjustment(false);
    setSelectedPart(null);
    onRefresh();
  };

  const getStockStatusBadge = (part: SparePart) => {
    if (part.quantity === 0) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-1 bg-red-100 text-red-800 text-xs font-medium rounded-full">
          <FaExclamationTriangle />
          Sin Stock
        </span>
      );
    } else if (part.is_low_stock) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-full">
          <FaExclamationTriangle />
          Stock Bajo
        </span>
      );
    } else {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
          <FaCheckCircle />
          Stock Normal
        </span>
      );
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Cargando repuestos...</p>
      </div>
    );
  }

  if (spareParts.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-600">No se encontraron repuestos</p>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Número de Parte
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nombre
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Categoría
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Cantidad
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Costo Unit.
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Valor Total
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {spareParts.map((part) => (
                <tr key={part.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {part.part_number}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900">{part.name}</div>
                    {part.manufacturer && (
                      <div className="text-xs text-gray-500">{part.manufacturer}</div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{part.category || '-'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {part.quantity} {part.unit_of_measure}
                    </div>
                    <div className="text-xs text-gray-500">
                      Mín: {part.min_quantity}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStockStatusBadge(part)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {formatCurrency(part.unit_cost)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {formatCurrency(part.total_value)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => handleAdjustStock(part)}
                        className="text-blue-600 hover:text-blue-900"
                        title="Ajustar Stock"
                      >
                        Ajustar
                      </button>
                      <button
                        onClick={() => handleViewHistory(part)}
                        className="text-gray-600 hover:text-gray-900"
                        title="Ver Historial"
                      >
                        <FaHistory />
                      </button>
                      <button
                        onClick={() => onEdit(part)}
                        className="text-indigo-600 hover:text-indigo-900"
                        title="Editar"
                      >
                        <FaEdit />
                      </button>
                      <button
                        onClick={() => onDelete(part.id)}
                        className="text-red-600 hover:text-red-900"
                        title="Eliminar"
                      >
                        <FaTrash />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Stock Adjustment Modal */}
      {showAdjustment && selectedPart && (
        <StockAdjustmentModal
          sparePart={selectedPart}
          onClose={() => {
            setShowAdjustment(false);
            setSelectedPart(null);
          }}
          onSuccess={handleAdjustmentSuccess}
        />
      )}

      {/* Stock History Modal */}
      {showHistory && selectedPart && (
        <StockHistoryModal
          sparePart={selectedPart}
          onClose={() => {
            setShowHistory(false);
            setSelectedPart(null);
          }}
        />
      )}
    </>
  );
};

export default SparePartList;
