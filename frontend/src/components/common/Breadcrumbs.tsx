/**
 * Breadcrumbs navigation component
 */
import { Link, useLocation } from 'react-router-dom';
import { FiHome, FiChevronRight } from 'react-icons/fi';

interface BreadcrumbItem {
  label: string;
  path: string;
}

const routeLabels: Record<string, string> = {
  dashboard: 'Dashboard',
  assets: 'Activos',
  'work-orders': 'Órdenes de Trabajo',
  maintenance: 'Mantenimiento',
  inventory: 'Inventario',
  checklists: 'Checklists',
  'machine-status': 'Estado de Máquinas',
  'ml-predictions': 'Predicciones ML',
  'celery-monitor': 'Monitor Celery',
  notifications: 'Notificaciones',
  reports: 'Reportes',
  locations: 'Ubicaciones',
  users: 'Usuarios',
  configuration: 'Configuración',
  new: 'Nuevo',
  edit: 'Editar',
};

export default function Breadcrumbs() {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  if (pathnames.length === 0 || pathnames[0] === 'dashboard') {
    return null; // Don't show breadcrumbs on dashboard
  }

  const breadcrumbs: BreadcrumbItem[] = [
    { label: 'Inicio', path: '/dashboard' },
  ];

  let currentPath = '';
  pathnames.forEach((segment) => {
    currentPath += `/${segment}`;
    const label = routeLabels[segment] || segment;
    breadcrumbs.push({ label, path: currentPath });
  });

  return (
    <nav className="flex items-center space-x-2 text-sm text-gray-600 mb-4">
      <Link
        to="/dashboard"
        className="flex items-center hover:text-blue-600 transition-colors"
      >
        <FiHome className="w-4 h-4" />
      </Link>

      {breadcrumbs.slice(1).map((breadcrumb, index) => {
        const isLast = index === breadcrumbs.length - 2;
        return (
          <div key={breadcrumb.path} className="flex items-center space-x-2">
            <FiChevronRight className="w-4 h-4 text-gray-400" />
            {isLast ? (
              <span className="font-medium text-gray-900">{breadcrumb.label}</span>
            ) : (
              <Link
                to={breadcrumb.path}
                className="hover:text-blue-600 transition-colors"
              >
                {breadcrumb.label}
              </Link>
            )}
          </div>
        );
      })}
    </nav>
  );
}
