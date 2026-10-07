import json
import re

text = """
**mtn_01** (mountain: black shirt, alone, sunny, afternoon, backpack)
> Candid smartphone photo of a young man wearing a plain black t-shirt, alone (exactly one person in the frame), on a hiking trail in the Himalayas with green slopes and distant peaks behind, carrying a backpack, bright sunny weather, afternoon light. 4:3, natural light, no text.

**mtn_02** (mountain: pink shirt, friend, sunny, morning, backpack)
> Candid smartphone photo of a young woman wearing a plain pink t-shirt, next to one friend (exactly two people in the frame), on a hiking trail in the Himalayas with green slopes and distant peaks behind, carrying a backpack, bright sunny weather, soft morning light. 4:3, natural light, no text.

**mtn_03** (mountain: blue shirt, group, cloudy, afternoon, none)
> Candid smartphone photo of a young man wearing a plain blue t-shirt, with three friends (four people in the frame), on a hiking trail in the Himalayas with green slopes and distant peaks behind, overcast sky, afternoon light. 4:3, natural light, no text.

**mtn_04** (mountain: white shirt, alone, foggy, morning, none)
> Candid smartphone photo of a young woman wearing a plain white t-shirt, alone (exactly one person in the frame), on a hiking trail in the Himalayas with green slopes and distant peaks behind, thick fog, soft morning light. 4:3, natural light, no text.

**mtn_05** (mountain: red shirt, friend, cloudy, afternoon, hat)
> Candid smartphone photo of a young man wearing a plain red t-shirt, next to one friend (exactly two people in the frame), on a hiking trail in the Himalayas with green slopes and distant peaks behind, wearing a cap, overcast sky, afternoon light. 4:3, natural light, no text.

**mtn_06** (mountain: black shirt, group, sunny, afternoon, hat)
> Candid smartphone photo of a young woman wearing a plain black t-shirt, with three friends (four people in the frame), on a hiking trail in the Himalayas with green slopes and distant peaks behind, wearing a cap, bright sunny weather, afternoon light. 4:3, natural light, no text.

**mtn_07** (mountain: green shirt, alone, sunny, sunset, backpack)
> Candid smartphone photo of a young man wearing a plain green t-shirt, alone (exactly one person in the frame), on a hiking trail in the Himalayas with green slopes and distant peaks behind, carrying a backpack, bright sunny weather, golden sunset light. 4:3, natural light, no text.

**mtn_08** (mountain: yellow shirt, friend, foggy, morning, none)
> Candid smartphone photo of a young woman wearing a plain yellow t-shirt, next to one friend (exactly two people in the frame), on a hiking trail in the Himalayas with green slopes and distant peaks behind, thick fog, soft morning light. 4:3, natural light, no text.

**bch_01** (beach: white shirt, alone, sunny, afternoon, sunglasses)
> Candid smartphone photo of a young man wearing a plain white t-shirt, alone (exactly one person in the frame), standing on a sandy beach with the sea and horizon behind, wearing sunglasses, bright sunny weather, afternoon light. 4:3, natural light, no text.

**bch_02** (beach: blue shirt, friend, sunny, sunset, none)
> Candid smartphone photo of a young woman wearing a plain blue t-shirt, next to one friend (exactly two people in the frame), standing on a sandy beach with the sea and horizon behind, bright sunny weather, golden sunset light. 4:3, natural light, no text.

**bch_03** (beach: black shirt, group, sunny, afternoon, hat)
> Candid smartphone photo of a young man wearing a plain black t-shirt, with three friends (four people in the frame), standing on a sandy beach with the sea and horizon behind, wearing a cap, bright sunny weather, afternoon light. 4:3, natural light, no text.

**bch_04** (beach: pink shirt, alone, cloudy, morning, none)
> Candid smartphone photo of a young woman wearing a plain pink t-shirt, alone (exactly one person in the frame), standing on a sandy beach with the sea and horizon behind, overcast sky, soft morning light. 4:3, natural light, no text.

**bch_05** (beach: yellow shirt, friend, sunny, afternoon, sunglasses)
> Candid smartphone photo of a young man wearing a plain yellow t-shirt, next to one friend (exactly two people in the frame), standing on a sandy beach with the sea and horizon behind, wearing sunglasses, bright sunny weather, afternoon light. 4:3, natural light, no text.

**bch_06** (beach: red shirt, group, cloudy, sunset, none)
> Candid smartphone photo of a young woman wearing a plain red t-shirt, with three friends (four people in the frame), standing on a sandy beach with the sea and horizon behind, overcast sky, golden sunset light. 4:3, natural light, no text.

**bch_07** (beach: green shirt, alone, sunny, sunset, hat)
> Candid smartphone photo of a young man wearing a plain green t-shirt, alone (exactly one person in the frame), standing on a sandy beach with the sea and horizon behind, wearing a cap, bright sunny weather, golden sunset light. 4:3, natural light, no text.

**bch_08** (beach: grey shirt, friend, cloudy, morning, sunglasses)
> Candid smartphone photo of a young woman wearing a plain grey t-shirt, next to one friend (exactly two people in the frame), standing on a sandy beach with the sea and horizon behind, wearing sunglasses, overcast sky, soft morning light. 4:3, natural light, no text.

**caf_01** (cafe: black shirt, alone, indoor, morning, coffee)
> Candid smartphone photo of a young man wearing a plain black t-shirt, alone (exactly one person in the frame), sitting at a wooden table in a cozy café, with a cup of coffee on the table, indoor lighting, soft morning light. 4:3, natural light, no text.

**caf_02** (cafe: pink shirt, friend, indoor, afternoon, dessert)
> Candid smartphone photo of a young woman wearing a plain pink t-shirt, next to one friend (exactly two people in the frame), sitting at a wooden table in a cozy café, with a dessert on the table, indoor lighting, afternoon light. 4:3, natural light, no text.

**caf_03** (cafe: blue shirt, group, indoor, afternoon, coffee)
> Candid smartphone photo of a young man wearing a plain blue t-shirt, with three friends (four people in the frame), sitting at a wooden table in a cozy café, with a cup of coffee on the table, indoor lighting, afternoon light. 4:3, natural light, no text.

**caf_04** (cafe: white shirt, alone, rainy, afternoon, hot chocolate)
> Candid smartphone photo of a young woman wearing a plain white t-shirt, alone (exactly one person in the frame), sitting at a wooden table in a cozy café, with a hot chocolate on the table, light rain, afternoon light, rain streaking the window behind. 4:3, natural light, no text.

**caf_05** (cafe: red shirt, friend, rainy, afternoon, coffee)
> Candid smartphone photo of a young man wearing a plain red t-shirt, next to one friend (exactly two people in the frame), sitting at a wooden table in a cozy café, with a cup of coffee on the table, light rain, afternoon light, rain streaking the window behind. 4:3, natural light, no text.

**caf_06** (cafe: grey shirt, group, indoor, night, cocktail)
> Candid smartphone photo of a young woman wearing a plain grey t-shirt, with three friends (four people in the frame), sitting at a wooden table in a cozy café, with a cocktail on the table, indoor lighting, night time. 4:3, natural light, no text.

**caf_07** (cafe: green shirt, friend, indoor, night, dessert)
> Candid smartphone photo of a young man wearing a plain green t-shirt, next to one friend (exactly two people in the frame), sitting at a wooden table in a cozy café, with a dessert on the table, indoor lighting, night time. 4:3, natural light, no text.

**caf_08** (cafe: yellow shirt, alone, rainy, morning, hot chocolate)
> Candid smartphone photo of a young woman wearing a plain yellow t-shirt, alone (exactly one person in the frame), sitting at a wooden table in a cozy café, with a hot chocolate on the table, light rain, soft morning light, rain streaking the window behind. 4:3, natural light, no text.

**con_01** (concert: black shirt, friend, indoor, night, purple lights)
> Candid smartphone photo of a young man wearing a plain black t-shirt, next to one friend (exactly two people in the frame), at a live music concert in a dark venue, crowd and stage behind, purple stage lights clearly visible, indoor lighting, night time. 4:3, natural light, no text.

**con_02** (concert: black shirt, group, indoor, night, red lights)
> Candid smartphone photo of a young woman wearing a plain black t-shirt, with three friends (four people in the frame), at a live music concert in a dark venue, crowd and stage behind, red stage lights clearly visible, indoor lighting, night time. 4:3, natural light, no text.

**con_03** (concert: pink shirt, alone, indoor, night, purple lights)
> Candid smartphone photo of a young man wearing a plain pink t-shirt, alone (exactly one person in the frame), at a live music concert in a dark venue, crowd and stage behind, purple stage lights clearly visible, indoor lighting, night time. 4:3, natural light, no text.

**con_04** (concert: blue shirt, friend, indoor, night, red lights)
> Candid smartphone photo of a young woman wearing a plain blue t-shirt, next to one friend (exactly two people in the frame), at a live music concert in a dark venue, crowd and stage behind, red stage lights clearly visible, indoor lighting, night time. 4:3, natural light, no text.

**con_05** (concert: white shirt, group, indoor, night, blue lights)
> Candid smartphone photo of a young man wearing a plain white t-shirt, with three friends (four people in the frame), at a live music concert in a dark venue, crowd and stage behind, blue stage lights clearly visible, indoor lighting, night time. 4:3, natural light, no text.

**con_06** (concert: red shirt, alone, indoor, night, blue lights)
> Candid smartphone photo of a young woman wearing a plain red t-shirt, alone (exactly one person in the frame), at a live music concert in a dark venue, crowd and stage behind, blue stage lights clearly visible, indoor lighting, night time. 4:3, natural light, no text.

**con_07** (concert: grey shirt, friend, indoor, night, blue lights)
> Candid smartphone photo of a young man wearing a plain grey t-shirt, next to one friend (exactly two people in the frame), at a live music concert in a dark venue, crowd and stage behind, blue stage lights clearly visible, indoor lighting, night time. 4:3, natural light, no text.

**con_08** (concert: green shirt, group, indoor, night, purple lights)
> Candid smartphone photo of a young woman wearing a plain green t-shirt, with three friends (four people in the frame), at a live music concert in a dark venue, crowd and stage behind, purple stage lights clearly visible, indoor lighting, night time. 4:3, natural light, no text.

**str_01** (street: black shirt, alone, rainy, night, umbrella)
> Candid smartphone photo of a young man wearing a plain black t-shirt, alone (exactly one person in the frame), on a busy Indian city street next to a street-food stall, wet road reflecting lights, holding an umbrella, light rain, night time. 4:3, natural light, no text.

**str_02** (street: pink shirt, friend, rainy, night, street food)
> Candid smartphone photo of a young woman wearing a plain pink t-shirt, next to one friend (exactly two people in the frame), on a busy Indian city street next to a street-food stall, wet road reflecting lights, with street food visible in the shot, light rain, night time. 4:3, natural light, no text.

**str_03** (street: blue shirt, group, rainy, sunset, umbrella)
> Candid smartphone photo of a young man wearing a plain blue t-shirt, with three friends (four people in the frame), on a busy Indian city street next to a street-food stall, wet road reflecting lights, holding an umbrella, light rain, golden sunset light. 4:3, natural light, no text.

**str_04** (street: yellow shirt, alone, rainy, sunset, none)
> Candid smartphone photo of a young woman wearing a plain yellow t-shirt, alone (exactly one person in the frame), on a busy Indian city street next to a street-food stall, wet road reflecting lights, light rain, golden sunset light. 4:3, natural light, no text.

**str_05** (street: white shirt, friend, cloudy, night, street food)
> Candid smartphone photo of a young man wearing a plain white t-shirt, next to one friend (exactly two people in the frame), on a busy Indian city street next to a street-food stall, wet road reflecting lights, with street food visible in the shot, overcast sky, night time. 4:3, natural light, no text.

**str_06** (street: red shirt, group, rainy, night, none)
> Candid smartphone photo of a young woman wearing a plain red t-shirt, with three friends (four people in the frame), on a busy Indian city street next to a street-food stall, wet road reflecting lights, light rain, night time. 4:3, natural light, no text.

**str_07** (street: green shirt, alone, cloudy, sunset, street food)
> Candid smartphone photo of a young man wearing a plain green t-shirt, alone (exactly one person in the frame), on a busy Indian city street next to a street-food stall, wet road reflecting lights, with street food visible in the shot, overcast sky, golden sunset light. 4:3, natural light, no text.

**str_08** (street: grey shirt, friend, rainy, sunset, umbrella)
> Candid smartphone photo of a young woman wearing a plain grey t-shirt, next to one friend (exactly two people in the frame), on a busy Indian city street next to a street-food stall, wet road reflecting lights, holding an umbrella, light rain, golden sunset light. 4:3, natural light, no text.

**bal_01** (balcony: black shirt, alone, sunny, sunset, orange sky)
> Candid smartphone photo of a young man wearing a plain black t-shirt, alone (exactly one person in the frame), on a home balcony, rooftops and sky behind, the sky glowing orange, bright sunny weather, golden sunset light. 4:3, natural light, no text.

**bal_02** (balcony: pink shirt, friend, cloudy, sunset, purple sky)
> Candid smartphone photo of a young woman wearing a plain pink t-shirt, next to one friend (exactly two people in the frame), on a home balcony, rooftops and sky behind, the sky glowing purple, overcast sky, golden sunset light. 4:3, natural light, no text.

**bal_03** (balcony: blue shirt, alone, cloudy, sunset, pink sky)
> Candid smartphone photo of a young man wearing a plain blue t-shirt, alone (exactly one person in the frame), on a home balcony, rooftops and sky behind, the sky glowing pink, overcast sky, golden sunset light. 4:3, natural light, no text.

**bal_04** (balcony: white shirt, friend, sunny, sunset, purple sky)
> Candid smartphone photo of a young woman wearing a plain white t-shirt, next to one friend (exactly two people in the frame), on a home balcony, rooftops and sky behind, the sky glowing purple, bright sunny weather, golden sunset light. 4:3, natural light, no text.

**bal_05** (balcony: yellow shirt, alone, foggy, sunset, orange sky)
> Candid smartphone photo of a young man wearing a plain yellow t-shirt, alone (exactly one person in the frame), on a home balcony, rooftops and sky behind, the sky glowing orange, thick fog, golden sunset light. 4:3, natural light, no text.

**bal_06** (balcony: red shirt, friend, sunny, sunset, pink sky)
> Candid smartphone photo of a young woman wearing a plain red t-shirt, next to one friend (exactly two people in the frame), on a home balcony, rooftops and sky behind, the sky glowing pink, bright sunny weather, golden sunset light. 4:3, natural light, no text.

**bal_07** (balcony: green shirt, group, cloudy, sunset, orange sky)
> Candid smartphone photo of a young man wearing a plain green t-shirt, with three friends (four people in the frame), on a home balcony, rooftops and sky behind, the sky glowing orange, overcast sky, golden sunset light. 4:3, natural light, no text.

**bal_08** (balcony: grey shirt, alone, sunny, sunset, purple sky)
> Candid smartphone photo of a young woman wearing a plain grey t-shirt, alone (exactly one person in the frame), on a home balcony, rooftops and sky behind, the sky glowing purple, bright sunny weather, golden sunset light. 4:3, natural light, no text.
"""

prompts = []
matches = re.finditer(r'\*\*(.*?)\*\*.*\n>\s*(.*)', text)
for m in matches:
    prompts.append({
        "id": m.group(1),
        "prompt": m.group(2)
    })

print(json.dumps(prompts))
