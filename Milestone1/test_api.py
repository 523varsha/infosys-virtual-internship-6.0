import urllib.request
import json
import uuid

email = f'user_{uuid.uuid4().hex[:6]}@example.com'

data = json.dumps({
    'name': 'Test User',
    'email': email,
    'password': 'testpassword',
    'role': 'citizen',
    'location': 'Seattle'
}).encode('utf-8')

print('1. Testing /register...')
req = urllib.request.Request('http://127.0.0.1:5000/register', data=data, headers={'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
    print('Status:', response.status)
    print('Response:', response.read().decode('utf-8').strip())
except Exception as e:
    print('Error:', getattr(e, 'read', lambda: getattr(e, 'msg', str(e)))())

print('\n2. Testing /login...')
login_data = json.dumps({
    'email': email,
    'password': 'testpassword'
}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:5000/login', data=login_data, headers={'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
    res_data = response.read().decode('utf-8')
    print('Status:', response.status)
    print('Response:', res_data.strip())
    token = json.loads(res_data)['token']
except Exception as e:
    print('Error:', getattr(e, 'read', lambda: getattr(e, 'msg', str(e)))())

print('\n3. Testing /profile (Session verification)...')
req = urllib.request.Request('http://127.0.0.1:5000/profile', headers={'Authorization': f'Bearer {token}'})
try:
    response = urllib.request.urlopen(req)
    print('Status:', response.status)
    print('Response:', response.read().decode('utf-8').strip())
except Exception as e:
    print('Error:', getattr(e, 'read', lambda: getattr(e, 'msg', str(e)))())
