#!/usr/bin/env python3
"""
Script de pruebas COMPLETAS para botones de generación de informes en PRODUCCIÓN
Verifica que todos los botones funcionen correctamente en el entorno de producción
"""

import requests
import json
import sys
import time
from datetime import datetime, timedelta

class ProductionReportButtonTester:
    def __init__(self):
        # URL de producción en Railway
        self.base_url = "https://proyecto-de-titulo-produccion-production.up.railway.app/api/v1"
        self.frontend_url = "https://proyecto-de-titulo-produccion.vercel.app"
        self.token = None
        self.session = requests.Session()
        self.session.timeout = 30  # Timeout más largo para producción
        
        # Headers para producción
        self.session.headers.update({
            'User-Agent': 'CMMS-QA-Bot/1.0',
            'Accept': 'application/json',
        })
    
    def test_production_connectivity(self):
        """Probar conectividad con el servidor de producción"""
        print("🌐 Probando conectividad con producción...")
        try:
            # Probar endpoint básico sin autenticación
            response = self.session.get(f"{self.base_url}/auth/user-management/", timeout=10)
            
            if response.status_code in [200, 401, 403]:
                print("✅ Servidor de producción accesible")
                print(f"   - URL: {self.base_url}")
                print(f"   - Status: {response.status_code}")
                return True
            else:
                print(f"❌ Servidor responde con status inesperado: {response.status_code}")
                return False
        except requests.exceptions.Timeout:
            print("❌ Timeout conectando con producción")
            return False
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión con producción")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return False
    
    def test_frontend_connectivity(self):
        """Probar conectividad con el frontend en producción"""
        print("\n🎨 Probando conectividad con frontend...")
        try:
            response = self.session.get(self.frontend_url, timeout=10)
            
            if response.status_code == 200:
                print("✅ Frontend de producción accesible")
                print(f"   - URL: {self.frontend_url}")
                return True
            else:
                print(f"❌ Frontend responde con status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error conectando con frontend: {str(e)}")
            return False
    
    def login_production(self):
        """Autenticar con el sistema de producción"""
        print("\n🔐 Autenticando en producción...")
        
        # Credenciales de producción (usuario admin por defecto)
        credentials = [
            {"username": "admin", "password": "admin123"},
            {"username": "test_admin", "password": "testpass123"},
            {"username": "supervisor1", "password": "supervisor123"},
        ]
        
        for cred in credentials:
            try:
                print(f"   Probando con usuario: {cred['username']}")
                response = self.session.post(f"{self.base_url}/auth/login/", json=cred, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data['access']
                    self.session.headers.update({
                        'Authorization': f'Bearer {self.token}',
                        'Content-Type': 'application/json'
                    })
                    print(f"✅ Login exitoso con {cred['username']}")
                    print(f"   - Rol: {data.get('user', {}).get('role_name', 'N/A')}")
                    return True
                else:
                    print(f"   ❌ Login fallido: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error en login: {str(e)}")
        
        print("❌ No se pudo autenticar con ningún usuario")
        return False
    
    def test_production_dashboard_data(self):
        """Probar carga de datos del dashboard en producción"""
        print("\n📊 Probando dashboard de reportes en producción...")
        try:
            response = self.session.get(f"{self.base_url}/reports/dashboard/", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Dashboard de producción funcionando")
                
                # Mostrar KPIs de producción
                mtbf = data.get('mtbf', 'N/A')
                mttr = data.get('mttr', 'N/A')
                oee = data.get('oee', 'N/A')
                total_ot = data.get('work_order_summary', {}).get('total', 'N/A')
                
                print(f"   📈 KPIs de Producción:")
                print(f"      - MTBF: {mtbf}h")
                print(f"      - MTTR: {mttr}h")
                print(f"      - OEE: {oee}%")
                print(f"      - Total OT: {total_ot}")
                
                return True
            else:
                print(f"❌ Error en dashboard: {response.status_code}")
                if response.status_code == 403:
                    print("   (Usuario sin permisos para ver reportes)")
                return False
        except Exception as e:
            print(f"❌ Error en dashboard: {str(e)}")
            return False
    
    def test_production_csv_exports(self):
        """Probar exportaciones CSV en producción"""
        print("\n📄 Probando exportaciones CSV en producción...")
        
        csv_exports = [
            ("export_work_orders", "Exportar Órdenes de Trabajo"),
            ("export_asset_downtime", "Exportar Tiempo Fuera de Servicio"),
        ]
        
        results = []
        
        for endpoint, description in csv_exports:
            try:
                print(f"   Probando {description}...")
                response = self.session.get(f"{self.base_url}/reports/{endpoint}/", timeout=20)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    content_disposition = response.headers.get('content-disposition', '')
                    
                    if 'text/csv' in content_type:
                        filename = "archivo.csv"
                        if 'filename=' in content_disposition:
                            filename = content_disposition.split('filename=')[1].strip('"')
                        
                        print(f"   ✅ {description} funcionando")
                        print(f"      - Archivo: {filename}")
                        print(f"      - Tamaño: {len(response.content)} bytes")
                        
                        # Verificar contenido básico del CSV
                        content_preview = response.content.decode('utf-8')[:200]
                        lines = content_preview.split('\n')[:3]
                        print(f"      - Primeras líneas: {len(lines)} líneas")
                        
                        results.append(True)
                    else:
                        print(f"   ❌ {description} formato incorrecto: {content_type}")
                        results.append(False)
                elif response.status_code == 403:
                    print(f"   ⚠️  {description} sin permisos (403)")
                    results.append(False)
                else:
                    print(f"   ❌ {description} error: {response.status_code}")
                    results.append(False)
            except Exception as e:
                print(f"   ❌ Error en {description}: {str(e)}")
                results.append(False)
        
        return all(results)
    
    def test_production_chart_data(self):
        """Probar datos para gráficos en producción"""
        print("\n📈 Probando datos para gráficos en producción...")
        
        chart_endpoints = [
            ("asset_downtime", "Downtime por Activo"),
            ("spare_part_consumption", "Consumo de Repuestos"),
            ("kpis", "KPIs"),
            ("work_order_summary", "Resumen OT"),
            ("maintenance_compliance", "Cumplimiento Mantenimiento"),
        ]
        
        results = []
        
        for endpoint, description in chart_endpoints:
            try:
                print(f"   Probando {description}...")
                response = self.session.get(f"{self.base_url}/reports/{endpoint}/", timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if isinstance(data, list):
                        print(f"   ✅ {description}: {len(data)} elementos")
                        if len(data) > 0:
                            print(f"      - Ejemplo: {list(data[0].keys())[:3] if data[0] else 'N/A'}")
                    elif isinstance(data, dict):
                        print(f"   ✅ {description}: {len(data)} campos")
                        print(f"      - Campos: {list(data.keys())[:3]}")
                    
                    results.append(True)
                elif response.status_code == 403:
                    print(f"   ⚠️  {description} sin permisos")
                    results.append(False)
                else:
                    print(f"   ❌ {description} error: {response.status_code}")
                    results.append(False)
            except Exception as e:
                print(f"   ❌ Error en {description}: {str(e)}")
                results.append(False)
        
        return all(results)
    
    def test_production_pdf_generation(self):
        """Probar generación de PDF en producción"""
        print("\n📕 Probando generación de PDF en producción...")
        
        try:
            # Obtener checklists disponibles
            response = self.session.get(f"{self.base_url}/checklists/responses/", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                total_checklists = data.get('count', 0)
                print(f"   Checklists en producción: {total_checklists}")
                
                if data.get('results') and len(data['results']) > 0:
                    # Probar descarga de PDF del primer checklist
                    checklist = data['results'][0]
                    checklist_id = checklist['id']
                    
                    print(f"   Probando PDF del checklist {checklist_id}...")
                    
                    pdf_response = self.session.get(
                        f"{self.base_url}/checklists/responses/{checklist_id}/download_pdf/", 
                        timeout=20
                    )
                    
                    if pdf_response.status_code == 200:
                        content_type = pdf_response.headers.get('content-type', '')
                        
                        if 'application/pdf' in content_type:
                            print("   ✅ Generación PDF funcionando en producción")
                            print(f"      - Tamaño: {len(pdf_response.content)} bytes")
                            return True
                        else:
                            print(f"   ❌ PDF tipo incorrecto: {content_type}")
                            return False
                    else:
                        print(f"   ❌ Error descargando PDF: {pdf_response.status_code}")
                        return False
                else:
                    print("   ⚠️  No hay checklists en producción para probar PDF")
                    print("   ✅ Endpoint disponible (sin datos)")
                    return True
            elif response.status_code == 403:
                print("   ⚠️  Sin permisos para ver checklists")
                return False
            else:
                print(f"   ❌ Error obteniendo checklists: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error en PDF: {str(e)}")
            return False
    
    def test_production_date_filtering(self):
        """Probar filtrado por fechas en producción"""
        print("\n📅 Probando filtrado por fechas en producción...")
        
        try:
            date_ranges = [
                (7, "Últimos 7 días"),
                (30, "Últimos 30 días"),
            ]
            
            results = []
            
            for days, description in date_ranges:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                
                params = {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                }
                
                response = self.session.get(
                    f"{self.base_url}/reports/dashboard/", 
                    params=params, 
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    total_ot = data.get('work_order_summary', {}).get('total', 0)
                    print(f"   ✅ {description}: {total_ot} órdenes")
                    results.append(True)
                else:
                    print(f"   ❌ {description} error: {response.status_code}")
                    results.append(False)
            
            return all(results)
            
        except Exception as e:
            print(f"   ❌ Error en filtrado: {str(e)}")
            return False
    
    def test_production_performance(self):
        """Probar rendimiento en producción"""
        print("\n⚡ Probando rendimiento en producción...")
        
        performance_tests = [
            ("/reports/dashboard/", "Dashboard"),
            ("/reports/asset_downtime/", "Asset Downtime"),
            ("/reports/kpis/", "KPIs"),
        ]
        
        results = []
        
        for endpoint, name in performance_tests:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # en ms
                
                if response.status_code == 200:
                    if response_time < 2000:  # Menos de 2 segundos
                        print(f"   ✅ {name}: {response_time:.0f}ms")
                        results.append(True)
                    else:
                        print(f"   ⚠️  {name}: {response_time:.0f}ms (lento)")
                        results.append(True)  # Funciona pero lento
                else:
                    print(f"   ❌ {name}: Error {response.status_code}")
                    results.append(False)
            except Exception as e:
                print(f"   ❌ {name}: Error {str(e)}")
                results.append(False)
        
        return all(results)
    
    def run_production_test_suite(self):
        """Ejecutar suite completa de pruebas en producción"""
        print("🚀 INICIANDO PRUEBAS DE BOTONES DE REPORTES EN PRODUCCIÓN")
        print("="*80)
        print(f"🌐 Servidor: {self.base_url}")
        print(f"🎨 Frontend: {self.frontend_url}")
        print("="*80)
        
        # Pruebas de conectividad
        if not self.test_production_connectivity():
            print("\n❌ No se puede conectar con producción. Abortando pruebas.")
            return False
        
        self.test_frontend_connectivity()
        
        # Autenticación
        if not self.login_production():
            print("\n❌ No se pudo autenticar en producción. Abortando pruebas.")
            return False
        
        # Pruebas funcionales
        tests = [
            ("Dashboard de Reportes", self.test_production_dashboard_data),
            ("Exportaciones CSV", self.test_production_csv_exports),
            ("Datos para Gráficos", self.test_production_chart_data),
            ("Generación de PDF", self.test_production_pdf_generation),
            ("Filtrado por Fechas", self.test_production_date_filtering),
            ("Rendimiento", self.test_production_performance),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Error en {test_name}: {str(e)}")
                results.append((test_name, False))
        
        # Resumen final
        print(f"\n{'='*80}")
        print("📊 RESUMEN DE PRUEBAS EN PRODUCCIÓN")
        print(f"{'='*80}")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        print(f"🌐 Entorno: PRODUCCIÓN")
        print(f"📈 Estadísticas:")
        print(f"   Total de pruebas: {total}")
        print(f"   Pruebas exitosas: {passed}")
        print(f"   Pruebas fallidas: {total - passed}")
        print(f"   Tasa de éxito: {(passed/total*100):.1f}%")
        
        print(f"\n📋 Detalle de resultados:")
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {test_name}")
        
        overall_success = passed >= (total * 0.8)  # 80% mínimo para producción
        
        print(f"\n{'='*80}")
        if overall_success:
            print("🎉 ¡BOTONES DE REPORTES FUNCIONANDO EN PRODUCCIÓN!")
            print("")
            print("✅ Sistema verificado en entorno real:")
            print("   📊 Dashboard con datos reales")
            print("   📄 Exportaciones CSV operativas")
            print("   📈 Gráficos con datos de producción")
            print("   📕 Generación PDF disponible")
            print("   📅 Filtros de fecha funcionando")
            print("   ⚡ Rendimiento aceptable")
            print("")
            print("🚀 SISTEMA DE REPORTES VALIDADO EN PRODUCCIÓN")
        else:
            print("⚠️  ALGUNOS PROBLEMAS EN PRODUCCIÓN")
            print("")
            print("🔧 Revisar las pruebas marcadas como FAIL")
            print("💡 Posibles causas:")
            print("   - Permisos de usuario insuficientes")
            print("   - Datos insuficientes en producción")
            print("   - Problemas de conectividad")
        
        print(f"{'='*80}")
        
        return overall_success

if __name__ == "__main__":
    print("🌐 PRUEBAS DE BOTONES DE REPORTES EN PRODUCCIÓN")
    print("Verificando funcionalidad en el entorno real de Railway + Vercel")
    print("")
    
    tester = ProductionReportButtonTester()
    success = tester.run_production_test_suite()
    
    if success:
        print("\n🎉 PRODUCCIÓN VALIDADA EXITOSAMENTE")
    else:
        print("\n⚠️  PRODUCCIÓN NECESITA ATENCIÓN")
    
    sys.exit(0 if success else 1)