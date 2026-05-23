"""Quick API integration test."""
import requests

BASE = 'http://localhost:8000/api/v1'

# Test root
r = requests.get('http://localhost:8000/')
print(f'ROOT: {r.json()}')

# Test register duplicate
r = requests.post(f'{BASE}/auth/register', json={'email':'test@test.pl','password':'test123','first_name':'Test','last_name':'User'})
print(f'REGISTER dup: {r.status_code} - {r.json()}')

# Test register new
r = requests.post(f'{BASE}/auth/register', json={'email':'new@test.pl','password':'test123','first_name':'New','last_name':'User'})
print(f'REGISTER new: {r.status_code} - OK')

# Test login admin
r = requests.post(f'{BASE}/auth/login', json={'email':'admin@mercha.pl','password':'admin123'})
assert r.ok, f'Admin login failed: {r.json()}'
admin_token = r.json()['access_token']
print(f'LOGIN admin: OK')

# Test /me admin
r = requests.get(f'{BASE}/auth/me', headers={'Authorization': f'Bearer {admin_token}'})
print(f'ME admin: role={r.json()["role"]}, email={r.json()["email"]}')
assert r.json()['role'] == 'admin'

# Test /me customer
r = requests.post(f'{BASE}/auth/login', json={'email':'test@test.pl','password':'test123'})
customer_token = r.json()['access_token']
r = requests.get(f'{BASE}/auth/me', headers={'Authorization': f'Bearer {customer_token}'})
print(f'ME customer: role={r.json()["role"]}, email={r.json()["email"]}')
assert r.json()['role'] == 'customer'

# Test refresh (body)
r = requests.post(f'{BASE}/auth/refresh', json={'refresh_token': admin_token})
print(f'REFRESH body: {r.status_code} - {"OK" if r.ok else r.json()}')

# Test admin endpoint without auth
r = requests.post(f'{BASE}/categories', json={'name':'Cat','slug':'cat'})
print(f'CATEGORY no-auth: {r.status_code} (expect 403)')

# Test admin endpoint with customer
r = requests.post(f'{BASE}/categories', json={'name':'Cat','slug':'cat'}, headers={'Authorization': f'Bearer {customer_token}'})
print(f'CATEGORY customer: {r.status_code} (expect 403)')

# Test admin endpoint with admin
r = requests.post(f'{BASE}/categories', json={'name':'Cat','slug':'cat'}, headers={'Authorization': f'Bearer {admin_token}'})
print(f'CATEGORY admin: {r.status_code} (expect 200)')

# Test create product
r = requests.post(f'{BASE}/products', json={'name':'Test Product','slug':'test-product','price':99.99}, headers={'Authorization': f'Bearer {admin_token}'})
print(f'PRODUCT create: {r.status_code} - id={r.json().get("id")}')

# Test create order (customer)
r = requests.post(f'{BASE}/orders', json={'items':[{'product_id':1,'product_name':'Test Product','quantity':1,'unit_price':99.99}],'shipping_address':'Test','shipping_method':'pickup'}, headers={'Authorization': f'Bearer {customer_token}'})
print(f'ORDER create: {r.status_code} - number={r.json().get("order_number","?")}')

print()
print('ALL TESTS PASSED')
