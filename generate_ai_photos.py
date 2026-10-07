import urllib.request
import urllib.parse
import time
import os
import json
import subprocess

prompts = [
{"id": "mtn_01", "prompt": "Candid smartphone photo of a young man wearing a plain black t-shirt, alone, on a hiking trail in the Himalayas, carrying a backpack, bright sunny weather, afternoon light."}, 
{"id": "mtn_02", "prompt": "Candid smartphone photo of a young woman wearing a plain pink t-shirt, next to one friend, on a hiking trail in the Himalayas, carrying a backpack, bright sunny weather, soft morning light."}, 
{"id": "mtn_03", "prompt": "Candid smartphone photo of a young man wearing a plain blue t-shirt, with three friends, on a hiking trail in the Himalayas, overcast sky, afternoon light."}, 
{"id": "mtn_04", "prompt": "Candid smartphone photo of a young woman wearing a plain white t-shirt, alone, on a hiking trail in the Himalayas, thick fog, soft morning light."}, 
{"id": "mtn_05", "prompt": "Candid smartphone photo of a young man wearing a plain red t-shirt, next to one friend, on a hiking trail in the Himalayas, wearing a cap, overcast sky, afternoon light."}, 
{"id": "mtn_06", "prompt": "Candid smartphone photo of a young woman wearing a plain black t-shirt, with three friends, on a hiking trail in the Himalayas, wearing a cap, bright sunny weather, afternoon light."}, 
{"id": "mtn_07", "prompt": "Candid smartphone photo of a young man wearing a plain green t-shirt, alone, on a hiking trail in the Himalayas, carrying a backpack, bright sunny weather, golden sunset light."}, 
{"id": "mtn_08", "prompt": "Candid smartphone photo of a young woman wearing a plain yellow t-shirt, next to one friend, on a hiking trail in the Himalayas, thick fog, soft morning light."}, 
{"id": "bch_01", "prompt": "Candid smartphone photo of a young man wearing a plain white t-shirt, alone, standing on a sandy beach with the sea, wearing sunglasses, bright sunny weather, afternoon light."}, 
{"id": "bch_02", "prompt": "Candid smartphone photo of a young woman wearing a plain blue t-shirt, next to one friend, standing on a sandy beach with the sea, bright sunny weather, golden sunset light."}, 
{"id": "bch_03", "prompt": "Candid smartphone photo of a young man wearing a plain black t-shirt, with three friends, standing on a sandy beach with the sea, wearing a cap, bright sunny weather, afternoon light."}, 
{"id": "bch_04", "prompt": "Candid smartphone photo of a young woman wearing a plain pink t-shirt, alone, standing on a sandy beach with the sea, overcast sky, soft morning light."}, 
{"id": "bch_05", "prompt": "Candid smartphone photo of a young man wearing a plain yellow t-shirt, next to one friend, standing on a sandy beach with the sea, wearing sunglasses, bright sunny weather, afternoon light."}, 
{"id": "bch_06", "prompt": "Candid smartphone photo of a young woman wearing a plain red t-shirt, with three friends, standing on a sandy beach with the sea, overcast sky, golden sunset light."}, 
{"id": "bch_07", "prompt": "Candid smartphone photo of a young man wearing a plain green t-shirt, alone, standing on a sandy beach with the sea, wearing a cap, bright sunny weather, golden sunset light."}, 
{"id": "bch_08", "prompt": "Candid smartphone photo of a young woman wearing a plain grey t-shirt, next to one friend, standing on a sandy beach with the sea, wearing sunglasses, overcast sky, soft morning light."}, 
{"id": "caf_01", "prompt": "Candid smartphone photo of a young man wearing a plain black t-shirt, alone, sitting at a wooden table in a cozy cafe, with a cup of coffee, indoor lighting, soft morning light."}, 
{"id": "caf_02", "prompt": "Candid smartphone photo of a young woman wearing a plain pink t-shirt, next to one friend, sitting at a wooden table in a cozy cafe, with a dessert, indoor lighting, afternoon light."}, 
{"id": "caf_03", "prompt": "Candid smartphone photo of a young man wearing a plain blue t-shirt, with three friends, sitting at a wooden table in a cozy cafe, with a cup of coffee, indoor lighting, afternoon light."}, 
{"id": "caf_04", "prompt": "Candid smartphone photo of a young woman wearing a plain white t-shirt, alone, sitting at a wooden table in a cozy cafe, with a hot chocolate, light rain, afternoon light."}, 
{"id": "caf_05", "prompt": "Candid smartphone photo of a young man wearing a plain red t-shirt, next to one friend, sitting at a wooden table in a cozy cafe, with a cup of coffee, light rain, afternoon light."}, 
{"id": "caf_06", "prompt": "Candid smartphone photo of a young woman wearing a plain grey t-shirt, with three friends, sitting at a wooden table in a cozy cafe, with a cocktail, indoor lighting, night time."}, 
{"id": "caf_07", "prompt": "Candid smartphone photo of a young man wearing a plain green t-shirt, next to one friend, sitting at a wooden table in a cozy cafe, with a dessert, indoor lighting, night time."}, 
{"id": "caf_08", "prompt": "Candid smartphone photo of a young woman wearing a plain yellow t-shirt, alone, sitting at a wooden table in a cozy cafe, with a hot chocolate, light rain, soft morning light."}, 
{"id": "con_01", "prompt": "Candid smartphone photo of a young man wearing a plain black t-shirt, next to one friend, at a live music concert, purple stage lights, indoor lighting, night time."}, 
{"id": "con_02", "prompt": "Candid smartphone photo of a young woman wearing a plain black t-shirt, with three friends, at a live music concert, red stage lights, indoor lighting, night time."}, 
{"id": "con_03", "prompt": "Candid smartphone photo of a young man wearing a plain pink t-shirt, alone, at a live music concert, purple stage lights, indoor lighting, night time."}, 
{"id": "con_04", "prompt": "Candid smartphone photo of a young woman wearing a plain blue t-shirt, next to one friend, at a live music concert, red stage lights, indoor lighting, night time."}, 
{"id": "con_05", "prompt": "Candid smartphone photo of a young man wearing a plain white t-shirt, with three friends, at a live music concert, blue stage lights, indoor lighting, night time."}, 
{"id": "con_06", "prompt": "Candid smartphone photo of a young woman wearing a plain red t-shirt, alone, at a live music concert, blue stage lights, indoor lighting, night time."}, 
{"id": "con_07", "prompt": "Candid smartphone photo of a young man wearing a plain grey t-shirt, next to one friend, at a live music concert, blue stage lights, indoor lighting, night time."}, 
{"id": "con_08", "prompt": "Candid smartphone photo of a young woman wearing a plain green t-shirt, with three friends, at a live music concert, purple stage lights, indoor lighting, night time."}, 
{"id": "str_01", "prompt": "Candid smartphone photo of a young man wearing a plain black t-shirt, alone, on a busy city street, holding an umbrella, light rain, night time."}, 
{"id": "str_02", "prompt": "Candid smartphone photo of a young woman wearing a plain pink t-shirt, next to one friend, on a busy city street, with street food, light rain, night time."}, 
{"id": "str_03", "prompt": "Candid smartphone photo of a young man wearing a plain blue t-shirt, with three friends, on a busy city street, holding an umbrella, light rain, golden sunset light."}, 
{"id": "str_04", "prompt": "Candid smartphone photo of a young woman wearing a plain yellow t-shirt, alone, on a busy city street, light rain, golden sunset light."}, 
{"id": "str_05", "prompt": "Candid smartphone photo of a young man wearing a plain white t-shirt, next to one friend, on a busy city street, with street food, overcast sky, night time."}, 
{"id": "str_06", "prompt": "Candid smartphone photo of a young woman wearing a plain red t-shirt, with three friends, on a busy city street, light rain, night time."}, 
{"id": "str_07", "prompt": "Candid smartphone photo of a young man wearing a plain green t-shirt, alone, on a busy city street, with street food, overcast sky, golden sunset light."}, 
{"id": "str_08", "prompt": "Candid smartphone photo of a young woman wearing a plain grey t-shirt, next to one friend, on a busy city street, holding an umbrella, light rain, golden sunset light."}, 
{"id": "bal_01", "prompt": "Candid smartphone photo of a young man wearing a plain black t-shirt, alone, on a home balcony, the sky glowing orange, bright sunny weather, golden sunset light."}, 
{"id": "bal_02", "prompt": "Candid smartphone photo of a young woman wearing a plain pink t-shirt, next to one friend, on a home balcony, the sky glowing purple, overcast sky, golden sunset light."}, 
{"id": "bal_03", "prompt": "Candid smartphone photo of a young man wearing a plain blue t-shirt, alone, on a home balcony, the sky glowing pink, overcast sky, golden sunset light."}, 
{"id": "bal_04", "prompt": "Candid smartphone photo of a young woman wearing a plain white t-shirt, next to one friend, on a home balcony, the sky glowing purple, bright sunny weather, golden sunset light."}, 
{"id": "bal_05", "prompt": "Candid smartphone photo of a young man wearing a plain yellow t-shirt, alone, on a home balcony, the sky glowing orange, thick fog, golden sunset light."}, 
{"id": "bal_06", "prompt": "Candid smartphone photo of a young woman wearing a plain red t-shirt, next to one friend, on a home balcony, the sky glowing pink, bright sunny weather, golden sunset light."}, 
{"id": "bal_07", "prompt": "Candid smartphone photo of a young man wearing a plain green t-shirt, with three friends, on a home balcony, the sky glowing orange, overcast sky, golden sunset light."}, 
{"id": "bal_08", "prompt": "Candid smartphone photo of a young woman wearing a plain grey t-shirt, alone, on a home balcony, the sky glowing purple, bright sunny weather, golden sunset light."}
]

