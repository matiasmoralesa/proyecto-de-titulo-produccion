from apps.ml_predictions.models import FailurePrediction
from apps.work_orders.models import WorkOrder

print("=== Estado de Predicciones ML ===\n")
print(f"Total predicciones: {FailurePrediction.objects.count()}")
print(f"Total órdenes de trabajo: {WorkOrder.objects.count()}")

print("\n=== Últimas Predicciones ===")
for p in FailurePrediction.objects.all().order_by('-prediction_date')[:10]:
    ot_status = "SI" if p.work_order_created else "NO"
    print(f"  {p.asset.name}: {p.risk_level} ({p.failure_probability:.1%}) - OT: {ot_status}")

print("\n=== Predicciones por Nivel de Riesgo ===")
for level in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
    count = FailurePrediction.objects.filter(risk_level=level).count()
    print(f"  {level}: {count}")

print("\n=== Órdenes de Trabajo Recientes ===")
for wo in WorkOrder.objects.all().order_by('-created_at')[:5]:
    print(f"  {wo.work_order_number}: {wo.asset.name} - {wo.status} - {wo.priority}")
