import json
import random
import re

rng = random.Random(42)

photos = []
pid = 1

# CLUSTER 1 (8 photos) Goa Beach Sunset
for i in range(8):
    if i < 3: comp, weather, cloth = "Nikhil", "Clear / Golden Hour", "Swim trunks"
    elif i < 6: comp, weather, cloth = "Sparsh", "Overcast / Hazy", "Casual tee"
    else: comp, weather, cloth = "Solo", "Dusk / Darkening", "Hoodie"
    
    photos.append({
        "photo_id": f"img_{pid:03d}",
        "cluster_name": "THE GOA BEACH SUNSET",
        "keyword_tags": ["sunset", "goa", "beach", "baga"],
        "location_name": "Baga Beach, Goa",
        "primary_object": "Sunset",
        "companion": comp,
        "weather_vibe": weather,
        "clothing_visuals": cloth,
        "foreground_vibe": "Sand and waves"
    })
    pid += 1

# CLUSTER 2 (8 photos) Dharamshala Cafe
for i in range(8):
    if i < 4: comp, weather, fg = "Rahul", "Raining outside", "Hot chocolate mug / Wooden table"
    else: comp, weather, fg = "Solo", "Sunny / Clear window", "Laptop / Notebook"
    
    photos.append({
        "photo_id": f"img_{pid:03d}",
        "cluster_name": "THE DHARAMSHALA CAFE / RAIN",
        "keyword_tags": ["cafe", "dharamshala", "coffee", "food"],
        "location_name": "Café Blue, Dharamshala",
        "primary_object": "Food / Coffee",
        "companion": comp,
        "weather_vibe": weather,
        "clothing_visuals": "Winter jacket" if "Raining" in weather else "Hoodie",
        "foreground_vibe": fg
    })
    pid += 1

# CLUSTER 3 (8 photos) Delhi Street Food
for i in range(8):
    if i < 4: comp, weather, fg = "Family", "Late Night", "Bright neon store signs"
    else: comp, weather, fg = "College Friends", "Evening / Foggy", "Dim street lamps / Foggy"
    
    photos.append({
        "photo_id": f"img_{pid:03d}",
        "cluster_name": "THE DELHI STREET FOOD NIGHT OUT",
        "keyword_tags": ["delhi", "street food", "night", "chandni chowk"],
        "location_name": "Chandni Chowk, Delhi",
        "primary_object": "Street Food",
        "companion": comp,
        "weather_vibe": weather,
        "clothing_visuals": "Casual tee",
        "foreground_vibe": fg
    })
    pid += 1

# CLUSTER 4 (8 photos) Tiny Noticeable Differences - Snow Point
for i in range(8):
    if i < 2: comp, weather, obj, cloth = "Sparsh", "Sunny", "Sunglasses", "Red jacket with beanie"
    elif i < 4: comp, weather, obj, cloth = "Rahul", "Snowing heavy", "Snowboard", "Red jacket unzipped"
    elif i < 6: comp, weather, obj, cloth = "Solo", "Foggy", "Coffee cup", "Red jacket full zip"
    else: comp, weather, obj, cloth = "Nikhil", "Sunny", "Snowball", "Red jacket with scarf"
    
    photos.append({
        "photo_id": f"img_{pid:03d}",
        "cluster_name": "THE RED JACKET AT SNOW POINT",
        "keyword_tags": ["snow", "mountain", "red jacket"],
        "location_name": "Gulmarg Snow Point",
        "primary_object": obj,
        "companion": comp,
        "weather_vibe": weather,
        "clothing_visuals": cloth,
        "foreground_vibe": "Snowy ground"
    })
    pid += 1

# 92 Background Generic Photos
locations = ["Connaught Place", "India Gate", "Lodhi Garden", "Triund Hill", "Chapora Fort"]
objects = ["Monument", "Trees", "Selfie", "Group picture", "Clouds"]
comps = ["Nikhil", "Rahul", "Sparsh", "Family", "College Friends", "Solo", "Ananya"]
weathers = ["Sunny", "Raining", "Overcast", "Foggy"]
cloths = ["Casual tee", "Winter jacket", "Hoodie", "Formal shirt"]
fgs = ["Pathway", "Grass", "Car window", "Restaurant table"]

for i in range(92):
    photos.append({
        "photo_id": f"img_{pid:03d}",
        "cluster_name": "GENERIC MEMORIES",
        "keyword_tags": ["generic", "trip", "hangout"],
        "location_name": rng.choice(locations),
        "primary_object": rng.choice(objects),
        "companion": rng.choice(comps),
        "weather_vibe": rng.choice(weathers),
        "clothing_visuals": rng.choice(cloths),
        "foreground_vibe": rng.choice(fgs)
    })
    pid += 1

# Write JSON
with open("mock_photos.json", "w", encoding="utf-8") as f:
    json.dump(photos, f, indent=4)

# Patch app.py to dynamically load this JSON instead of having 2000 lines hardcoded
with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the giant get_mock_library function entirely
# We find everything from @st.cache_data to library = get_mock_library()
pattern = re.compile(r'@st\.cache_data\ndef get_mock_library\(\):.*?library = get_mock_library\(\)', re.DOTALL)

new_func = '''@st.cache_data
def get_mock_library():
    import json
    with open("mock_photos.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data:
        p["id"] = p["photo_id"]
        p["palette"] = "blue"
        p["companions"] = [p["companion"]] # map for UI compatibility
    return data

library = get_mock_library()'''

content = re.sub(pattern, new_func, content)

# Also ensure get_candidates sim_score uses correct attributes
sim_pattern = re.compile(r'def sim_score\(p\):.*?return \(score, p\["id"\]\)', re.DOTALL)
new_sim = '''def sim_score(p):
                score = 0
                if p.get("location_name") == anchor.get("location_name"): score += 2
                if p.get("weather_vibe") == anchor.get("weather_vibe"): score += 2
                if p.get("clothing_visuals") == anchor.get("clothing_visuals"): score += 1
                if p.get("companion") == anchor.get("companion"): score += 1
                return (score, p["id"])'''
content = re.sub(sim_pattern, new_sim, content)

# Fix unasked in agent_step
unasked_pattern = re.compile(r'unasked = \[.*?\]')
new_unasked = 'unasked = [a for a in ["location_name", "companion", "weather_vibe", "clothing_visuals", "primary_object", "foreground_vibe"] if a not in state.hints and a not in state.asked]'
content = re.sub(unasked_pattern, new_unasked, content)

# Fix filter_lib in get_candidates
filter_pattern = re.compile(r'def filter_lib.*?items\(\)\)\]', re.DOTALL)
new_filter = '''def filter_lib(lib, h):
        return [p for p in lib if all(p.get(k) == v or (isinstance(p.get(k), list) and v in p.get(k)) for k, v in h.items())]'''
content = re.sub(filter_pattern, new_filter, content)

# Fix drop_order
drop_pattern = re.compile(r'drop_order = \[.*?\]')
new_drop = 'drop_order = ["foreground_vibe", "clothing_visuals", "primary_object", "location_name", "weather_vibe", "companion"]'
content = re.sub(drop_pattern, new_drop, content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Dataset updated and app.py patched.")
