import json
import random

rng = random.Random(42)

photos = []
pid = 1

# CLUSTER 1 (8 photos)
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
        "episodic_discriminators": {
            "companion": comp,
            "weather": weather,
            "clothing": cloth,
            "foreground_vibe": "Sand and waves"
        }
    })
    pid += 1

# CLUSTER 2 (8 photos)
for i in range(8):
    if i < 4: comp, weather, fg = "Rahul", "Raining outside", "Hot chocolate mug / Wooden table"
    else: comp, weather, fg = "Solo", "Sunny / Clear window", "Laptop / Notebook"
    
    photos.append({
        "photo_id": f"img_{pid:03d}",
        "cluster_name": "THE DHARAMSHALA CAFE / RAIN",
        "keyword_tags": ["cafe", "dharamshala", "coffee", "food"],
        "location_name": "Café Blue, Dharamshala",
        "primary_object": "Food / Coffee",
        "episodic_discriminators": {
            "companion": comp,
            "weather": weather,
            "clothing": "Winter jacket" if "Raining" in weather else "Hoodie",
            "foreground_vibe": fg
        }
    })
    pid += 1

# CLUSTER 3 (8 photos)
for i in range(8):
    if i < 4: comp, weather, fg = "Family", "Late Night", "Bright neon store signs"
    else: comp, weather, fg = "College Friends", "Evening / Foggy", "Dim street lamps / Foggy"
    
    photos.append({
        "photo_id": f"img_{pid:03d}",
        "cluster_name": "THE DELHI STREET FOOD NIGHT OUT",
        "keyword_tags": ["delhi", "street food", "night", "chandni chowk"],
        "location_name": "Chandni Chowk, Delhi",
        "primary_object": "Street Food",
        "episodic_discriminators": {
            "companion": comp,
            "weather": weather,
            "clothing": "Casual tee",
            "foreground_vibe": fg
        }
    })
    pid += 1

# 76 Background Generic Photos
locations = ["Connaught Place", "India Gate", "Lodhi Garden", "Triund Hill", "Chapora Fort"]
objects = ["Monument", "Trees", "Selfie", "Group picture", "Clouds"]
comps = ["Nikhil", "Rahul", "Sparsh", "Family", "College Friends", "Solo", "Ananya"]
weathers = ["Sunny", "Raining", "Overcast", "Foggy"]
cloths = ["Casual tee", "Winter jacket", "Hoodie", "Formal shirt"]
fgs = ["Pathway", "Grass", "Car window", "Restaurant table"]

for i in range(76):
    photos.append({
        "photo_id": f"img_{pid:03d}",
        "cluster_name": "GENERIC MEMORIES",
        "keyword_tags": ["generic", "trip", "hangout"],
        "location_name": rng.choice(locations),
        "primary_object": rng.choice(objects),
        "episodic_discriminators": {
            "companion": rng.choice(comps),
            "weather": rng.choice(weathers),
            "clothing": rng.choice(cloths),
            "foreground_vibe": rng.choice(fgs)
        }
    })
    pid += 1

with open("mock_data.py", "w", encoding="utf-8") as f:
    f.write("MOCK_PHOTOS_DATABASE = " + json.dumps(photos, indent=4) + "\\n")

print(f"Generated {len(photos)} photos in mock_data.py")
