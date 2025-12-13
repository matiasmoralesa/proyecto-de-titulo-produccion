/**
 * 404 Not Found page
 */
import { useNavigate } from 'react-router-dom';
import { FiHome, FiArrowLeft } from 'react-icons/fi';

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center">
        {/* 404 Illustration */}
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-blue-600 mb-4">404</h1>
          <div className="w-32 h-1 bg-blue-600 mx-auto rounded-full"></div>
        </div>

        {/* Message */}
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Página No Encontrada
        </h2>
        <p className="text-lg text-gray-600 mb-8">
          Lo sentimos, la página que estás buscando no existe o ha sido movida.
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
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md"
          >
            <FiHome className="w-5 h-5" />
            Ir al Dashboard
          </button>
        </div>

        {/* Additional Help */}
        <div className="mt-12 p-6 bg-white rounded-lg shadow-md">
          <h3 className="font-semibold text-gray-900 mb-3">¿Necesitas ayuda?</h3>
          <p className="text-sm text-gray-600 mb-4">
            Si crees que esto es un error, por favor contacta al administrador del sistema.
          </p>
          <div className="flex flex-wrap gap-4 justify-center text-sm">
            <a href="/dashboard" className="text-blue-600 hover:underline">
              Dashboard
            </a>
            <a href="/assets" className="text-blue-600 hover:underline">
              Activos
            </a>
            <a href="/work-orders" className="text-blue-600 hover:underline">
              Órdenes de Trabajo
            </a>
            <a href="/reports" className="text-blue-600 hover:underline">
              Reportes
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
