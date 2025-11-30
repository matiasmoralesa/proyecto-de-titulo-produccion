# Performance Optimization Guide

## Backend Optimizations

### 1. Database Query Optimization

#### Implemented Optimizations:
- ✅ `select_related()` for foreign key relationships
- ✅ `prefetch_related()` for many-to-many and reverse foreign keys
- ✅ Query optimization utilities in `apps/core/query_optimization.py`
- ✅ Database indexes on frequently queried fields

#### Usage Example:
```python
from apps.core.query_optimization import QueryOptimizer

# Optimize Asset queryset
assets = QueryOptimizer.optimize_asset_queryset(Asset.objects.all())

# Optimize WorkOrder queryset
work_orders = QueryOptimizer.optimize_work_order_queryset(WorkOrder.objects.all())
```

#### Recommended Indexes:
Run the following SQL commands to add indexes (already included in migrations):
```sql
-- Assets
CREATE INDEX idx_assets_status ON assets_asset(status);
CREATE INDEX idx_assets_vehicle_type ON assets_asset(vehicle_type);
CREATE INDEX idx_assets_location ON assets_asset(location_id);

-- Work Orders
CREATE INDEX idx_wo_status ON work_orders_workorder(status);
CREATE INDEX idx_wo_priority ON work_orders_workorder(priority);
CREATE INDEX idx_wo_asset ON work_orders_workorder(asset_id);
```

### 2. Caching

#### Implemented:
- ✅ Django local memory cache
- ✅ Dashboard stats cached for 5 minutes
- ✅ Cache invalidation on data updates

#### Configuration:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cmms-cache',
    }
}
```

#### Usage:
```python
from django.core.cache import cache

# Get from cache
data = cache.get('key')

# Set cache (300 seconds = 5 minutes)
cache.set('key', data, 300)

# Delete from cache
cache.delete('key')
```

### 3. API Response Optimization

- ✅ Pagination (20 items per page)
- ✅ Field filtering in serializers
- ✅ Rate limiting (100 requests/minute per user)
- ✅ Gzip compression (Django middleware)

### 4. Database Connection Pooling

For production, consider using connection pooling:
```python
# settings/production.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

## Frontend Optimizations

### 1. Code Splitting

#### Implemented:
- ✅ Manual chunks for vendors and features
- ✅ Lazy loading for routes
- ✅ Dynamic imports for heavy components

#### Vite Configuration:
```typescript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        'react-vendor': ['react', 'react-dom', 'react-router-dom'],
        'ui-vendor': ['react-hot-toast', 'react-icons'],
      },
    },
  },
}
```

### 2. Bundle Size Optimization

- ✅ Tree shaking enabled
- ✅ Minification with Terser
- ✅ Console.log removal in production
- ✅ Chunk size warnings at 1000kb

### 3. Image Optimization

Recommendations:
- Use WebP format for images
- Implement lazy loading for images
- Use appropriate image sizes
- Consider using a CDN for static assets

### 4. Component Optimization

#### React Best Practices:
```typescript
// Use React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
  // Component logic
});

// Use useMemo for expensive calculations
const expensiveValue = useMemo(() => {
  return calculateExpensiveValue(data);
}, [data]);

// Use useCallback for event handlers
const handleClick = useCallback(() => {
  // Handler logic
}, [dependencies]);
```

### 5. Virtual Scrolling

For large lists (>100 items), implement virtual scrolling:
```bash
npm install react-window
```

```typescript
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={items.length}
  itemSize={50}
  width="100%"
>
  {Row}
</FixedSizeList>
```

## Performance Monitoring

### 1. Backend Monitoring

#### Query Logging:
```python
from apps.core.query_optimization import log_queries

@log_queries
def my_view(request):
    # View logic
    pass
```

#### Django Debug Toolbar (Development):
```bash
pip install django-debug-toolbar
```

### 2. Frontend Monitoring

#### Lighthouse Scores:
Run Lighthouse audits regularly:
```bash
npm run build
npx lighthouse http://localhost:5173 --view
```

#### Bundle Analysis:
```bash
npm run build
npx vite-bundle-visualizer
```

## Performance Benchmarks

### Target Metrics:

#### Backend:
- API response time: < 200ms (p95)
- Database queries per request: < 10
- Cache hit rate: > 80%

#### Frontend:
- First Contentful Paint (FCP): < 1.5s
- Largest Contentful Paint (LCP): < 2.5s
- Time to Interactive (TTI): < 3.5s
- Total Bundle Size: < 500kb (gzipped)

## Optimization Checklist

### Backend:
- [x] Database indexes on frequently queried fields
- [x] Query optimization with select_related/prefetch_related
- [x] Caching for expensive operations
- [x] Pagination for list endpoints
- [x] Rate limiting
- [ ] Database connection pooling (production)
- [ ] Redis cache (production)
- [ ] CDN for static files (production)

### Frontend:
- [x] Code splitting
- [x] Lazy loading for routes
- [x] Bundle size optimization
- [x] Minification and compression
- [ ] Image optimization
- [ ] Virtual scrolling for large lists
- [ ] Service worker for offline support
- [ ] Progressive Web App (PWA) features

## Production Recommendations

### 1. Use Redis for Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 2. Enable Gzip Compression
```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... other middleware
]
```

### 3. Use CDN for Static Files
- Configure Django to serve static files from CDN
- Use CloudFlare or similar CDN service

### 4. Database Optimization
- Regular VACUUM and ANALYZE (PostgreSQL)
- Monitor slow queries
- Add indexes based on query patterns

### 5. Frontend Optimization
- Enable HTTP/2
- Use service workers for caching
- Implement Progressive Web App features
- Use lazy loading for images

## Monitoring Tools

### Backend:
- Django Debug Toolbar (development)
- New Relic or DataDog (production)
- PostgreSQL pg_stat_statements

### Frontend:
- Lighthouse
- WebPageTest
- Chrome DevTools Performance tab
- Bundle analyzer

## Conclusion

These optimizations provide a solid foundation for performance. Continue monitoring and optimizing based on real-world usage patterns and metrics.
