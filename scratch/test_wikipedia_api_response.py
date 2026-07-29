import urllib.request
import urllib.parse
import json

url = "https://en.wikipedia.org/w/api.php?action=query&titles=Tirupati&prop=pageimages|extracts&piprop=original|thumbnail&pithumbsize=1200&exintro=1&explaintext=1&format=json"

req = urllib.request.Request(url, headers={"User-Agent": "PrismAI/1.0"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    print(json.dumps(data, indent=2))
