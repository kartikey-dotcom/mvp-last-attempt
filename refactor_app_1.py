import re
import os

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
if "import engine" not in content:
    content = content.replace("import streamlit as st", "import streamlit as st\nimport engine\nfrom PIL import Image\nimport io\nimport base64")

# 2. Replace get_mock_library with new loading logic
pattern = re.compile(r'# -----------------\n# DATA MODEL\n# -----------------.*?library = get_mock_library\(\)', re.DOTALL)
new_data_model = """# -----------------
# DATA MODEL
# -----------------
@st.cache_data
def get_library():
    return engine.load_manifest("assets/photo_manifest.csv")

library = get_library()

@st.cache_data
def get_image_base64(photo_id, category, shirt, companion):
    path = f"assets/photos/{photo_id}.jpg"
    if os.path.exists(path):
        try:
            img = Image.open(path)
            img.thumbnail((480, 480))
            # crop square
            w, h = img.size
            if w != h:
                min_dim = min(w, h)
                left = (w - min_dim)/2
                top = (h - min_dim)/2
                right = (w + min_dim)/2
                bottom = (h + min_dim)/2
                img = img.crop((left, top, right, bottom))
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            return base64.b64encode(buf.getvalue()).decode()
        except Exception:
            pass
            
    # Inline SVG placeholder
    colors = {
        "black": "#202124", "pink": "#F43F5E", "blue": "#1A73E8", 
        "white": "#FFFFFF", "red": "#EA4335", "yellow": "#FBBC04", 
        "green": "#34A853", "grey": "#5F6368"
    }
    emojis = {
        "mountain": "⛰️", "beach": "🏖️", "cafe": "☕", 
        "concert": "🎤", "street": "🌧️", "balcony": "🌇"
    }
    comp_count = {"alone": 1, "friend": 2, "group": 4}.get(companion, 1)
    
    shirt_color = colors.get(shirt, "#9AA0A6")
    emoji = emojis.get(category, "📷")
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
        <rect width="400" height="400" fill="#F8F9FA"/>
        <text x="50%" y="40%" font-size="80" text-anchor="middle" dominant-baseline="middle">{emoji}</text>
        <circle cx="200" cy="240" r="30" fill="{shirt_color}" stroke="#DADCE0" stroke-width="2"/>
        <text x="50%" y="320" font-size="24" text-anchor="middle" fill="#5F6368">{"👤 " * comp_count}</text>
    </svg>'''
    return base64.b64encode(svg.encode()).decode()
"""
content = re.sub(pattern, new_data_model, content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated data model in app.py")
