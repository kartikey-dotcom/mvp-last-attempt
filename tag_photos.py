import os
import json
import glob
from google import genai

def tag_photos():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable.")
        return

    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"

    prompt = """You are a photo tagging assistant. Analyze the image and return a JSON object with the following keys and allowed values only:
- scene: beach, city, mountain, home, restaurant, wedding
- weather: sunny, rainy, cloudy, foggy
- time_of_day: morning, afternoon, sunset, night
- season: summer, monsoon, winter
- palette: purple, orange, blue, green, red, grey
- caption: a one-sentence descriptive caption

Only output valid JSON. Do not include markdown formatting like ```json.
Only include a key if you are reasonably confident.
Never invent values outside the allowed list for the categorical keys.
"""

    tags = {}
    
    photo_files = glob.glob("assets/photos/photo_*.jpg")
    photo_files.sort()
    
    for photo_path in photo_files:
        filename = os.path.basename(photo_path)
        print(f"Processing {filename}...")
        
        try:
            with open(photo_path, "rb") as f:
                image_data = f.read()
                
            response = client.models.generate_content(
                model=model,
                contents=[
                    prompt,
                    genai.types.Part.from_bytes(data=image_data, mime_type="image/jpeg")
                ],
                config=genai.types.GenerateContentConfig(
                    temperature=0.0,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            
            # Validation
            vocab = {
                "scene": ["beach", "city", "mountain", "home", "restaurant", "wedding"],
                "weather": ["sunny", "rainy", "cloudy", "foggy"],
                "time_of_day": ["morning", "afternoon", "sunset", "night"],
                "season": ["summer", "monsoon", "winter"],
                "palette": ["purple", "orange", "blue", "green", "red", "grey"]
            }
            
            valid_result = {}
            for k, v in result.items():
                if k in vocab and v in vocab[k]:
                    valid_result[k] = v
                elif k == "caption":
                    valid_result[k] = v
                    
            tags[filename] = valid_result
            print(f"  Success: {valid_result}")
            
        except Exception as e:
            print(f"  Failed for {filename}: {e}")

    with open("photo_tags.json", "w") as f:
        json.dump(tags, f, indent=2)
    print("Done. Wrote photo_tags.json")

if __name__ == "__main__":
    tag_photos()
