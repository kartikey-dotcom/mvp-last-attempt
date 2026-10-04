import streamlit as st
import pandas as pd
import random
import math
from collections import Counter
import time

# Phase 1: Environment Setup & Data Model

# Set up basic Streamlit page config
st.set_page_config(page_title="Progressive Contextual Disambiguation", layout="wide", initial_sidebar_state="collapsed")

# Inject High-Fidelity UI Styling
st.markdown("""
<style>
/* 1. Mobile App Container Simulation */
.stApp {
    background-color: #EFEFEF;
}
.block-container {
    max-width: 450px !important;
    padding-top: 1rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    padding-bottom: 0rem !important;
    margin: 0 auto !important;
    background-color: white;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.1);
    min-height: 100vh;
}
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Custom Search Bar adjustments */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 16px !important;
    background-color: white;
    margin-bottom: 0px !important;
}

/* 2. The Assistant Card */
.assistant-card-top {
    background-color: #F0F4F9;
    border-radius: 24px 24px 0 0;
    padding: 24px 20px 8px 20px;
    margin: 16px 16px 0 16px;
}
.assistant-header {
    font-size: 11px;
    font-weight: 600;
    color: #444746;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.assistant-context {
    font-size: 14px;
    color: #444746;
    margin-bottom: 16px;
    line-height: 1.5;
}
.assistant-question {
    font-size: 24px;
    font-weight: 400;
    color: #1F1F1F;
    margin-bottom: 8px;
}
.assistant-caption {
    font-size: 13px;
    color: #76777A;
    margin-bottom: 0px;
}

div[data-testid="stHorizontalBlock"]:has(.chip-container-marker) {
    background-color: #F0F4F9;
    border-radius: 0 0 24px 24px;
    padding: 8px 20px 24px 20px;
    margin: 0px 16px 24px 16px;
    width: auto !important;
    gap: 8px !important;
}

/* 3. Interaction Chips */
div[data-testid="stHorizontalBlock"]:has(.chip-container-marker) div[data-testid="stButton"] button {
    border-radius: 999px !important;
    border: 1px solid #727775 !important;
    background-color: transparent !important;
    color: #1F1F1F !important;
    padding: 4px 16px !important;
    font-weight: 500 !important;
    min-height: 32px !important;
}
div[data-testid="stHorizontalBlock"]:has(.chip-container-marker) div[data-testid="stButton"] button:hover {
    background-color: #E8DEF8 !important;
    border-color: #1F1F1F !important;
}

/* 4. The Photo Grid */
div[data-testid="stHorizontalBlock"]:has(.photo-grid-marker) {
    gap: 0px !important;
    padding: 0 !important;
    margin: 0 !important;
}
div[data-testid="stHorizontalBlock"]:has(.photo-grid-marker) div[data-testid="column"] {
    padding: 0 !important;
    gap: 0 !important;
}

.timeline-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 16px 8px 16px;
}
.timeline-date {
    font-size: 15px;
    font-weight: 500;
    color: #1F1F1F;
}
.timeline-count {
    font-size: 13px;
    color: #76777A;
}

div[data-testid="stHorizontalBlock"]:has(.photo-grid-marker) div[data-testid="stButton"] button {
    border-radius: 0px !important;
    border: none !important;
    background-color: #F8F9FA !important;
    color: #1F1F1F !important;
    padding: 4px !important;
    font-size: 12px !important;
    margin: 0 !important;
}
div[data-testid="stHorizontalBlock"]:has(.photo-grid-marker) div[data-testid="stButton"] button:hover {
    background-color: #E0E0E0 !important;
}

/* 5. Bottom Navigation Bar */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 450px;
    height: 80px;
    background-color: white;
    border-top: 1px solid #E0E0E0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    z-index: 9999;
}
.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 500;
    color: #444746;
    width: 64px;
}
.nav-icon-container {
    width: 64px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
}
.nav-item.active .nav-icon-container {
    background-color: #C2E7FF;
}
.nav-item.active {
    color: #001D35;
}
.nav-icon {
    font-size: 20px;
}

.bottom-spacer {
    height: 100px;
}
</style>
""", unsafe_allow_html=True)


def generate_mock_library(seed=11):
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
        
        if i < 10:
            palette = "purple"
            time_of_day = "sunset"
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
        
        objective = [
            scene, people, weather, time_of_day, season, palette, occasion, activity
        ]
        
        if scene == "beach":
            objective.extend(["sea", "sand", "sky"])
        elif scene == "city":
            objective.extend(["buildings", "streets", "urban"])
        elif scene == "mountain":
            objective.extend(["hills", "nature", "trek"])
            
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
            "objective": list(set(objective))
        }
        library.append(photo)
        
    return library

def init_session_state():
    if "mock_library" not in st.session_state:
        st.session_state.mock_library = generate_mock_library()
    if "search_mode" not in st.session_state:
        st.session_state.search_mode = "With Contextual Disambiguation"
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
    st.session_state.start_time = None

def baseline_search(query, library):
    tokens = set(query.lower().split())
    if not tokens:
        return library
    results = []
    for photo in library:
        match = True
        for token in tokens:
            if not any(token in obj for obj in photo['objective']):
                match = False
                break
        if match:
            results.append(photo)
    return results

