"""Comprehensive API integration test with unique slugs and retry logic."""
import time
import requests
import uuid

BASE = 'http://localhost:8000/api/v1'
UNIQ = uuid.uuid4().hex[:8]


def wait_for_backend(url: str = "http://localhost:8000/", timeout: int = 60) -> None:
    """Poll the backend health endpoint until it responds 200 or timeout expires."""
    start = time.time()
    last_error = ""
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                elapsed = time.time() - start
                print(f"[OK] Backend ready after {elapsed:.1f}s")
                return
            last_error = f"HTTP {r.status_code}"
        except requests.ConnectionError as e:
            last_error = f"ConnectionError: {e}"
        except requests.Timeout as e:
            last_error = f"Timeout: {e}"
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"
        time.sleep(1)
    raise RuntimeError(
        f"Backend NOT ready after {timeout}s (last error: {last_error})\n"
        f"  URL: {url}\n"
        f"  Is the server running?"
    )


def req(method: str, url: str, **kwargs) -> requests.Response:
    """Make an HTTP request with up to 3 retries and 1s delay between attempts."""
    max_retries = 3
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.request(method, url, timeout=10, **kwargs)
            # 5xx errors are worth retrying (server-side)
            if r.status_code < 500:
                return r
            last_exc = f"HTTP {r.status_code}"
        except (requests.ConnectionError, requests.Timeout) as e:
            last_exc = f"{type(e).__name__}: {e}"
        except Exception as e:
            last_exc = f"{type(e).__name__}: {e}"
        if attempt < max_retries:
            time.sleep(1)
    raise RuntimeError(
        f"Request failed after {max_retries} attempts: {method} {url}\n"
        f"  Last error: {last_exc}\n"
        f"  kwargs: {kwargs}"
    )


# ═══════════════════════════════════════════════════
# Wait for backend before running any tests
# ═══════════════════════════════════════════════════
wait_for_backend()

# ═══════════════════════════════════════════════════
# 1. Root
# ═══════════════════════════════════════════════════
r = req('GET', 'http://localhost:8000/')
assert r.status_code == 200, f'[1] Root failed: {r.status_code} {r.text[:200]}'
print(f'1. ROOT: {r.json()}')

# ═══════════════════════════════════════════════════
# 2. Register duplicate
# ═══════════════════════════════════════════════════
email = f'dup-{UNIQ}@test.pl'
r = req('POST', f'{BASE}/auth/register', json={'email': email, 'password': 'test123'})
assert r.status_code == 200, f'[2a] First register failed: {r.status_code} {r.text[:200]}'
r = req('POST', f'{BASE}/auth/register', json={'email': email, 'password': 'test123'})
assert r.status_code == 400, f'[2b] Duplicate register should be 400, got {r.status_code}: {r.text[:200]}'
print(f'2. REGISTER duplicate: {r.status_code} - {r.json()["detail"]}')

# ═══════════════════════════════════════════════════
# 3. Login admin
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/auth/login', json={'email': 'admin@stitchcore.pl', 'password': 'admin123'})
assert r.status_code == 200, f'[3] Admin login failed: {r.status_code} {r.text[:300]}'
admin_token = r.json()['access_token']
refresh_token = r.json()['refresh_token']
print('3. LOGIN admin: OK')

