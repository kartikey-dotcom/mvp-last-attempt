import os
import csv
from PIL import Image, ImageDraw, ImageFont

colors = {
    "black": (32, 33, 36), "pink": (244, 63, 94), "blue": (26, 115, 232), 
    "white": (255, 255, 255), "red": (234, 67, 53), "yellow": (251, 188, 4), 
    "green": (52, 168, 83), "grey": (95, 99, 104)
}

bg_colors = {
    "mountain": (220, 240, 220), "beach": (220, 230, 250), "cafe": (240, 230, 220), 
    "concert": (230, 220, 240), "street": (230, 230, 230), "balcony": (250, 230, 220)
}

# Try to find a default font
try:
    font = ImageFont.truetype("arial.ttf", 32)
except IOError:
    font = ImageFont.load_default()

manifest_path = "assets/photo_manifest.csv"
with open(manifest_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fid = row['id']
        path = f"assets/photos/{fid}.jpg"
        
        # If image is > 100KB, it's probably our real AI image, skip
        if os.path.exists(path) and os.path.getsize(path) > 100000:
            print(f"Skipping {fid} (already has real image)")
            continue
            
        print(f"Generating mock for {fid}")
        
        cat = row['category']
        shirt = row['shirt']
        comp = row['companion']
        comp_count = {"alone": 1, "friend": 2, "group": 4}.get(comp, 1)
        
        bg = bg_colors.get(cat, (240, 240, 240))
        img = Image.new('RGB', (480, 480), color=bg)
        draw = ImageDraw.Draw(img)
        
        # Draw people
        c = colors.get(shirt, (150, 150, 150))
        for i in range(comp_count):
            x = 240 - (comp_count * 40) + (i * 80)
            y = 240
            # head
            draw.ellipse((x-20, y-40, x+20, y), fill=(200, 180, 150))
            # body (shirt)
            draw.rectangle((x-25, y, x+25, y+60), fill=c)
            
        # Draw text
        text = f"{cat.upper()}\n{shirt.upper()} SHIRT\n{comp_count} PEOPLE"
        
        try:
            # For PIL < 9.2.0 compatibility
            w, h = draw.textsize(text, font=font)
        except AttributeError:
            bbox = draw.textbbox((0,0), text, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            
        draw.text(((480-w)/2, 60), text, font=font, fill=(50, 50, 50), align="center")
        
        img.save(path, format="JPEG", quality=90)

print("Done generating mock images!")
