"""Comprehensive API integration test with unique slugs."""
import requests
import uuid

BASE = 'http://localhost:8000/api/v1'
UNIQ = uuid.uuid4().hex[:8]

# 1. Root
r = requests.get('http://localhost:8000/')
assert r.status_code == 200, f'Root failed: {r.status_code}'
print(f'1. ROOT: {r.json()}')

# 2. Register duplicate
email = f'dup-{UNIQ}@test.pl'
r = requests.post(f'{BASE}/auth/register', json={'email': email, 'password':'test123'})
assert r.status_code == 200, f'First register failed: {r.status_code}'
r = requests.post(f'{BASE}/auth/register', json={'email': email, 'password':'test123'})
assert r.status_code == 400, f'Duplicate register should be 400, got {r.status_code}'
print(f'2. REGISTER duplicate: {r.status_code} - {r.json()["detail"]}')

# 3. Login admin
r = requests.post(f'{BASE}/auth/login', json={'email':'admin@stitchcore.pl','password':'admin123'})
assert r.status_code == 200, f'Admin login failed: {r.status_code}'
admin_token = r.json()['access_token']
refresh_token = r.json()['refresh_token']
print(f'3. LOGIN admin: OK')

# 4. /me admin
r = requests.get(f'{BASE}/auth/me', headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200
assert r.json()['role'] == 'admin'
print(f'4. ME admin: role=admin, email={r.json()["email"]}')

# 5. Register customer
cust_email = f'test-{UNIQ}@test.pl'
r = requests.post(f'{BASE}/auth/register', json={'email': cust_email, 'password':'test123','first_name':'Test','last_name':'User'})
assert r.status_code == 200, f'Customer register failed: {r.status_code}'
print(f'5. REGISTER customer: OK ({cust_email})')

# 6. Login customer
r = requests.post(f'{BASE}/auth/login', json={'email': cust_email, 'password':'test123'})
assert r.status_code == 200, f'Customer login failed: {r.status_code}'
customer_token = r.json()['access_token']
print(f'6. LOGIN customer: OK')

# 7. /me customer
r = requests.get(f'{BASE}/auth/me', headers={'Authorization': f'Bearer {customer_token}'})
assert r.json()['role'] == 'customer'
print(f'7. ME customer: role=customer')

# 8. Refresh token
r = requests.post(f'{BASE}/auth/refresh', json={'refresh_token': refresh_token})
assert r.status_code == 200, f'Refresh should be 200, got {r.status_code}'
assert 'access_token' in r.json()
print(f'8. REFRESH token: OK')

# 9. Admin endpoint - no auth (expect 401)
r = requests.post(f'{BASE}/categories', json={'name':'TestCat','slug':f'test-cat-{UNIQ}'})
assert r.status_code == 401, f'Should be 401, got {r.status_code}'
print(f'9. CATEGORY no-auth: {r.status_code} (401 from HTTPBearer)')

# 10. Admin endpoint - customer token (expect 403)
r = requests.post(f'{BASE}/categories', json={'name':'TestCat','slug':f'test-cat-{UNIQ}'}, headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 403, f'Should be 403, got {r.status_code}'
print(f'10. CATEGORY customer: {r.status_code} (correct 403)')

# 11. Admin endpoint - admin token
r = requests.post(f'{BASE}/categories', json={'name':'TestCat','slug':f'test-cat-{UNIQ}'}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Should be 200, got {r.status_code} ({r.text[:200]})'
print(f'11. CATEGORY create: {r.status_code} - id={r.json()["id"]}')

# 12. List categories
r = requests.get(f'{BASE}/categories')
assert r.status_code == 200
print(f'12. CATEGORIES list: {r.status_code} - count={len(r.json())}')

# 13. Create product
r = requests.post(f'{BASE}/products', json={'name':'Test Product','slug':f'test-product-{UNIQ}','price':99.99}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Product creation failed: {r.status_code} {r.text[:300]}'
product_id = r.json()['id']
print(f'13. PRODUCT create: {r.status_code} - id={product_id}')

# 14. List products
r = requests.get(f'{BASE}/products')
assert r.status_code == 200
print(f'14. PRODUCTS list: {r.status_code} - count={r.json()["count"]}')

# 15. Get product by id
r = requests.get(f'{BASE}/products/{product_id}')
assert r.status_code == 200
print(f'15. PRODUCT get: {r.status_code} - name={r.json()["name"]}')

# 16. Create variant
r = requests.post(f'{BASE}/products/{product_id}/variants', json={'sku':f'TEST-{UNIQ}','size':'M','color':'Red'}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Variant creation failed: {r.status_code} {r.text[:200]}'
print(f'16. VARIANT create: {r.status_code} - id={r.json()["id"]}')

# 17. Inventory: create location
r = requests.post(f'{BASE}/inventory/locations', json={'code':f'A-01-{UNIQ}','zone':'A','aisle':'1','rack':'1','shelf':'1'}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Location creation failed: {r.status_code} {r.text[:200]}'
print(f'17. LOCATION create: {r.status_code} - id={r.json()["id"]}')

# 18. Inventory: adjust stock
r = requests.post(f'{BASE}/inventory/stock/adjust', json={'variant_id':1,'location_id':1,'quantity':100,'notes':'Initial stock'}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Stock adjust failed: {r.status_code} {r.text[:200]}'
print(f'18. STOCK adjust: {r.status_code}')

# 19. List stock
r = requests.get(f'{BASE}/inventory/stock', headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200
print(f'19. STOCK list: {r.status_code} - items={len(r.json())}')

# 20. Create order (as customer)
r = requests.post(f'{BASE}/orders', json={'items':[{'product_id':product_id,'variant_id':1,'product_name':'Test Product','variant_label':'M / Red','quantity':2,'unit_price':99.99}],'shipping_address':'Test Address 123','shipping_method':'courier'}, headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 200, f'Order creation failed: {r.status_code} {r.text[:300]}'
order_id = r.json()['id']
print(f'20. ORDER create: {r.status_code} - number={r.json()["order_number"]}')

# 21. Update order status (admin)
r = requests.patch(f'{BASE}/orders/{order_id}/status', json={'status':'confirmed'}, headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200, f'Status update failed: {r.status_code} {r.text[:200]}'
print(f'21. ORDER status: {r.status_code} - status={r.json()["status"]}')

# 22. Customer sees their order
r = requests.get(f'{BASE}/orders', headers={'Authorization': f'Bearer {customer_token}'})
assert r.status_code == 200
print(f'22. ORDERS (customer): {r.status_code} - count={r.json()["count"]}')

# 23. Admin sees all orders
r = requests.get(f'{BASE}/orders', headers={'Authorization': f'Bearer {admin_token}'})
assert r.status_code == 200
print(f'23. ORDERS (admin): {r.status_code} - count={r.json()["count"]}')

print()
print('=' * 50)
print('ALL 23 TESTS PASSED')
print('=' * 50)
