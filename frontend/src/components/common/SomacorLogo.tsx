/**
 * SOMACOR Logo Component
 * Reusable logo component with fallback support
 */
import { FiTool } from 'react-icons/fi';

interface SomacorLogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showText?: boolean;
  showSubtext?: boolean;
  className?: string;
}

const sizeClasses = {
  sm: 'w-8 h-8',
  md: 'w-12 h-12',
  lg: 'w-16 h-16',
  xl: 'w-20 h-20'
};

const textSizeClasses = {
  sm: 'text-sm',
  md: 'text-lg',
  lg: 'text-xl',
  xl: 'text-2xl'
};

export default function SomacorLogo({ 
  size = 'md', 
  showText = true, 
  showSubtext = false,
  className = '' 
}: SomacorLogoProps) {
  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <div className="relative">
        <img 
          src="/logo-somacor.png" 
          alt="SOMACOR Logo" 
          className={`${sizeClasses[size]} rounded-full object-contain bg-white p-1 shadow-sm border border-gray-200`}
          onError={(e) => {
            // Fallback to icon if image fails to load
            e.currentTarget.style.display = 'none';
            const fallback = e.currentTarget.nextElementSibling as HTMLElement;
            if (fallback) {
              fallback.classList.remove('hidden');
            }
          }}
        />
        <div className={`${sizeClasses[size]} bg-white rounded-full flex items-center justify-center shadow-sm border border-gray-200 hidden`}>
          <FiTool className="w-1/2 h-1/2 text-primary-600" />
        </div>
      </div>
      
      {showText && (
        <div className="flex flex-col">
          <span className={`font-bold text-gray-900 dark:text-white ${textSizeClasses[size]}`}>
            CMMS
          </span>
          {showSubtext && (
            <span className="text-xs text-gray-500 dark:text-gray-400">
              SOMACOR
            </span>
          )}
        </div>
      )}
    </div>
  );
}