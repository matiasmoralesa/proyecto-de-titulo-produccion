/**
 * Forbidden (403) Page
 * 
 * Shown when user tries to access a resource they don't have permission for.
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldExclamationIcon } from '@heroicons/react/24/outline';

export const ForbiddenPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center">
        <ShieldExclamationIcon className="mx-auto h-24 w-24 text-red-500" />
        
        <h1 className="mt-6 text-6xl font-bold text-gray-900">403</h1>
        
        <h2 className="mt-4 text-3xl font-bold text-gray-900">
          Acceso Denegado
        </h2>
        
        <p className="mt-4 text-lg text-gray-600">
          No tiene permisos para acceder a este recurso.
        </p>
        
        <p className="mt-2 text-sm text-gray-500">
          Si cree que esto es un error, contacte a su administrador.
        </p>
        
        <div className="mt-8 flex gap-4 justify-center">
          <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Volver
          </button>
          
          <button
            onClick={() => navigate('/')}
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Ir al Inicio
          </button>
        </div>
      </div>
    </div>
  );
};
