import urllib.request
import json
import time

def test():
    print("Testing /api/chat...")
    data = json.dumps({'message': 'hello', 'session_id': '123'}).encode('utf-8')
    req = urllib.request.Request('http://localhost:8000/api/chat', data=data, headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req)
        print("Status:", response.status)
        for line in response:
            print("CHUNK:", line.decode('utf-8').strip())
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    test()
