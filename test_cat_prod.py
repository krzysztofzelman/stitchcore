"""Test category and product creation."""
import requests, sys

BASE = 'http://localhost:8000/api/v1'

# Login admin
r = requests.post(f'{BASE}/auth/login', json={'email':'admin@stitchcore.pl','password':'admin123'})
token = r.json()['access_token']
print(f'Admin token: {token[:20]}...')

# Create category
r = requests.post(f'{BASE}/categories', json={'name':'Cat','slug':'cat'}, headers={'Authorization': f'Bearer {token}'})
print(f'CATEGORY: {r.status_code}')
print(f'  Response: {r.text[:300]}')

# Check if category exists
r = requests.get(f'{BASE}/categories')
print(f'CATEGORIES list: {r.status_code} - {r.text[:300]}')

# Create product
r = requests.post(f'{BASE}/products', json={'name':'Test','slug':'test','price':99.99}, headers={'Authorization': f'Bearer {token}'})
print(f'PRODUCT: {r.status_code}')
print(f'  Response: {r.text[:500]}')
