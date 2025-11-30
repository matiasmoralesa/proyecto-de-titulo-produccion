/**
 * Locations Management Page (Admin Only)
 */
import React, { useState, useEffect } from 'react';
import MainLayout from '../components/layout/MainLayout';
import { locationService } from '../services/locationService';
import { Location } from '../types/location';
import { FiEdit2, FiTrash2, FiPlus, FiMapPin } from 'react-icons/fi';

const LocationsPage: React.FC = () => {
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingLocation, setEditingLocation] = useState<Location | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    coordinates: '',
    description: '',
  });

  useEffect(() => {
    fetchLocations();
  }, []);

  const fetchLocations = async () => {
    try {
      setLoading(true);
      const data = await locationService.getLocations();
      setLocations(data);
    } catch (error) {
      console.error('Error fetching locations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingLocation) {
        await locationService.updateLocation(editingLocation.id, formData);
      } else {
        await locationService.createLocation(formData);
      }
      setShowForm(false);
      setEditingLocation(null);
      setFormData({ name: '', address: '', coordinates: '', description: '' });
      fetchLocations();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error al guardar la ubicación');
    }
  };

  const handleEdit = (location: Location) => {
    setEditingLocation(location);
    setFormData({
      name: location.name,
      address: location.address,
      coordinates: location.coordinates,
      description: location.description,
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar esta ubicación?')) {
      return;
    }

    try {
      await locationService.deleteLocation(id);
      fetchLocations();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error al eliminar la ubicación');
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingLocation(null);
    setFormData({ name: '', address: '', coordinates: '', description: '' });
  };

  return (
    <MainLayout>
      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Gestión de Ubicaciones</h1>
              <p className="text-sm text-gray-600 mt-1">
                Administrar ubicaciones físicas de activos (Solo Administradores)
              </p>
            </div>
            {!showForm && (
              <button
                onClick={() => setShowForm(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center space-x-2"
              >
                <FiPlus />
                <span>Nueva Ubicación</span>
              </button>
            )}
          </div>
        </div>

        {/* Form */}
        {showForm && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">
              {editingLocation ? 'Editar Ubicación' : 'Nueva Ubicación'}
            </h2>
            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Coordenadas (Lat,Long)
                  </label>
                  <input
                    type="text"
                    value={formData.coordinates}
                    onChange={(e) => setFormData({ ...formData, coordinates: e.target.value })}
                    placeholder="-33.4489, -70.6693"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Dirección
                  </label>
                  <textarea
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                    rows={2}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Descripción
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {editingLocation ? 'Actualizar' : 'Crear'}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Locations List */}
        {loading ? (
          <div className="flex justify-center items-center p-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : locations.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <FiMapPin className="mx-auto text-6xl text-gray-400 mb-4" />
            <p className="text-gray-500 text-lg">No hay ubicaciones registradas</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {locations.map((location) => (
              <div key={location.id} className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <FiMapPin className="text-2xl text-blue-600" />
                      <h3 className="text-lg font-semibold text-gray-900">{location.name}</h3>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(location)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        <FiEdit2 />
                      </button>
                      {location.asset_count === 0 && (
                        <button
                          onClick={() => handleDelete(location.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <FiTrash2 />
                        </button>
                      )}
                    </div>
                  </div>
                  {location.address && (
                    <p className="text-sm text-gray-600 mb-2">📍 {location.address}</p>
                  )}
                  {location.coordinates && (
                    <p className="text-sm text-gray-500 mb-2">🌐 {location.coordinates}</p>
                  )}
                  {location.description && (
                    <p className="text-sm text-gray-700 mb-3">{location.description}</p>
                  )}
                  <div className="pt-3 border-t border-gray-200">
                    <span className="text-sm text-gray-600">
                      {location.asset_count} {location.asset_count === 1 ? 'activo' : 'activos'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default LocationsPage;
