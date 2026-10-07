import csv
import re
import math

def load_manifest(path="assets/photo_manifest.csv"):
    photos = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['objective_tags'] = row['objective_tags'].split('|')
                photos.append(row)
    except FileNotFoundError:
        pass
    return photos

def baseline_search(photos, query):
    if not query: return photos
    import string
    # lowercase, strip punctuation
    q = query.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = set(q.split())
    stopwords = {"a", "an", "the", "my", "me", "of", "in", "at", "on", "photo", "photos", "picture", "pictures"}
    tokens = tokens - stopwords
    if not tokens: return photos
    
    # Try singular forms naively by stripping 's' if not in token list
    singular_tokens = set()
    for t in tokens:
        singular_tokens.add(t)
        if t.endswith('s') and len(t) > 3:
            singular_tokens.add(t[:-1])
    
    results = []
    for p in photos:
        # Build a comprehensive search string from all attributes
        search_blob = " ".join([str(v) for v in p.values()]).lower()
        # Add implied words to help with matching
        search_blob += f" {p.get('shirt', '')} shirt tee t-shirt"
        search_blob += f" {p.get('companion', '')} people person group friends"
        search_blob += f" {p.get('category', '')} place location"
        search_blob += f" {p.get('weather', '')} weather"
        search_blob += f" {p.get('time_of_day', '')} time"
        search_blob += f" {p.get('extra', '')} extra"
        
        match = True
        for original_token in tokens:
            sing = original_token[:-1] if original_token.endswith('s') and len(original_token) > 3 else original_token
            if original_token not in search_blob and sing not in search_blob:
                match = False
                break
        if match:
            results.append(p)
    return results

def parse_query(query, photos):
    if not query: return photos, {}, []
    import string
    q = query.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = set(q.split())
    
    # Extract hints
    hints = {}
    
    category_map = {
        "mountain": ["mountain", "mountains", "hill", "hills", "trek", "trekking", "hike", "hiking", "himalaya", "dharamshala"],
        "beach": ["beach", "sea", "sand", "goa", "waves"],
        "cafe": ["cafe", "café", "coffee", "dessert", "dinner", "lunch", "restaurant", "food"],
        "concert": ["concert", "gig", "music", "stage", "neon"],
        "street": ["street", "stall", "metro"],
        "balcony": ["balcony", "terrace", "home"]
    }
    
    weather_map = {
        "sunny": ["sunny"],
        "cloudy": ["cloudy"],
        "rainy": ["rain", "rainy", "raining", "monsoon"],
        "foggy": ["fog", "foggy", "misty"]
    }
    
    time_map = {
        "morning": ["morning"],
        "afternoon": ["afternoon"],
        "sunset": ["sunset", "dusk", "evening"],
        "night": ["night"]
    }
    
    companion_map = {
        "alone": ["alone"],
        "friend": ["friend", "friends"],
        "group": ["group"]
    }
    
    # find category
    for cat, words in category_map.items():
        if any(w in tokens for w in words):
            hints["category"] = cat
            break
            
    # find weather
    for w, words in weather_map.items():
        if any(w2 in tokens for w2 in words):
            hints["weather"] = w
            break
            
    # find time_of_day
    for t, words in time_map.items():
        if any(w in tokens for w in words):
            hints["time_of_day"] = t
            break
            
    # find companion
    for c, words in companion_map.items():
        if any(w in tokens for w in words):
            hints["companion"] = c
            break
            
    # shirt and extra based on colors
    colors = ["black", "pink", "blue", "white", "red", "yellow", "green", "grey", "gray"]
    words_list = q.split()
    for i, w in enumerate(words_list):
        if w in colors:
            if i + 1 < len(words_list):
                nxt = words_list[i+1]
                if nxt in ["shirt", "tee", "t-shirt", "tshirt"]:
                    hints["shirt"] = "grey" if w == "gray" else w
                elif nxt == "lights":
                    hints["extra"] = f"{w} lights"
                elif nxt == "sky":
                    hints["extra"] = f"{w} sky"

    def match_hints(hints_dict):
        res = []
        for p in photos:
            match = True
            for k, v in hints_dict.items():
                if p[k] != v:
                    match = False
                    break
            if match:
                res.append(p)
        return res

    candidates = match_hints(hints)
    dropped = []
    
    if len(candidates) == 0 and len(hints) > 0:
        drop_order = ["shirt", "extra", "time_of_day", "weather", "companion", "category"]
        for attr in drop_order:
            if attr in hints:
                dropped.append(hints[attr]) # or format it
                del hints[attr]
                candidates = match_hints(hints)
                if len(candidates) > 0:
                    break
                    
    if len(candidates) == 0:
        candidates = photos

    return candidates, hints, dropped

def binary_entropy(p):
    if p <= 0 or p >= 1: return 0.0
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))

