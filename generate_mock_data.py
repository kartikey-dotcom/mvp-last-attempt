import json
import random
from datetime import datetime, timedelta

rng = random.Random(42)

# Eras
eras = [
    {"name": "Goa Trip Oct 2023", "start": datetime(2023, 10, 1), "end": datetime(2023, 10, 10), "locations": ["Baga Beach", "Anjuna", "Panjim", "Chapora Fort", "Curlies Shack"]},
    {"name": "Dharamshala Trek Mar 2024", "start": datetime(2024, 3, 15), "end": datetime(2024, 3, 22), "locations": ["Triund Hill", "Bhagsu Waterfall", "McLeod Ganj", "Dalai Lama Temple", "Illiterati Cafe"]},
    {"name": "Local Hangouts Delhi", "start": datetime(2024, 4, 1), "end": datetime(2024, 8, 30), "locations": ["Café Coffee Day", "Hauz Khas Village", "Connaught Place", "India Gate", "Lodhi Garden"]}
]

# Pools
companions_pool = [["Nikhil"], ["Rahul"], ["Sparsh"], ["Nikhil", "Sparsh"], ["Rahul", "Nikhil"], ["Solo"], ["Family"]]
weather_pool = ["Sunny / Beach", "Raining", "Overcast", "Cozy / Indoors", "Clear Night", "Foggy"]
clothing_pool = ["Hoodie", "Swim trunks", "Winter jacket", "Casual tee", "Formal shirt", "Sundress", "Trek pants"]
object_pool = ["Food", "Sunset", "Backpack", "Drinks", "Street dog", "Bonfire", "Coffee cup", "Guitar"]

dataset = []

for i in range(1, 73):
    era = eras[i % 3] # distribute evenly across 3 eras
    
    # Pick a random date within the era
    days_diff = (era["end"] - era["start"]).days
    rand_days = rng.randint(0, max(1, days_diff))
    timestamp = era["start"] + timedelta(days=rand_days, hours=rng.randint(8, 22))
    
    # Force Rahul/Nikhil for 15-20 photos
    comp = rng.choice(companions_pool)
    if i <= 20: 
        comp = rng.choice([["Rahul"], ["Nikhil"], ["Rahul", "Nikhil"]])
    
    # Weather
    weather = rng.choice(weather_pool)
    if i % 2 == 0 and weather not in ["Sunny / Beach", "Raining"]:
        weather = rng.choice(["Sunny / Beach", "Raining"])
        
    loc = rng.choice(era["locations"])
    obj = rng.choice(object_pool)
    cloth = rng.choice(clothing_pool)
    
    # Logical adjustments
    if "Beach" in loc: 
        weather = "Sunny / Beach" if rng.random() > 0.3 else "Clear Night"
        cloth = rng.choice(["Swim trunks", "Casual tee"])
        obj = rng.choice(["Sunset", "Drinks", "Food"])
    if "Trek" in loc or "Hill" in loc or "Waterfall" in loc:
        cloth = rng.choice(["Hoodie", "Winter jacket", "Trek pants"])
        weather = rng.choice(["Foggy", "Overcast", "Sunny / Beach"])
    if "Cafe" in loc or "Café" in loc or "Indoors" in weather:
        weather = "Cozy / Indoors"
        obj = rng.choice(["Coffee cup", "Food", "Drinks"])
    
    photo = {
        "photo_id": f"img_{i:03d}",
        "filename": f"{loc.lower().replace(' ', '_')}_{obj.lower().replace(' ', '_')}.jpg",
        "absolute_timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
        "location_name": loc,
        "companions": comp,
        "weather_vibe": weather,
        "clothing_visuals": cloth,
        "primary_object": obj
    }
    dataset.append(photo)

# Generate python file string
py_out = "MOCK_PHOTOS_DATABASE = " + json.dumps(dataset, indent=4) + "\\n"
with open("mock_data.py", "w", encoding="utf-8") as f:
    f.write(py_out)

print("Generated mock_data.py")
