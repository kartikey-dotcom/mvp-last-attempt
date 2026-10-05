import json
import random

categories = [
    ("sunsets", "Sunset", ["sunset", "beach", "evening", "sun"]),
    ("bridges", "Bridge", ["bridge", "water", "architecture", "river"]),
    ("work desks", "Desk", ["desk", "work", "laptop", "office", "coffee"]),
    ("forests", "Forest", ["forest", "trees", "nature", "woods", "hiking"]),
    ("wildlife like bears", "Animal", ["bear", "wildlife", "nature", "animal"]),
    ("ocean piers", "Pier", ["pier", "ocean", "water", "sea", "beach"]),
    ("vintage cars", "Car", ["car", "vintage", "classic", "vehicle"]),
    ("city streets", "City", ["city", "street", "urban", "downtown", "buildings"]),
    ("trains", "Train", ["train", "station", "railway", "travel"]),
    ("clocks", "Clock", ["clock", "time", "vintage", "wall"]),
    ("underwater jellyfish", "Jellyfish", ["underwater", "jellyfish", "ocean", "aquarium"]),
    ("architecture", "Building", ["architecture", "building", "modern", "facade"]),
    ("portraits", "Portrait", ["portrait", "face", "person", "smile"])
]

companions_list = [["Nikhil"], ["Rahul"], ["Solo"], ["Family"], ["Sparsh"]]
weather_list = ["Sunny", "Overcast", "Raining", "Foggy", "Golden Hour", "Clear Night", "Snowing", "Indoors"]
clothing_list = ["Casual tee", "Winter jacket", "Hoodie", "Formal shirt", "Swim trunks", "Sundress"]

photos = []

# Generate exactly 50 photos
for i in range(1, 51):
    cat = random.choice(categories)
    cluster = f"Cluster_{cat[1]}"
    
    photo = {
        "photo_id": f"img_{i:03d}",
        "filename": f"{cat[1].lower()}_{i:03d}.jpg",
        "primary_object": cat[1],
        "keywords": cat[2],
        "location_name": f"Location {i}",
        "companions": random.choice(companions_list),
        "weather_vibe": random.choice(weather_list),
        "clothing_visuals": random.choice(clothing_list),
        "cluster": cluster
    }
    photos.append(photo)

output = "MOCK_PHOTOS_DATABASE = [\n"
for i, p in enumerate(photos):
    output += "    {\n"
    for k, v in p.items():
        if isinstance(v, str):
            output += f'        "{k}": "{v}",\n'
        elif isinstance(v, list):
            output += f'        "{k}": {json.dumps(v)},\n'
    output += "    }"
    if i < len(photos) - 1:
        output += ","
    output += "\n"
output += "]\n"

with open("generated_50.py", "w", encoding="utf-8") as f:
    f.write(output)

print("Generated.")