def render_photo_grid(photos):
    if not photos:
        st.warning("No photos found.")
        return
        
    display_photos = photos[:18]
    
    # Timeline Header
    st.markdown(f'''
        <div class="timeline-header">
            <div class="timeline-date">Sun, 22 Sep</div>
            <div class="timeline-count">{len(photos)} photos</div>
        </div>
    ''', unsafe_allow_html=True)
    
    cols = st.columns(3)
    with cols[0]:
        # Inject marker to strip column gaps
        st.markdown('<span class="photo-grid-marker"></span>', unsafe_allow_html=True)
        
    for idx, photo in enumerate(display_photos):
        col = cols[idx % 3]
        with col:
            color = photo['palette']
            emoji = SCENE_EMOJIS.get(photo['scene'], "📷")
            st.markdown(
                f'''
                <div style="background-color: {color}; width: 100%; aspect-ratio: 1; 
                            display: flex; align-items: center; justify-content: center; 
                            font-size: 2rem; color: white; border: 1px solid white;">
                    {emoji}
                </div>
                ''', unsafe_allow_html=True
            )
            st.button("✅ This is it", key=f"btn_success_{photo['id']}", on_click=on_success_click, args=(photo['id'],), use_container_width=True)
            
    if len(photos) > 18:
        st.markdown(f'<div style="text-align: center; color: #76777A; padding: 16px;">+ {len(photos) - 18} more</div>', unsafe_allow_html=True)


def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()

def main():
    init_session_state()
    
    with st.sidebar:
        st.header("Settings")
        mode = st.radio(
            "Search Mode", 
            ["Current search (baseline)", "With Contextual Disambiguation"], 
            index=0 if st.session_state.search_mode == "Current search (baseline)" else 1
        )
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
            
    # Search Input
    with st.form(key="search_form"):
        query = st.text_input("Search", value=st.session_state.current_query, label_visibility="collapsed", placeholder="Search your photos")
        submit_search = st.form_submit_button("🔍 Search")
        
    if submit_search:
        st.session_state.current_query = query
        st.session_state.search_submitted = True
        st.session_state.success_message = None
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
        
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        
    if st.session_state.search_submitted and st.session_state.current_query:
        if st.session_state.search_mode == "Current search (baseline)":
            render_photo_grid(baseline_search(st.session_state.current_query, st.session_state.mock_library))
        else:
            best_attr, entropy = calculate_shannon_entropy(
                st.session_state.candidate_photos, 
                st.session_state.asked_questions, 
                st.session_state.inferred_hints
            )
            
            stop_condition_met = False
            if len(st.session_state.candidate_photos) <= 6:
                stop_condition_met = True
            elif len(st.session_state.asked_questions) >= 3:
                stop_condition_met = True
            elif not best_attr or entropy == 0:
                stop_condition_met = True
                
            if stop_condition_met:
                render_photo_grid(st.session_state.candidate_photos)
            else:
                if st.session_state.inferred_hints:
                    parts = []
                    for k, v in st.session_state.inferred_hints.items():
                        parts.append(f"<b>{k}: {v}</b>")
                    understood_html = f"I understood {', '.join(parts)}. That leaves <b>{len(st.session_state.candidate_photos)}</b> possible photos."
                else:
                    understood_html = f"I didn't catch any specific filters. That leaves <b>{len(st.session_state.candidate_photos)}</b> possible photos."

                question = QUESTION_MAP.get(best_attr, f"What about the {best_attr}?")
                
                # Render the top part of the Assistant Card
                st.markdown(f'''
                <div class="assistant-card-top">
                    <div class="assistant-header">✨ ASSISTANT</div>
                    <div class="assistant-context">{understood_html}</div>
                    <div class="assistant-question">{question}</div>
                    <div class="assistant-caption">Asking to narrow down the results. Tap 'Not sure' to skip.</div>
                </div>
                ''', unsafe_allow_html=True)
                
                counts = Counter([p.get(best_attr) for p in st.session_state.candidate_photos])
                top_values = [item[0] for item in counts.most_common(4)]
                
                cols = st.columns(len(top_values) + 1)
                with cols[0]:
                    # Inject marker to link this block's CSS
                    st.markdown('<span class="chip-container-marker"></span>', unsafe_allow_html=True)
                    st.button(f"{str(top_values[0]).capitalize()} ({counts[top_values[0]]})", key=f"chip_{best_attr}_{top_values[0]}_{len(st.session_state.asked_questions)}", on_click=on_chip_click, args=(best_attr, top_values[0]))
                
                for idx in range(1, len(top_values)):
                    val = top_values[idx]
                    with cols[idx]:
                        st.button(f"{str(val).capitalize()} ({counts[val]})", key=f"chip_{best_attr}_{val}_{len(st.session_state.asked_questions)}", on_click=on_chip_click, args=(best_attr, val))
                
                with cols[-1]:
                    st.button("Not sure", key=f"chip_{best_attr}_notsure_{len(st.session_state.asked_questions)}", on_click=on_chip_click, args=(best_attr, "Not sure"))
                
                render_photo_grid(st.session_state.candidate_photos)

    # Render Bottom Navigation Bar
    st.markdown("""
    <div class="bottom-spacer"></div>
    <div class="bottom-nav">
        <div class="nav-item">
            <div class="nav-icon-container"><span class="nav-icon">🖼️</span></div>
            <span>Photos</span>
        </div>
        <div class="nav-item active">
            <div class="nav-icon-container"><span class="nav-icon">🔍</span></div>
            <span>Search</span>
        </div>
        <div class="nav-item">
            <div class="nav-icon-container"><span class="nav-icon">👥</span></div>
            <span>Sharing</span>
        </div>
        <div class="nav-item">
            <div class="nav-icon-container"><span class="nav-icon">📁</span></div>
            <span>Library</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