# ═══════════════════════════════════════════════════
# 4. /me admin
# ═══════════════════════════════════════════════════
r = req('GET', f'{BASE}/auth/me', headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[4] /me admin failed: {r.status_code} {r.text[:200]}'
assert r.json()['role'] == 'admin', f'[4] Expected admin role, got {r.json()}'
print(f'4. ME admin: role=admin, email={r.json()["email"]}')

# ═══════════════════════════════════════════════════
# 5. Register customer
# ═══════════════════════════════════════════════════
cust_email = f'test-{UNIQ}@test.pl'
r = req('POST', f'{BASE}/auth/register', json={
    'email': cust_email, 'password': 'test123',
    'first_name': 'Test', 'last_name': 'User',
})
assert r.status_code == 200, f'[5] Customer register failed: {r.status_code} {r.text[:200]}'
print(f'5. REGISTER customer: OK ({cust_email})')

# ═══════════════════════════════════════════════════
# 6. Login customer
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/auth/login', json={'email': cust_email, 'password': 'test123'})
assert r.status_code == 200, f'[6] Customer login failed: {r.status_code} {r.text[:300]}'
customer_token = r.json()['access_token']
print('6. LOGIN customer: OK')

# ═══════════════════════════════════════════════════
# 7. /me customer
# ═══════════════════════════════════════════════════
r = req('GET', f'{BASE}/auth/me', headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 200, f'[7] /me customer failed: {r.status_code} {r.text[:200]}'
assert r.json()['role'] == 'customer', f'[7] Expected customer role, got {r.json()}'
print('7. ME customer: role=customer')

# ═══════════════════════════════════════════════════
# 8. Refresh token
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/auth/refresh', json={'refresh_token': refresh_token})
assert r.status_code == 200, f'[8] Refresh failed: {r.status_code} {r.text[:200]}'
assert 'access_token' in r.json(), f'[8] No access_token in response: {r.json()}'
print('8. REFRESH token: OK')

# ═══════════════════════════════════════════════════
# 9. Admin endpoint - no auth (expect 401)
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/categories', json={'name': 'TestCat', 'slug': f'test-cat-{UNIQ}'})
assert r.status_code == 401, f'[9] Should be 401, got {r.status_code}'
print(f'9. CATEGORY no-auth: {r.status_code} (401 from HTTPBearer)')

# ═══════════════════════════════════════════════════
# 10. Admin endpoint - customer token (expect 403)
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/categories', json={'name': 'TestCat', 'slug': f'test-cat-{UNIQ}'},
        headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 403, f'[10] Should be 403, got {r.status_code}'
print(f'10. CATEGORY customer: {r.status_code} (correct 403)')

# ═══════════════════════════════════════════════════
# 11. Admin endpoint - admin token
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/categories', json={'name': 'TestCat', 'slug': f'test-cat-{UNIQ}'},
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[11] Should be 200, got {r.status_code} ({r.text[:300]})'
print(f'11. CATEGORY create: {r.status_code} - id={r.json()["id"]}')

# ═══════════════════════════════════════════════════
# 12. List categories
# ═══════════════════════════════════════════════════
r = req('GET', f'{BASE}/categories')
assert r.status_code == 200, f'[12] List categories failed: {r.status_code} {r.text[:200]}'
print(f'12. CATEGORIES list: {r.status_code} - count={len(r.json())}')

# ═══════════════════════════════════════════════════
# 13. Create product
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/products', json={
    'name': 'Test Product', 'slug': f'test-product-{UNIQ}', 'price': 99.99,
}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[13] Product creation failed: {r.status_code} {r.text[:300]}'
product_id = r.json()['id']
print(f'13. PRODUCT create: {r.status_code} - id={product_id}')

# ═══════════════════════════════════════════════════
# 14. List products
# ═══════════════════════════════════════════════════
r = req('GET', f'{BASE}/products')
assert r.status_code == 200, f'[14] List products failed: {r.status_code}'
print(f'14. PRODUCTS list: {r.status_code} - count={r.json()["count"]}')

# ═══════════════════════════════════════════════════
# 15. Get product by id
# ═══════════════════════════════════════════════════
r = req('GET', f'{BASE}/products/{product_id}')
assert r.status_code == 200, f'[15] Get product failed: {r.status_code} {r.text[:200]}'
print(f'15. PRODUCT get: {r.status_code} - name={r.json()["name"]}')

# ═══════════════════════════════════════════════════
# 16. Create variant
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/products/{product_id}/variants', json={
    'sku': f'TEST-{UNIQ}', 'size': 'M', 'color': 'Red',
}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[16] Variant creation failed: {r.status_code} {r.text[:200]}'
print(f'16. VARIANT create: {r.status_code} - id={r.json()["id"]}')

# ═══════════════════════════════════════════════════
# 17. Inventory: create location
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/inventory/locations', json={
    'code': f'A-01-{UNIQ}', 'zone': 'A', 'aisle': '1', 'rack': '1', 'shelf': '1',
}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[17] Location creation failed: {r.status_code} {r.text[:200]}'
print(f'17. LOCATION create: {r.status_code} - id={r.json()["id"]}')

# ═══════════════════════════════════════════════════
# 18. Inventory: adjust stock
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/inventory/stock/adjust', json={
    'variant_id': 1, 'location_id': 1, 'quantity': 100, 'notes': 'Initial stock',
}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[18] Stock adjust failed: {r.status_code} {r.text[:200]}'
print(f'18. STOCK adjust: {r.status_code}')

# ═══════════════════════════════════════════════════
# 19. List stock
# ═══════════════════════════════════════════════════
r = req('GET', f'{BASE}/inventory/stock', headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[19] List stock failed: {r.status_code}'
print(f'19. STOCK list: {r.status_code} - items={len(r.json())}')

# ═══════════════════════════════════════════════════
# 20. Create order (as customer)
# ═══════════════════════════════════════════════════
r = req('POST', f'{BASE}/orders', json={
    'items': [{
        'product_id': product_id, 'variant_id': 1,
        'product_name': 'Test Product', 'variant_label': 'M / Red',
        'quantity': 2, 'unit_price': 99.99,
    }],
    'shipping_address': 'Test Address 123',
    'shipping_method': 'courier',
}, headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 200, f'[20] Order creation failed: {r.status_code} {r.text[:300]}'
order_id = r.json()['id']
print(f'20. ORDER create: {r.status_code} - number={r.json()["order_number"]}')

# ═══════════════════════════════════════════════════
# 21. Update order status (admin)
# ═══════════════════════════════════════════════════
r = req('PATCH', f'{BASE}/orders/{order_id}/status', json={'status': 'confirmed'},
        headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[21] Status update failed: {r.status_code} {r.text[:200]}'
print(f'21. ORDER status: {r.status_code} - status={r.json()["status"]}')

# ═══════════════════════════════════════════════════
# 22. Customer sees their order
# ═══════════════════════════════════════════════════
r = req('GET', f'{BASE}/orders', headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 200, f'[22] Customer orders failed: {r.status_code}'
print(f'22. ORDERS (customer): {r.status_code} - count={r.json()["count"]}')

# ═══════════════════════════════════════════════════
# 23. Admin sees all orders
# ═══════════════════════════════════════════════════
r = req('GET', f'{BASE}/orders', headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'[23] Admin orders failed: {r.status_code}'
print(f'23. ORDERS (admin): {r.status_code} - count={r.json()["count"]}')

# ═══════════════════════════════════════════════════
# Done
# ═══════════════════════════════════════════════════
print()
print('=' * 50)
print('ALL 23 TESTS PASSED')
print('=' * 50)
