import requests

def test_stream():
    url = "http://localhost:8000/api/chat"
    payload = {"message": "who are you", "history": []}
    headers = {"Content-Type": "application/json"}
    
    with requests.post(url, json=payload, headers=headers, stream=True) as r:
        for chunk in r.iter_lines():
            if chunk:
                print(chunk.decode('utf-8'))

if __name__ == "__main__":
    test_stream()
