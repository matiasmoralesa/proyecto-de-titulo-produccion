/**
 * Global search component
 */
import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiSearch, FiX, FiTruck, FiClipboard, FiPackage, FiTool, FiCheckSquare } from 'react-icons/fi';
import api from '../../services/api';

interface SearchResult {
  id: string;
  type: string;
  title: string;
  subtitle: string;
  status: string;
  url: string;
}

interface SearchResults {
  assets: SearchResult[];
  work_orders: SearchResult[];
  spare_parts: SearchResult[];
  maintenance_plans: SearchResult[];
  checklists: SearchResult[];
}

export default function GlobalSearch() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResults | null>(null);
  const [loading, setLoading] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
  const searchRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ctrl+K or Cmd+K to open search
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        setIsOpen(true);
        setTimeout(() => inputRef.current?.focus(), 100);
      }
      // Escape to close
      if (event.key === 'Escape') {
        setIsOpen(false);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    if (query.length < 2) {
      setResults(null);
      setTotalCount(0);
      return;
    }

    const delayDebounce = setTimeout(() => {
      performSearch();
    }, 300);

    return () => clearTimeout(delayDebounce);
  }, [query]);

  const performSearch = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/search/global/?q=${encodeURIComponent(query)}`);
      setResults(response.data.results);
      setTotalCount(response.data.total_count);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResultClick = (result: SearchResult) => {
    navigate(result.url);
    setIsOpen(false);
    setQuery('');
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'asset':
        return <FiTruck className="w-5 h-5 text-blue-500" />;
      case 'work_order':
        return <FiClipboard className="w-5 h-5 text-purple-500" />;
      case 'spare_part':
        return <FiPackage className="w-5 h-5 text-green-500" />;
      case 'maintenance_plan':
        return <FiTool className="w-5 h-5 text-orange-500" />;
      case 'checklist':
        return <FiCheckSquare className="w-5 h-5 text-indigo-500" />;
      default:
        return <FiSearch className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'OPERATIONAL':
      case 'in_stock':
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'MAINTENANCE':
      case 'Pendiente':
        return 'bg-yellow-100 text-yellow-800';
      case 'OUT_OF_SERVICE':
      case 'low_stock':
      case 'inactive':
        return 'bg-red-100 text-red-800';
      case 'En Progreso':
        return 'bg-blue-100 text-blue-800';
      case 'Completada':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const renderResults = () => {
    if (!results || totalCount === 0) {
      return (
        <div className="p-8 text-center text-gray-500">
          <FiSearch className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>No se encontraron resultados</p>
        </div>
      );
    }

    return (
      <div className="max-h-96 overflow-y-auto">
        {Object.entries(results).map(([category, items]) => {
          if (items.length === 0) return null;

          const categoryLabels: Record<string, string> = {
            assets: 'Activos',
            work_orders: 'Órdenes de Trabajo',
            spare_parts: 'Repuestos',
            maintenance_plans: 'Planes de Mantenimiento',
            checklists: 'Checklists',
          };

          return (
            <div key={category} className="mb-4">
              <h3 className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase bg-gray-50">
                {categoryLabels[category]}
              </h3>
              {items.map((result: SearchResult) => (
                <button
                  key={result.id}
                  onClick={() => handleResultClick(result)}
                  className="w-full px-4 py-3 flex items-center gap-3 hover:bg-gray-50 transition-colors text-left"
                >
                  {getIcon(result.type)}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {result.title}
                    </p>
                    <p className="text-xs text-gray-500 truncate">{result.subtitle}</p>
                  </div>
                  <span
                    className={`px-2 py-1 text-xs rounded-full ${getStatusColor(
                      result.status
                    )}`}
                  >
                    {result.status}
                  </span>
                </button>
              ))}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div ref={searchRef} className="relative">
      {/* Search Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-4 py-2 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
      >
        <FiSearch className="w-4 h-4" />
        <span>Buscar...</span>
        <kbd className="hidden sm:inline-block px-2 py-1 text-xs font-semibold text-gray-600 bg-white border border-gray-300 rounded">
          Ctrl+K
        </kbd>
      </button>

      {/* Search Modal */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div className="fixed inset-0 bg-black bg-opacity-50 z-40" />

          {/* Modal */}
          <div className="fixed inset-x-0 top-20 mx-auto max-w-2xl z-50 px-4">
            <div className="bg-white rounded-lg shadow-2xl overflow-hidden">
              {/* Search Input */}
              <div className="flex items-center gap-3 px-4 py-3 border-b">
                <FiSearch className="w-5 h-5 text-gray-400" />
                <input
                  ref={inputRef}
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Buscar activos, órdenes, repuestos..."
                  className="flex-1 outline-none text-gray-900 placeholder-gray-400"
                  autoFocus
                />
                {query && (
                  <button
                    onClick={() => setQuery('')}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <FiX className="w-5 h-5" />
                  </button>
                )}
                {loading && (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                )}
              </div>

              {/* Results */}
              {query.length >= 2 ? (
                renderResults()
              ) : (
                <div className="p-8 text-center text-gray-500">
                  <p>Escribe al menos 2 caracteres para buscar</p>
                </div>
              )}

              {/* Footer */}
              <div className="px-4 py-3 bg-gray-50 border-t text-xs text-gray-500 flex items-center justify-between">
                <span>
                  {totalCount > 0 && `${totalCount} resultado${totalCount !== 1 ? 's' : ''}`}
                </span>
                <div className="flex items-center gap-4">
                  <span className="flex items-center gap-1">
                    <kbd className="px-2 py-1 bg-white border border-gray-300 rounded">↑↓</kbd>
                    Navegar
                  </span>
                  <span className="flex items-center gap-1">
                    <kbd className="px-2 py-1 bg-white border border-gray-300 rounded">ESC</kbd>
                    Cerrar
                  </span>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
