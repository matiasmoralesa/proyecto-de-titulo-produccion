/**
 * StockHistoryModal component - Modal for viewing stock movement history
 */
import { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import { inventoryService } from '../../services/inventoryService';
import type { SparePart, StockMovement } from '../../types/inventory.types';
import { formatCurrency, formatDateTime } from '../../utils/formatters';

interface StockHistoryModalProps {
  sparePart: SparePart;
  onClose: () => void;
}

const StockHistoryModal = ({ sparePart, onClose }: StockHistoryModalProps) => {
  const [movements, setMovements] = useState<StockMovement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await inventoryService.getStockHistory(sparePart.id);
      setMovements(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error al cargar historial');
      console.error('Error loading stock history:', err);
    } finally {
      setLoading(false);
    }
  };



  const getMovementColor = (type: string) => {
    switch (type) {
      case 'IN':
      case 'RETURN':
      case 'INITIAL':
        return 'text-green-600 bg-green-50';
      case 'OUT':
        return 'text-red-600 bg-red-50';
      case 'ADJUSTMENT':
        return 'text-blue-600 bg-blue-50';
      case 'TRANSFER':
        return 'text-purple-600 bg-purple-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Historial de Movimientos</h2>
            <p className="text-sm text-gray-600 mt-1">
              {sparePart.part_number} - {sparePart.name}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <FaTimes size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Cargando historial...</p>
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          ) : movements.length === 0 ? (
            <div className="text-center py-8 text-gray-600">
              No hay movimientos registrados
            </div>
          ) : (
            <div className="space-y-4">
              {movements.map((movement) => (
                <div
                  key={movement.id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span
                          className={`px-3 py-1 rounded-full text-sm font-medium ${getMovementColor(
                            movement.movement_type
                          )}`}
                        >
                          {movement.movement_type_display}
                        </span>
                        <span className="text-sm text-gray-600">
                          {formatDateTime(movement.created_at)}
                        </span>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                        <div>
                          <p className="text-xs text-gray-500">Cantidad</p>
                          <p className="text-sm font-medium text-gray-900">
                            {movement.quantity > 0 ? '+' : ''}
                            {movement.quantity} {sparePart.unit_of_measure}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-500">Stock Anterior</p>
                          <p className="text-sm font-medium text-gray-900">
                            {movement.quantity_before}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-500">Stock Posterior</p>
                          <p className="text-sm font-medium text-gray-900">
                            {movement.quantity_after}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-500">Costo Total</p>
                          <p className="text-sm font-medium text-gray-900">
                            {formatCurrency(movement.total_cost)}
                          </p>
                        </div>
                      </div>

                      {movement.notes && (
                        <div className="mb-2">
                          <p className="text-xs text-gray-500">Notas</p>
                          <p className="text-sm text-gray-700">{movement.notes}</p>
                        </div>
                      )}

                      {(movement.reference_type || movement.reference_id) && (
                        <div className="flex items-center gap-4 text-xs text-gray-500">
                          {movement.reference_type && (
                            <span>Tipo: {movement.reference_type}</span>
                          )}
                          {movement.reference_id && (
                            <span>Ref: {movement.reference_id}</span>
                          )}
                        </div>
                      )}
                    </div>

                    <div className="text-right ml-4">
                      <p className="text-xs text-gray-500">Usuario</p>
                      <p className="text-sm font-medium text-gray-900">
                        {movement.user.username}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};

export default StockHistoryModal;
