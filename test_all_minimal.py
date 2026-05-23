"""Minimal API smoke test — only the most critical endpoints."""
import time
import requests
import uuid

BASE = 'http://localhost:8000/api/v1'
UNIQ = uuid.uuid4().hex[:8]


def req(method: str, url: str, **kwargs) -> requests.Response:
    """Request with retry (3 attempts, 2s delay)."""
    last = None
    for attempt in range(1, 4):
        try:
            r = requests.request(method, url, timeout=15, **kwargs)
            if r.status_code < 500:
                return r
            last = f"HTTP {r.status_code}"
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        if attempt < 3:
            time.sleep(2)
    raise RuntimeError(f"Failed after 3 retries: {method} {url} — {last}")


def wait_for_backend(timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get("http://localhost:8000/", timeout=5)
            if r.status_code == 200:
                print(f"Backend ready after {time.time()-start:.1f}s")
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Backend NOT ready")


wait_for_backend()

# 1. Root
assert req('GET', 'http://localhost:8000/').status_code == 200
print('1. ROOT: OK')

# 2. Register + login admin
r = req('POST', f'{BASE}/auth/login',
        json={'email': 'admin@mercha.pl', 'password': 'admin123'})
assert r.status_code == 200, f'Admin login: {r.status_code} {r.text[:200]}'
admin_token = r.json()['access_token']
refresh_token = r.json()['refresh_token']
print('2. LOGIN admin: OK')

# 3. /me admin
r = req('GET', f'{BASE}/auth/me',
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200 and r.json()['role'] == 'admin'
print('3. /ME admin: OK')

# 4. Register customer
cust = f'cust-{UNIQ}@test.pl'
r = req('POST', f'{BASE}/auth/register',
        json={'email': cust, 'password': 'test123'})
assert r.status_code == 200, f'Register: {r.status_code} {r.text[:200]}'
print('4. REGISTER customer: OK')

# 5. Login customer
r = req('POST', f'{BASE}/auth/login',
        json={'email': cust, 'password': 'test123'})
assert r.status_code == 200, f'Cust login: {r.status_code} {r.text[:200]}'
customer_token = r.json()['access_token']
print('5. LOGIN customer: OK')

# 6. Refresh token
r = req('POST', f'{BASE}/auth/refresh',
        json={'refresh_token': refresh_token})
assert r.status_code == 200 and 'access_token' in r.json()
print('6. REFRESH: OK')

# 7. Create category (admin)
r = req('POST', f'{BASE}/categories',
        json={'name': f'Cat-{UNIQ}', 'slug': f'cat-{UNIQ}'},
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Category: {r.status_code} {r.text[:200]}'
print('7. CATEGORY create: OK')

# 8. Create product (admin)
r = req('POST', f'{BASE}/products',
        json={'name': f'Prod-{UNIQ}', 'slug': f'prod-{UNIQ}', 'price': 49.99},
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Product: {r.status_code} {r.text[:200]}'
pid = r.json()['id']
print(f'8. PRODUCT create: OK (id={pid})')

# 9. Customer cannot create products (403)
r = req('POST', f'{BASE}/products',
        json={'name': 'X', 'slug': 'x', 'price': 10},
        headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 403, f'Expected 403, got {r.status_code}'
print('9. PRODUCT auth (customer→403): OK')

# 10. Create variant (admin)
r = req('POST', f'{BASE}/products/{pid}/variants',
        json={'sku': f'SKU-{UNIQ}', 'size': 'L', 'color': 'Blue'},
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Variant: {r.status_code} {r.text[:200]}'
print('10. VARIANT create: OK')

# 11. Create location (admin)
r = req('POST', f'{BASE}/inventory/locations',
        json={'code': f'LOC-{UNIQ}'},
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Location: {r.status_code} {r.text[:200]}'
print('11. LOCATION create: OK')

# 12. Adjust stock (admin)
r = req('POST', f'{BASE}/inventory/stock/adjust',
        json={'variant_id': 1, 'location_id': 1, 'quantity': 50},
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Stock: {r.status_code} {r.text[:200]}'
print('12. STOCK adjust: OK')

# 13. Create order (customer)
r = req('POST', f'{BASE}/orders',
        json={'items': [{'product_id': pid, 'variant_id': 1,
                         'product_name': 'Test', 'variant_label': 'L / Blue',
                         'quantity': 1, 'unit_price': 49.99}],
              'shipping_address': 'Test 123'},
        headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 200, f'Order: {r.status_code} {r.text[:300]}'
oid = r.json()['id']
print(f'13. ORDER create: OK (order={r.json()["order_number"]})')

# 14. Update order status (admin)
r = req('PATCH', f'{BASE}/orders/{oid}/status',
        json={'status': 'confirmed'},
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200
print('14. ORDER status update: OK')

# 15. Customer sees orders
r = req('GET', f'{BASE}/orders',
        headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 200
print(f'15. ORDERS (customer): count={r.json()["count"]}')

# 16. Admin sees all orders
r = req('GET', f'{BASE}/orders',
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200
print(f'16. ORDERS (admin): count={r.json()["count"]}')

print()
print('=' * 50)
print('ALL 16 MINIMAL TESTS PASSED')
print('=' * 50)
