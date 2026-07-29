import requests
import json

url = "http://localhost:8000/api/chat"
payload = {
    "message": "Loop Engineering",
    "history": [],
    "model": "meta/llama-3.3-70b-instruct"
}

print("=== Testing Live Backend Stream for 'Loop Engineering' ===")
try:
    response = requests.post(url, json=payload, stream=True, timeout=10)
    full_text = ""
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if line_str.startswith("data: "):
                data_json = line_str[6:]
                try:
                    data = json.loads(data_json)
                    if "token" in data:
                        full_text += data["token"]
                except:
                    pass
    print("\n--- Streamed Response Content ---")
    print(full_text)
    
    # Check for forbidden temple strings
    forbidden = ["Sacred darshan", "Evening Aarti", "Opening & Closing Timings", "Visitor Guide"]
    found = [f for f in forbidden if f.lower() in full_text.lower()]
    if found:
        print(f"\n❌ FAIL: Found forbidden temple strings: {found}")
    else:
        print("\n✅ SUCCESS: 0% Temple text in streamed response!")
except Exception as e:
    print(f"Backend offline or unreachable: {e}")
