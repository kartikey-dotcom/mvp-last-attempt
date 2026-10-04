import streamlit as st
import pandas as pd
import random
import math
from collections import Counter

# Phase 1: Environment Setup & Data Model

# Set up basic Streamlit page config
st.set_page_config(page_title="Progressive Contextual Disambiguation", layout="wide")

def generate_mock_library(seed=11):
    """
    Generates exactly 72 mock photos using a fixed random seed.
    Enforces the demo seeding rule for the first 10 photos.
    """
    random.seed(seed)
    library = []
    
    scenes = ["beach", "city", "mountain", "home", "restaurant", "wedding"]
    peoples = ["Rohan", "Mom", "Ananya", "alone"]
    weathers = ["sunny", "rainy", "cloudy", "foggy"]
    times_of_day = ["morning", "afternoon", "sunset", "night"]
    seasons = ["summer", "monsoon", "winter"]
    palettes = ["purple", "orange", "blue", "green", "red", "grey"]
    occasions = ["none", "none", "trip", "birthday", "wedding"]
    activities = ["walking", "driving", "scooter ride", "shopping", "relaxing"]
    
    for i in range(72):
        photo_id = f"IMG_{1000 + i}"
        
        # Demo seeding rule: first 10 photos explicitly have palette=purple and time_of_day=sunset
        if i < 10:
            palette = "purple"
            time_of_day = "sunset"
            # Rotate through scenes to guarantee variety
            scene = scenes[i % len(scenes)]
        else:
            palette = random.choice(palettes)
            time_of_day = random.choice(times_of_day)
            scene = random.choice(scenes)
            
        people = random.choice(peoples)
        weather = random.choice(weathers)
        season = random.choice(seasons)
        occasion = random.choice(occasions)
        activity = random.choice(activities)
        
        # Build objective tags
        objective = [
            scene, people, weather, time_of_day, season, palette, occasion, activity
        ]
        
        # Standard searchable tags for specific scenes
        if scene == "beach":
            objective.extend(["sea", "sand", "sky"])
        elif scene == "city":
            objective.extend(["buildings", "streets", "urban"])
        elif scene == "mountain":
            objective.extend(["hills", "nature", "trek"])
            
        # Ensure all objectives are lowercase for baseline search
        objective = [str(o).lower() for o in objective]
        
        photo = {
            "id": photo_id,
            "scene": scene,
            "people": people,
            "weather": weather,
            "time_of_day": time_of_day,
            "season": season,
            "palette": palette,
            "occasion": occasion,
            "activity": activity,
            "objective": list(set(objective)) # Remove duplicates
        }
        library.append(photo)
        
    return library

def init_session_state():
    """
    Initializes required variables in st.session_state.
    """
    if "mock_library" not in st.session_state:
        st.session_state.mock_library = generate_mock_library()
    
    if "search_mode" not in st.session_state:
        st.session_state.search_mode = "Current search (baseline)"
        
    if "current_query" not in st.session_state:
        st.session_state.current_query = ""
        
    if "inferred_hints" not in st.session_state:
        st.session_state.inferred_hints = {}
        
    if "asked_questions" not in st.session_state:
        st.session_state.asked_questions = []
        
    if "candidate_photos" not in st.session_state:
        st.session_state.candidate_photos = st.session_state.mock_library
        
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
        
    if "log_data" not in st.session_state:
        st.session_state.log_data = pd.DataFrame(columns=[
            "query", "mode", "questions_answered", "seconds_to_success", "photo_id", "timestamp"
        ])
        
    if "search_submitted" not in st.session_state:
        st.session_state.search_submitted = False
        
    if "success_message" not in st.session_state:
        st.session_state.success_message = None

SCENE_EMOJIS = {
    "beach": "🏖️",
    "city": "🏙️",
    "mountain": "⛰️",
    "home": "🏠",
    "restaurant": "🍽️",
    "wedding": "💒"
}

