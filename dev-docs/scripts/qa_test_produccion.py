"""
Script de QA automatizado para probar endpoints en producción
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple

# Configuración
BACKEND_URL = "https://proyecto-de-titulo-produccion-production.up.railway.app"
FRONTEND_URL = "https://somacor-cmms.vercel.app"

# Credenciales de prueba
TEST_CREDENTIALS = {
    "username": "admin",
    "password": "admin123"
}

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

class QATester:
    def __init__(self):
        self.token = None
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'tests': []
        }
    
    def print_header(self, text: str):
        """Imprime un encabezado"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    def print_test(self, name: str, passed: bool, message: str = ""):
        """Imprime resultado de un test"""
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"{status} - {name}")
        if message:
            print(f"      {message}")
        
        self.results['tests'].append({
            'name': name,
            'passed': passed,
            'message': message
        })
        
        if passed:
            self.results['passed'] += 1
        else:
            self.results['failed'] += 1
    
    def print_warning(self, message: str):
        """Imprime una advertencia"""
        print(f"{Colors.YELLOW}⚠ WARNING{Colors.END} - {message}")
        self.results['warnings'] += 1
    
    def test_frontend_availability(self) -> bool:
        """Prueba que el frontend esté disponible"""
        try:
            response = requests.get(FRONTEND_URL, timeout=10)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def test_backend_availability(self) -> bool:
        """Prueba que el backend esté disponible"""
        try:
            response = requests.get(f"{BACKEND_URL}/api/v1/", timeout=10)
            return response.status_code in [200, 404]  # 404 es OK, significa que está corriendo
        except Exception as e:
            return False
    
    def test_login(self) -> Tuple[bool, str]:
        """Prueba el login y obtiene token"""
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/auth/login/",
                json=TEST_CREDENTIALS,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access')
                return True, f"Token obtenido: {self.token[:20]}..."
            else:
                return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def get_headers(self) -> Dict:
        """Retorna headers con token"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def test_endpoint(self, name: str, endpoint: str, method: str = "GET", data: Dict = None) -> Tuple[bool, str]:
        """Prueba un endpoint genérico"""
        try:
            url = f"{BACKEND_URL}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, headers=self.get_headers(), timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.get_headers(), json=data, timeout=10)
            
            if response.status_code in [200, 201]:
                return True, f"Status: {response.status_code}"
            else:
                return False, f"Status: {response.status_code}, Response: {response.text[:100]}"
        except Exception as e:
            return False, str(e)
    
    def test_assets(self):
        """Prueba endpoints de activos"""
        self.print_header("PRUEBAS DE ACTIVOS")
        
        # Listar activos
        passed, msg = self.test_endpoint("Listar activos", "/api/v1/assets/")
        self.print_test("GET /api/v1/assets/", passed, msg)
        
        # Obtener primer activo
        try:
            response = requests.get(
                f"{BACKEND_URL}/api/v1/assets/",
                headers=self.get_headers(),
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('results') and len(data['results']) > 0:
                    asset_id = data['results'][0]['id']
                    passed, msg = self.test_endpoint(
                        "Obtener detalle de activo",
                        f"/api/v1/assets/{asset_id}/"
                    )
                    self.print_test(f"GET /api/v1/assets/{asset_id}/", passed, msg)
                else:
                    self.print_warning("No hay activos para probar detalle")
        except Exception as e:
            self.print_test("Obtener detalle de activo", False, str(e))
    
    def test_work_orders(self):
        """Prueba endpoints de órdenes de trabajo"""
        self.print_header("PRUEBAS DE ÓRDENES DE TRABAJO")
        
        # Listar órdenes
        passed, msg = self.test_endpoint("Listar órdenes de trabajo", "/api/v1/work-orders/")
        self.print_test("GET /api/v1/work-orders/", passed, msg)
        
        # Filtros
        passed, msg = self.test_endpoint(
            "Filtrar por estado",
            "/api/v1/work-orders/?status=Completada"
        )
        self.print_test("GET /api/v1/work-orders/?status=Completada", passed, msg)
        
        passed, msg = self.test_endpoint(
            "Filtrar por prioridad",
            "/api/v1/work-orders/?priority=Alta"
        )
        self.print_test("GET /api/v1/work-orders/?priority=Alta", passed, msg)
    
    def test_inventory(self):
        """Prueba endpoints de inventario"""
        self.print_header("PRUEBAS DE INVENTARIO")
        
        # Listar repuestos
        passed, msg = self.test_endpoint("Listar repuestos", "/api/v1/inventory/spare-parts/")
        self.print_test("GET /api/v1/inventory/spare-parts/", passed, msg)
        
        # Movimientos de stock
        passed, msg = self.test_endpoint("Listar movimientos", "/api/v1/inventory/stock-movements/")
        self.print_test("GET /api/v1/inventory/stock-movements/", passed, msg)
        
        # Alertas de stock bajo
        passed, msg = self.test_endpoint(
            "Alertas de stock bajo",
            "/api/v1/inventory/spare-parts/low-stock-alerts/"
        )
        self.print_test("GET /api/v1/inventory/spare-parts/low-stock-alerts/", passed, msg)
    
    def test_reports(self):
        """Prueba endpoints de reportes"""
        self.print_header("PRUEBAS DE REPORTES")
        
        # KPIs
        passed, msg = self.test_endpoint("KPIs", "/api/v1/reports/kpis/")
        self.print_test("GET /api/v1/reports/kpis/", passed, msg)
        
        # Resumen de órdenes
        passed, msg = self.test_endpoint(
            "Resumen de órdenes",
            "/api/v1/reports/work_order_summary/"
        )
        self.print_test("GET /api/v1/reports/work_order_summary/", passed, msg)
        
        # Downtime de activos
        passed, msg = self.test_endpoint(
            "Downtime de activos",
            "/api/v1/reports/asset_downtime/"
        )
        self.print_test("GET /api/v1/reports/asset_downtime/", passed, msg)
        
        # Consumo de repuestos
        passed, msg = self.test_endpoint(
            "Consumo de repuestos",
            "/api/v1/reports/spare_part_consumption/"
        )
        self.print_test("GET /api/v1/reports/spare_part_consumption/", passed, msg)
    
    def test_checklists(self):
        """Prueba endpoints de checklists"""
        self.print_header("PRUEBAS DE CHECKLISTS")
        
        # Plantillas
        passed, msg = self.test_endpoint(
            "Listar plantillas",
            "/api/v1/checklists/templates/"
        )
        self.print_test("GET /api/v1/checklists/templates/", passed, msg)
        
        # Checklists completados
        passed, msg = self.test_endpoint(
            "Listar checklists",
            "/api/v1/checklists/responses/"
        )
        self.print_test("GET /api/v1/checklists/responses/", passed, msg)
    
    def test_notifications(self):
        """Prueba endpoints de notificaciones"""
        self.print_header("PRUEBAS DE NOTIFICACIONES")
        
        # Listar notificaciones
        passed, msg = self.test_endpoint(
            "Listar notificaciones",
            "/api/v1/notifications/"
        )
        self.print_test("GET /api/v1/notifications/", passed, msg)
    
    def test_machine_status(self):
        """Prueba endpoints de estado de máquinas"""
        self.print_header("PRUEBAS DE ESTADO DE MÁQUINAS")
        
        # Listar estados
        passed, msg = self.test_endpoint(
            "Listar estados",
            "/api/v1/machine-status/"
        )
        self.print_test("GET /api/v1/machine-status/", passed, msg)
    
    def test_dashboard(self):
        """Prueba endpoint del dashboard"""
        self.print_header("PRUEBAS DE DASHBOARD")
        
        # Dashboard stats
        passed, msg = self.test_endpoint(
            "Estadísticas del dashboard",
            "/api/v1/dashboard/stats/"
        )
        self.print_test("GET /api/v1/dashboard/stats/", passed, msg)
        
        # Dashboard data from reports
        passed, msg = self.test_endpoint(
            "Datos del dashboard (reportes)",
            "/api/v1/reports/dashboard/"
        )
        self.print_test("GET /api/v1/reports/dashboard/", passed, msg)
    
    def print_summary(self):
        """Imprime resumen de resultados"""
        self.print_header("RESUMEN DE RESULTADOS")
        
        total = self.results['passed'] + self.results['failed']
        pass_rate = (self.results['passed'] / total * 100) if total > 0 else 0
        
        print(f"Total de pruebas: {total}")
        print(f"{Colors.GREEN}Exitosas: {self.results['passed']}{Colors.END}")
        print(f"{Colors.RED}Fallidas: {self.results['failed']}{Colors.END}")
        print(f"{Colors.YELLOW}Advertencias: {self.results['warnings']}{Colors.END}")
        print(f"\nTasa de éxito: {pass_rate:.1f}%")
        
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ TODAS LAS PRUEBAS PASARON{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ HAY PRUEBAS FALLIDAS{Colors.END}")
            print(f"\n{Colors.BOLD}Pruebas fallidas:{Colors.END}")
            for test in self.results['tests']:
                if not test['passed']:
                    print(f"  - {test['name']}: {test['message']}")
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}QA TESTING - PRODUCCIÓN{Colors.END}")
        print(f"{Colors.BOLD}Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        
        # Pruebas de disponibilidad
        self.print_header("PRUEBAS DE DISPONIBILIDAD")
        
        passed = self.test_frontend_availability()
        self.print_test("Frontend disponible", passed, FRONTEND_URL)
        
        passed = self.test_backend_availability()
        self.print_test("Backend disponible", passed, BACKEND_URL)
        
        # Login
        self.print_header("PRUEBAS DE AUTENTICACIÓN")
        passed, msg = self.test_login()
        self.print_test("Login con credenciales correctas", passed, msg)
        
        if not self.token:
            print(f"\n{Colors.RED}No se pudo obtener token. Abortando pruebas.{Colors.END}")
            return
        
        # Pruebas de endpoints
        self.test_dashboard()
        self.test_assets()
        self.test_work_orders()
        self.test_inventory()
        self.test_reports()
        self.test_checklists()
        self.test_notifications()
        self.test_machine_status()
        
        # Resumen
        self.print_summary()
        
        # Guardar resultados
        self.save_results()
    
    def save_results(self):
        """Guarda resultados en archivo JSON"""
        filename = f"qa_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'frontend_url': FRONTEND_URL,
                'backend_url': BACKEND_URL,
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n{Colors.BLUE}Resultados guardados en: {filename}{Colors.END}")

def main():
    """Función principal"""
    tester = QATester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
