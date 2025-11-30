/**
 * Inventory page - Main inventory management interface
 */
import { useState, useEffect } from 'react';
import { FaPlus, FaSearch, FaExclamationTriangle } from 'react-icons/fa';
import { inventoryService } from '../services/inventoryService';
import SparePartList from '../components/inventory/SparePartList';
import SparePartForm from '../components/inventory/SparePartForm';
import MainLayout from '../components/layout/MainLayout';
import type { SparePart } from '../types/inventory.types';
import { formatCurrency } from '../utils/formatters';

const Inventory = () => {
  const [spareParts, setSpareParts] = useState<SparePart[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [selectedPart, setSelectedPart] = useState<SparePart | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [lowStockFilter, setLowStockFilter] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [statistics, setStatistics] = useState<any>(null);

  useEffect(() => {
    loadSpareParts();
    loadStatistics();
  }, [currentPage, searchTerm, categoryFilter, lowStockFilter]);

  const loadSpareParts = async () => {
    try {
      setLoading(true);
      const response = await inventoryService.getSpareParts({
        page: currentPage,
        search: searchTerm || undefined,
        category: categoryFilter || undefined,
        low_stock: lowStockFilter || undefined,
      });
      setSpareParts(response.results);
      setTotalPages(Math.ceil(response.count / 10));
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error al cargar repuestos');
      console.error('Error loading spare parts:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    try {
      const stats = await inventoryService.getStatistics();
      setStatistics(stats);
    } catch (err) {
      console.error('Error loading statistics:', err);
    }
  };

  const handleCreate = () => {
    setSelectedPart(null);
    setShowForm(true);
  };

  const handleEdit = (part: SparePart) => {
    setSelectedPart(part);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setSelectedPart(null);
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setSelectedPart(null);
    loadSpareParts();
    loadStatistics();
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('¿Está seguro de eliminar este repuesto?')) {
      return;
    }

    try {
      await inventoryService.deleteSparePart(id);
      loadSpareParts();
      loadStatistics();
    } catch (err: any) {
      alert(err.response?.data?.message || 'Error al eliminar repuesto');
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    loadSpareParts();
  };

  const categories = Array.from(
    new Set(spareParts.map((part) => part.category).filter(Boolean))
  );

  return (
    <MainLayout>
      <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Inventario</h1>
        <p className="text-gray-600">Gestión de repuestos y stock</p>
      </div>

      {/* Statistics Cards */}
      {statistics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Repuestos</p>
                <p className="text-2xl font-bold text-gray-800">
                  {statistics.total_parts}
                </p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <FaSearch className="text-blue-600 text-xl" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Stock Bajo</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {statistics.low_stock_count}
                </p>
              </div>
              <div className="bg-yellow-100 p-3 rounded-full">
                <FaExclamationTriangle className="text-yellow-600 text-xl" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Sin Stock</p>
                <p className="text-2xl font-bold text-red-600">
                  {statistics.out_of_stock_count}
                </p>
              </div>
              <div className="bg-red-100 p-3 rounded-full">
                <FaExclamationTriangle className="text-red-600 text-xl" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Valor Total</p>
                <p className="text-2xl font-bold text-green-600">
                  {formatCurrency(statistics.total_inventory_value)}
                </p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <span className="text-green-600 text-xl font-bold">$</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters and Actions */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <form onSubmit={handleSearch} className="flex-1">
            <div className="relative">
              <input
                type="text"
                placeholder="Buscar por número de parte o nombre..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <FaSearch className="absolute left-3 top-3 text-gray-400" />
            </div>
          </form>

          {/* Category Filter */}
          <select
            value={categoryFilter}
            onChange={(e) => {
              setCategoryFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todas las categorías</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>

          {/* Low Stock Filter */}
          <label className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
            <input
              type="checkbox"
              checked={lowStockFilter}
              onChange={(e) => {
                setLowStockFilter(e.target.checked);
                setCurrentPage(1);
              }}
              className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <span className="text-sm text-gray-700">Solo stock bajo</span>
          </label>

          {/* Create Button */}
          <button
            onClick={handleCreate}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <FaPlus />
            <span>Nuevo Repuesto</span>
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Spare Parts List */}
      <SparePartList
        spareParts={spareParts}
        loading={loading}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onRefresh={loadSpareParts}
      />

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-6">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Anterior
          </button>
          <span className="px-4 py-2 text-gray-700">
            Página {currentPage} de {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Siguiente
          </button>
        </div>
      )}

      {/* Form Modal */}
      {showForm && (
        <SparePartForm
          sparePart={selectedPart}
          onClose={handleFormClose}
          onSuccess={handleFormSuccess}
        />
      )}
      </div>
    </MainLayout>
  );
};

export default Inventory;