SYNONYM_MAP = {
    "beach": {"scene": "beach"}, "sea": {"scene": "beach"}, "sand": {"scene": "beach"}, "ocean": {"scene": "beach"},
    "city": {"scene": "city"}, "urban": {"scene": "city"}, "street": {"scene": "city"},
    "mountain": {"scene": "mountain"}, "hills": {"scene": "mountain"}, "trek": {"scene": "mountain"},
    "home": {"scene": "home"}, "house": {"scene": "home"},
    "restaurant": {"scene": "restaurant"}, "food": {"scene": "restaurant"}, "dining": {"scene": "restaurant"},
    "wedding": {"scene": "wedding"}, "marriage": {"scene": "wedding"},
    "rohan": {"people": "Rohan"}, "mom": {"people": "Mom"}, "mother": {"people": "Mom"}, "ananya": {"people": "Ananya"},
    "alone": {"people": "alone"}, "solo": {"people": "alone"},
    "sunny": {"weather": "sunny"}, "sun": {"weather": "sunny"}, "rainy": {"weather": "rainy"}, "rain": {"weather": "rainy"},
    "cloudy": {"weather": "cloudy"}, "clouds": {"weather": "cloudy"}, "foggy": {"weather": "foggy"}, "fog": {"weather": "foggy"},
    "morning": {"time_of_day": "morning"}, "afternoon": {"time_of_day": "afternoon"}, 
    "sunset": {"time_of_day": "sunset"}, "dusk": {"time_of_day": "sunset"},
    "night": {"time_of_day": "night"}, "dark": {"time_of_day": "night"},
    "summer": {"season": "summer"}, "monsoon": {"season": "monsoon"}, "winter": {"season": "winter"},
    "purple": {"palette": "purple"}, "orange": {"palette": "orange"}, "blue": {"palette": "blue"},
    "green": {"palette": "green"}, "red": {"palette": "red"}, "grey": {"palette": "grey"},
    "trip": {"occasion": "trip"}, "vacation": {"occasion": "trip"}, "birthday": {"occasion": "birthday"},
    "walking": {"activity": "walking"}, "walk": {"activity": "walking"},
    "driving": {"activity": "driving"}, "drive": {"activity": "driving"},
    "scooter": {"activity": "scooter ride"}, "ride": {"activity": "scooter ride"},
    "shopping": {"activity": "shopping"}, "relaxing": {"activity": "relaxing"}, "chill": {"activity": "relaxing"}
}

DROP_HIERARCHY = [
    "season", "activity", "occasion", "time_of_day", "scene", "palette", "people", "weather"
]

def parse_hints(query):
    hints = {}
    tokens = set(query.lower().split())
    for token in tokens:
        if token in SYNONYM_MAP:
            hints.update(SYNONYM_MAP[token])
    return hints

def filter_by_hints(library, hints):
    results = []
    for photo in library:
        match = True
        for k, v in hints.items():
            if photo.get(k) != v:
                match = False
                break
        if match:
            results.append(photo)
    return results

def apply_constraint_relaxation(library, hints):
    current_hints = hints.copy()
    results = filter_by_hints(library, current_hints)
    
    if len(results) > 0:
        return results, current_hints
        
    for attr in DROP_HIERARCHY:
        if attr in current_hints:
            del current_hints[attr]
            results = filter_by_hints(library, current_hints)
            if len(results) > 0:
                return results, current_hints
                
    return library, current_hints

QUESTION_MAP = {
    "scene": "Where were you?",
    "season": "Which season was it?",
    "occasion": "Was it a special occasion?",
    "people": "Who was with you?",
    "weather": "What was the weather like?",
    "time_of_day": "What time of day was it?",
    "palette": "Which colour stands out in your memory?",
    "activity": "What were you doing just before?"
}