def build_predicates(candidates, skipped_attrs):
    n = len(candidates)
    if n == 0: return []
    
    preds = []
    
    def add_pred(attr, key, text, label, fn):
        if attr in skipped_attrs: return
        yes_count = sum(1 for p in candidates if fn(p))
        if 0 < yes_count < n:
            preds.append({
                "attr": attr,
                "key": key,
                "text": text,
                "label": label,
                "fn": fn,
                "yes_count": yes_count
            })
            
    # Category
    cat_texts = {
        "mountain": "Were you in the mountains?",
        "beach": "Were you at the beach?",
        "cafe": "Were you at a café?",
        "concert": "Were you at a concert?",
        "street": "Were you out on a city street?",
        "balcony": "Were you on a balcony at home?"
    }
    for cat in cat_texts.keys():
        add_pred("category", f"cat={cat}", cat_texts[cat], cat.capitalize(), lambda p, c=cat: p["category"] == c)
        
    # Companion
    add_pred("companion", "with_someone", "Were you with someone?", "With someone", lambda p: p["companion"] != "alone")
    add_pred("companion", "group", "Were you with a group of people?", "Group", lambda p: p["companion"] == "group")
    add_pred("companion", "friend", "Were you with just one other person?", "One person", lambda p: p["companion"] == "friend")
    
    # Shirt
    colors = ["black", "pink", "blue", "white", "red", "yellow", "green", "grey"]
    for c in colors:
        add_pred("shirt", f"shirt={c}", f"Do you remember if you were wearing a {c} shirt?", f"{c.capitalize()} shirt", lambda p, color=c: p["shirt"] == color)
        
    # Extra
    extra_texts = {
        "backpack": ("Were you carrying a backpack?", "Backpack"),
        "hat": ("Were you wearing a cap?", "Hat"),
        "sunglasses": ("Were you wearing sunglasses?", "Sunglasses"),
        "umbrella": ("Did you have an umbrella?", "Umbrella"),
        "street food": ("Was there street food in the shot?", "Street food"),
        "coffee": ("Was there a coffee on the table?", "Coffee"),
        "hot chocolate": ("Was there a hot chocolate on the table?", "Hot chocolate"),
        "dessert": ("Was there a dessert on the table?", "Dessert"),
        "cocktail": ("Was there a cocktail on the table?", "Cocktail"),
        "purple lights": ("Were the stage lights purple?", "Purple lights"),
        "red lights": ("Were the stage lights red?", "Red lights"),
        "blue lights": ("Were the stage lights blue?", "Blue lights"),
        "orange sky": ("Was the sky orange?", "Orange sky"),
        "purple sky": ("Was the sky purple?", "Purple sky"),
        "pink sky": ("Was the sky pink?", "Pink sky")
    }
    for ext, (txt, lbl) in extra_texts.items():
        add_pred("extra", f"extra={ext}", txt, lbl, lambda p, e=ext: p["extra"] == e)
        
    # Weather
    w_texts = {
        "sunny": ("Was it sunny?", "Sunny"),
        "cloudy": ("Was it cloudy?", "Cloudy"),
        "rainy": ("Was it raining?", "Rainy"),
        "foggy": ("Was it foggy?", "Foggy"),
        "indoor": ("Were you indoors?", "Indoor")
    }
    for w, (txt, lbl) in w_texts.items():
        add_pred("weather", f"w={w}", txt, lbl, lambda p, wx=w: p["weather"] == wx)
        
    # Time of day
    t_texts = {
        "morning": ("Was it in the morning?", "Morning"),
        "afternoon": ("Was it in the afternoon?", "Afternoon"),
        "sunset": ("Was it around sunset?", "Sunset"),
        "night": ("Was it at night?", "Night")
    }
    for t, (txt, lbl) in t_texts.items():
        add_pred("time_of_day", f"t={t}", txt, lbl, lambda p, tx=t: p["time_of_day"] == tx)
        
    return preds

def pick_question(preds, n):
    if not preds: return None
    
    WEIGHTS = {
        "category": 1.0,
        "companion": 1.0,
        "shirt": 0.95,
        "extra": 0.9,
        "weather": 0.9,
        "time_of_day": 0.8
    }
    
    ATTR_ORDER = {"category": 0, "companion": 1, "shirt": 2, "extra": 3, "weather": 4, "time_of_day": 5}
    
    best_pred = None
    best_score = -1.0
    best_tie_1 = 999
    best_tie_2 = 999
    best_tie_3 = 999
    best_tie_4 = ""
    
    for p in preds:
        score = binary_entropy(p["yes_count"] / n) * WEIGHTS[p["attr"]]
        score = round(score, 9)
        
        t1 = abs(p["yes_count"] - n/2)
        t2 = ATTR_ORDER[p["attr"]]
        t3 = 0 if p["key"] == "with_someone" else 1
        t4 = p["key"]
        
        is_better = False
        if score > best_score:
            is_better = True
        elif score == best_score:
            if t1 < best_tie_1: is_better = True
            elif t1 == best_tie_1:
                if t2 < best_tie_2: is_better = True
                elif t2 == best_tie_2:
                    if t3 < best_tie_3: is_better = True
                    elif t3 == best_tie_3:
                        if t4 < best_tie_4: is_better = True
                        
        if is_better:
            best_score = score
            best_tie_1 = t1
            best_tie_2 = t2
            best_tie_3 = t3
            best_tie_4 = t4
            best_pred = p
            
    return best_pred

def apply_answers(initial_candidates, answers_list):
    # answers_list: list of dicts {"attr": attr, "key": key, "val": True/False/None, "fn": fn, "label": label, "text": text}
    cands = initial_candidates
    skipped_attrs = set()
    
    for ans in answers_list:
        if ans["val"] is None:
            skipped_attrs.add(ans["attr"])
        else:
            cands = [p for p in cands if ans["fn"](p) == ans["val"]]
            
    return cands, skipped_attrs
