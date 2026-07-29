import urllib.request

urls_to_test = [
    "https://upload.wikimedia.org/wikipedia/commons/4/4e/Tirumala_090615.jpg",
    "https://wsrv.nl/?url=upload.wikimedia.org/wikipedia/commons/4/4e/Tirumala_090615.jpg&w=1200&output=webp",
    "https://wsrv.nl/?url=https://upload.wikimedia.org/wikipedia/commons/4/4e/Tirumala_090615.jpg&w=1200&output=webp"
]

for url in urls_to_test:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"URL: {url[:60]}... => Status: {resp.status}, Content-Type: {resp.headers.get('Content-Type')}")
    except Exception as e:
        print(f"URL: {url[:60]}... => ERROR: {e}")
