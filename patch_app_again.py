import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update get_mock_library to flatten episodic_discriminators
old_mock = re.search(r'@st\.cache_data\ndef get_mock_library\(\):.*?return MOCK_PHOTOS_DATABASE', content, flags=re.DOTALL)
new_mock = """@st.cache_data
def get_mock_library():
    from mock_data import MOCK_PHOTOS_DATABASE
    for p in MOCK_PHOTOS_DATABASE:
        p["id"] = p["photo_id"]
        p["palette"] = "blue"
        if "episodic_discriminators" in p:
            for k, v in p["episodic_discriminators"].items():
                p[k] = v
                if k == "companion": p["companions"] = [v]
                if k == "weather": p["weather_vibe"] = v
                if k == "clothing": p["clothing_visuals"] = v
    return MOCK_PHOTOS_DATABASE"""

if old_mock:
    content = content.replace(old_mock.group(0), new_mock)

# 2. Remove the 24 photo limit from the grids
# Library home view
content = content.replace("enumerate(library[:24]):", "enumerate(library):")
# Search results view
content = content.replace("enumerate(candidates[:24]):", "enumerate(candidates):")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("App patched for 100 photos and new schema.")
