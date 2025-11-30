/**
 * 403 Unauthorized page
 */
import { useNavigate } from 'react-router-dom';
import { FiShield, FiHome, FiArrowLeft } from 'react-icons/fi';

export default function Unauthorized() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-red-100 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center">
        {/* 403 Illustration */}
        <div className="mb-8">
          <div className="inline-flex items-center justify-center w-32 h-32 bg-red-100 rounded-full mb-6">
            <FiShield className="w-16 h-16 text-red-600" />
          </div>
          <h1 className="text-6xl font-bold text-red-600 mb-4">403</h1>
          <div className="w-32 h-1 bg-red-600 mx-auto rounded-full"></div>
        </div>

        {/* Message */}
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Acceso No Autorizado
        </h2>
        <p className="text-lg text-gray-600 mb-8">
          No tienes permisos para acceder a esta página. Si crees que esto es un error,
          contacta al administrador del sistema.
        </p>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors shadow-md"
          >
            <FiArrowLeft className="w-5 h-5" />
            Volver Atrás
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors shadow-md"
          >
            <FiHome className="w-5 h-5" />
            Ir al Dashboard
          </button>
        </div>

        {/* Permission Info */}
        <div className="mt-12 p-6 bg-white rounded-lg shadow-md">
          <h3 className="font-semibold text-gray-900 mb-3">Información de Permisos</h3>
          <p className="text-sm text-gray-600 mb-4">
            Esta página requiere permisos especiales. Los diferentes roles tienen acceso a diferentes funcionalidades:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="p-3 bg-gray-50 rounded">
              <p className="font-semibold text-gray-900 mb-1">Operador</p>
              <p className="text-gray-600">Acceso básico a activos y órdenes asignadas</p>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <p className="font-semibold text-gray-900 mb-1">Supervisor</p>
              <p className="text-gray-600">Gestión de órdenes y reportes</p>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <p className="font-semibold text-gray-900 mb-1">Administrador</p>
              <p className="text-gray-600">Acceso completo al sistema</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