import random

UAS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'PostmanRuntime/7.28.4',
    'python-requests/2.26.0',
    'curl/7.68.0',
    'Wget/1.20.3'
]

os.makedirs('assets/photos', exist_ok=True)

for item in prompts:
    fid = item["id"]
    prompt = item["prompt"]
    full_prompt = prompt + " 4:3 aspect ratio, hyperrealistic photography."
    
    path = f"assets/photos/{fid}.jpg"
    
    print(f"Generating {fid}.jpg...", flush=True)
    if os.path.exists(path) and os.path.getsize(path) > 100000:
        print(f"Skipping {fid} (already exists, size: {os.path.getsize(path)})", flush=True)
        continue
        
    success = False
    for attempt in range(5):
        try:
            encoded_prompt = urllib.parse.quote(full_prompt)
            # Add random parameter to bypass cache/limits
            r_seed = random.randint(1000, 99999)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=480&height=480&nologo=true&seed={r_seed}&bypass={r_seed}"
            
            ua = random.choice(UAS)
            req = urllib.request.Request(url, headers={'User-Agent': ua})
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read()
                if len(data) > 50000:
                    with open(path, 'wb') as out_file:
                        out_file.write(data)
                    success = True
                    print(f"Success for {fid}!")
                    time.sleep(0.5) 
                    break
                else:
                    print(f"Returned data too small: {len(data)} bytes")
        except Exception as e:
            print(f"Attempt {attempt+1} failed to download {fid}: {e}", flush=True)
            time.sleep(1)
            
    if not success:
        print(f"FAILED permanently for {fid}")

print("Done generating 48 images!", flush=True)

# automatically add and commit
try:
    subprocess.run(["git", "add", "assets/photos/*.jpg"], check=True)
    subprocess.run(["git", "commit", "-m", "Generate actual images via pollinations API"], check=True)
    subprocess.run(["git", "push"], check=True)
except Exception as e:
    print(f"Git push failed: {e}", flush=True)
