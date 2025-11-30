from apps.authentication.models import User

users = User.objects.filter(is_active=True)[:10]
print('\nUsuarios activos:')
for u in users:
    role_name = u.role.name if u.role else 'Sin rol'
    full_name = u.get_full_name() or 'Sin nombre'
    print(f'  - {u.username} ({full_name}) - {role_name}')