def calculate_shannon_entropy(candidate_photos, asked_questions, inferred_hints):
    attributes = ["scene", "people", "weather", "time_of_day", "season", "palette", "occasion", "activity"]
    unasked_attributes = [attr for attr in attributes if attr not in asked_questions and attr not in inferred_hints]
    
    best_attr = None
    max_entropy = 0
    total_photos = len(candidate_photos)
    
    if total_photos <= 1 or not unasked_attributes:
        return None, 0
        
    for attr in unasked_attributes:
        counts = Counter([photo.get(attr) for photo in candidate_photos])
        entropy = 0
        for count in counts.values():
            p = count / total_photos
            entropy -= p * math.log2(p)
            
        if entropy > max_entropy:
            max_entropy = entropy
            best_attr = attr
            
    return best_attr, max_entropy

def on_chip_click(attr, value):
    if value != "Not sure":
        st.session_state.inferred_hints[attr] = value
        st.session_state.candidate_photos = filter_by_hints(
            st.session_state.candidate_photos, {attr: value}
        )
    st.session_state.asked_questions.append(attr)

def on_success_click(photo_id):
    if st.session_state.start_time:
        seconds = time.time() - st.session_state.start_time
    else:
        seconds = 0
        
    new_row = {
        "query": st.session_state.current_query,
        "mode": st.session_state.search_mode,
        "questions_answered": len(st.session_state.asked_questions),
        "seconds_to_success": round(seconds, 2),
        "photo_id": photo_id,
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    st.session_state.log_data = pd.concat([st.session_state.log_data, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.success_message = f"✅ Success! You found {photo_id} in {round(seconds, 2)} seconds."
    st.session_state.start_time = None  # prevent duplicate logging on double clicks

def baseline_search(query, library):
    """
    Splits query into lowercase tokens.
    Returns photos where the objective list contains ALL tokens.
    """
    tokens = set(query.lower().split())
    if not tokens:
        return library
        
    results = []
    for photo in library:
        # Check if all tokens match something in the objective tags (substring match allowed)
        match = True
        for token in tokens:
            if not any(token in obj for obj in photo['objective']):
                match = False
                break
        if match:
            results.append(photo)
    return results

def render_photo_grid(photos):
    """
    Renders a 6-column photo grid. Caps at 18 photos.
    """
    if not photos:
        st.warning("No photos found.")
        return
        
    display_photos = photos[:18]
    
    cols = st.columns(6)
    for idx, photo in enumerate(display_photos):
        col = cols[idx % 6]
        with col:
            color = photo['palette']
            emoji = SCENE_EMOJIS.get(photo['scene'], "📷")
            st.markdown(
                f'''
                <div style="background-color: {color}; width: 100%; aspect-ratio: 1; 
                            display: flex; align-items: center; justify-content: center; 
                            border-radius: 8px; font-size: 2rem; color: white; margin-bottom: 10px;">
                    {emoji}
                </div>
                ''', unsafe_allow_html=True
            )
            st.caption(f"**{photo['id']}**")
            st.button("✅ This is it", key=f"btn_success_{photo['id']}", on_click=on_success_click, args=(photo['id'],))
            
    if len(photos) > 18:
        st.info(f"+ {len(photos) - 18} more")

import time

def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()

def main():
    init_session_state()
    
    # Sidebar UI
    with st.sidebar:
        st.header("Settings")
        mode = st.radio(
            "Search Mode", 
            ["Current search (baseline)", "With Contextual Disambiguation"], 
            index=0 if st.session_state.search_mode == "Current search (baseline)" else 1
        )
        
        # Mode Switching Retention: If toggled, re-process with existing query.
        if mode != st.session_state.search_mode:
            st.session_state.search_mode = mode
            if mode == "With Contextual Disambiguation" and st.session_state.current_query:
                st.session_state.asked_questions = []
                initial_hints = parse_hints(st.session_state.current_query)
                candidates, final_hints = apply_constraint_relaxation(st.session_state.mock_library, initial_hints)
                st.session_state.inferred_hints = final_hints
                st.session_state.candidate_photos = candidates
            st.rerun()
            
        if st.button("Reset session"):
            reset_session()
            st.rerun()
            
        if not st.session_state.log_data.empty:
            st.divider()
            csv = st.session_state.log_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV Logs",
                data=csv,
                file_name='disambiguation_logs.csv',
                mime='text/csv',
            )
            
    st.title("Progressive Contextual Disambiguation MVP")
    
    # Search Input UI (Decoupled Logic using st.form)
    with st.form(key="search_form"):
        query = st.text_input("Search your photos", value=st.session_state.current_query)
        submit_search = st.form_submit_button("Search")
        
    if submit_search:
        st.session_state.current_query = query
        st.session_state.search_submitted = True
        st.session_state.success_message = None
        
        # Phase 5: New Search Reset (Clears answers, asked list, and restarts timer)
        st.session_state.asked_questions = []
        st.session_state.start_time = time.time()
        
        if st.session_state.search_mode == "With Contextual Disambiguation":
            initial_hints = parse_hints(query)
            candidates, final_hints = apply_constraint_relaxation(st.session_state.mock_library, initial_hints)
            st.session_state.inferred_hints = final_hints
            st.session_state.candidate_photos = candidates
        else:
            st.session_state.inferred_hints = {}
            st.session_state.candidate_photos = st.session_state.mock_library
        
    # Main Canvas Display
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        
    if st.session_state.search_submitted and st.session_state.current_query:
        if st.session_state.search_mode == "Current search (baseline)":
            st.subheader(f"Baseline Results for: '{st.session_state.current_query}'")
            results = baseline_search(st.session_state.current_query, st.session_state.mock_library)
            render_photo_grid(results)
        else:
            st.subheader(f"Disambiguation Results for: '{st.session_state.current_query}'")
            
            # Show parsed hints via chat bubble if any
            if st.session_state.inferred_hints:
                hints_text = ", ".join([f"{k}: {v}" for k, v in st.session_state.inferred_hints.items()])
                st.info(f"🗨️ I understood {hints_text}. That leaves {len(st.session_state.candidate_photos)} possible photos.")
            else:
                st.info(f"🗨️ I didn't catch any specific filters. That leaves {len(st.session_state.candidate_photos)} possible photos.")
                
            best_attr, entropy = calculate_shannon_entropy(
                st.session_state.candidate_photos, 
                st.session_state.asked_questions, 
                st.session_state.inferred_hints
            )
            
            # Phase 5: Implementing Stop Conditions
            stop_condition_met = False
            if len(st.session_state.candidate_photos) <= 6:
                stop_condition_met = True
            elif len(st.session_state.asked_questions) >= 3:
                stop_condition_met = True
            elif not best_attr or entropy == 0:
                stop_condition_met = True
                
            if stop_condition_met:
                st.success("Disambiguation complete!")
                render_photo_grid(st.session_state.candidate_photos)
            else:
                question = QUESTION_MAP.get(best_attr, f"What about the {best_attr}?")
                st.markdown(f"**{question}**")
                st.caption(f"Asking so I can narrow down {len(st.session_state.candidate_photos)} photos. Tap Not sure to skip.")
                
                counts = Counter([p.get(best_attr) for p in st.session_state.candidate_photos])
                top_values = [item[0] for item in counts.most_common(4)]
                
                cols = st.columns(len(top_values) + 1)
                for idx, val in enumerate(top_values):
                    with cols[idx]:
                        # Never-Zero Rule is fulfilled by taking from `counts` of `candidate_photos`
                        st.button(str(val), key=f"chip_{best_attr}_{val}_{len(st.session_state.asked_questions)}", on_click=on_chip_click, args=(best_attr, val))
                
                with cols[-1]:
                    st.button("Not sure", key=f"chip_{best_attr}_notsure_{len(st.session_state.asked_questions)}", on_click=on_chip_click, args=(best_attr, "Not sure"))
                
                st.write("---")
                render_photo_grid(st.session_state.candidate_photos)
    else:
        st.info("Enter a query and click 'Search' to begin.")

if __name__ == "__main__":
    main()
