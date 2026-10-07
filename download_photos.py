import urllib.request
import time
import os
import csv

os.makedirs('assets/photos', exist_ok=True)

with open('assets/photo_manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    photos = list(reader)

req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for i, row in enumerate(photos):
    fid = row['id']
    url = f"https://picsum.photos/seed/{fid}/400/400"
    path = f"assets/photos/{fid}.jpg"
    
    if not os.path.exists(path):
        print(f"Downloading {fid}.jpg...")
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
                data = response.read()
                out_file.write(data)
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed to download {fid}: {e}")
print("Done!")
