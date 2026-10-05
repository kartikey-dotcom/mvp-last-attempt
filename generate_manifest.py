import os
import csv
import re
import pytest

def generate_manifest():
    os.makedirs('assets', exist_ok=True)
    raw_data = """
MOUNTAIN: mtn_01 black alone sunny afternoon backpack | mtn_02 pink friend sunny morning backpack | mtn_03 blue group cloudy afternoon none | mtn_04 white alone foggy morning none | mtn_05 red friend cloudy afternoon hat | mtn_06 black group sunny afternoon hat | mtn_07 green alone sunny sunset backpack | mtn_08 yellow friend foggy morning none
BEACH: bch_01 white alone sunny afternoon sunglasses | bch_02 blue friend sunny sunset none | bch_03 black group sunny afternoon hat | bch_04 pink alone cloudy morning none | bch_05 yellow friend sunny afternoon sunglasses | bch_06 red group cloudy sunset none | bch_07 green alone sunny sunset hat | bch_08 grey friend cloudy morning sunglasses
CAFE: caf_01 black alone indoor morning coffee | caf_02 pink friend indoor afternoon dessert | caf_03 blue group indoor afternoon coffee | caf_04 white alone rainy afternoon "hot chocolate" | caf_05 red friend rainy afternoon coffee | caf_06 grey group indoor night cocktail | caf_07 green friend indoor night dessert | caf_08 yellow alone rainy morning "hot chocolate"
CONCERT: con_01 black friend indoor night "purple lights" | con_02 black group indoor night "red lights" | con_03 pink alone indoor night "purple lights" | con_04 blue friend indoor night "red lights" | con_05 white group indoor night "blue lights" | con_06 red alone indoor night "blue lights" | con_07 grey friend indoor night "blue lights" | con_08 green group indoor night "purple lights"
STREET: str_01 black alone rainy night umbrella | str_02 pink friend rainy night "street food" | str_03 blue group rainy sunset umbrella | str_04 yellow alone rainy sunset none | str_05 white friend cloudy night "street food" | str_06 red group rainy night none | str_07 green alone cloudy sunset "street food" | str_08 grey friend rainy sunset umbrella
BALCONY: bal_01 black alone sunny sunset "orange sky" | bal_02 pink friend cloudy sunset "purple sky" | bal_03 blue alone cloudy sunset "pink sky" | bal_04 white friend sunny sunset "purple sky" | bal_05 yellow alone foggy sunset "orange sky" | bal_06 red friend sunny sunset "pink sky" | bal_07 green group cloudy sunset "orange sky" | bal_08 grey alone sunny sunset "purple sky"
"""
    
    base_tags = {
        "mountain": ["mountain", "hill", "sky", "tree", "person"],
        "beach": ["beach", "sea", "sand", "sky", "person"],
        "cafe": ["cafe", "table", "person"],
        "concert": ["concert", "stage", "crowd", "person"],
        "street": ["street", "road", "building", "person"],
        "balcony": ["balcony", "sky", "rooftop", "person"]
    }
    
    extra_to_tags = {
        "backpack": ["backpack"],
        "hat": ["hat"],
        "sunglasses": ["sunglasses"],
        "umbrella": ["umbrella"],
        "street food": ["food"],
        "coffee": ["coffee", "drink"],
        "hot chocolate": ["drink"],
        "dessert": ["dessert", "food"],
        "cocktail": ["drink", "glass"],
        "none": []
    }
    
    rows = []
    
    for line in raw_data.strip().split('\n'):
        if not line.strip(): continue
        cat_name, items = line.split(':', 1)
        cat_name = cat_name.strip().lower()
        items = [i.strip() for i in items.split('|')]
        for item in items:
            # Handle quotes in extra
            match = re.match(r'(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(.+)', item)
            id_val = match.group(1)
            shirt = match.group(2)
            companion = match.group(3)
            weather = match.group(4)
            time_of = match.group(5)
            extra = match.group(6).replace('"', '')
            
            tags = list(base_tags[cat_name])
            if extra in extra_to_tags:
                tags.extend(extra_to_tags[extra])
            elif "lights" in extra:
                tags.append("lights")
            # For "orange sky" etc, nothing is explicitly added from extra?
            # Wait, user didn't specify adding anything for sky colours, only "any lights extra -> lights"
            
            if time_of == "sunset":
                tags.append("sunset")
                
            objective_tags = "|".join(tags)
            filename = f"{id_val}.jpg"
            caption = f"A {weather} {time_of} in {cat_name}"
            rows.append({
                "id": id_val,
                "category": cat_name,
                "filename": filename,
                "shirt": shirt,
                "companion": companion,
                "weather": weather,
                "time_of_day": time_of,
                "extra": extra,
                "objective_tags": objective_tags,
                "caption": caption
            })
            
    with open('assets/photo_manifest.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

generate_manifest()
print("Generated manifest.")
