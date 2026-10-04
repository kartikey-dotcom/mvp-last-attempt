import os

app_code = r'''import streamlit as st
import pandas as pd
import random
import math
import time
from collections import Counter
import base64
import os
import json

# Setup
st.set_page_config(layout="wide", page_title="Photos concept: Contextual Disambiguation", initial_sidebar_state="collapsed")

# -----------------
# DATA MODEL
# -----------------
SCENES = ["beach", "city", "mountain", "home", "restaurant", "wedding"]
PEOPLE = ["Rohan", "Mom", "Ananya", "alone"]
WEATHER = ["sunny", "rainy", "cloudy", "foggy"]
TIME_OF_DAY = ["morning", "afternoon", "sunset", "night"]
SEASON = ["summer", "monsoon", "winter"]
PALETTE = ["purple", "orange", "blue", "green", "red", "grey"]
OCCASION = ["none", "none", "trip", "birthday", "wedding"]
ACTIVITY = ["walking", "driving", "scooter ride", "shopping", "relaxing"]

def get_objective(scene, people):
    tags = []
    if scene == "beach": tags.extend(["beach", "sea", "sand", "sky"])
    elif scene == "city": tags.extend(["city", "building", "street", "sky"])
    elif scene == "mountain": tags.extend(["mountain", "hill", "tree", "sky"])
    elif scene == "home": tags.extend(["home", "room", "sofa"])
    elif scene == "restaurant": tags.extend(["restaurant", "food", "table"])
    elif scene == "wedding": tags.extend(["wedding", "stage", "crowd"])
    if people != "alone": tags.append("person")
    return tags

@st.cache_data
def get_mock_library():
    rng = random.Random(11)
    library = []
    
    # 0 to 12 must be the demo seed (13 photos total)
    demo_scenes = ["beach", "city", "mountain", "beach", "city", "mountain", "home", "beach", "city", "mountain", "home", "beach", "beach"]
    
    for i in range(72):
        photo_id = f"IMG_{1000 + i}"
        
        if i < 13:
            scene = demo_scenes[i]
            palette = "purple"
            time_of_day = "sunset"
            people = rng.choice(PEOPLE)
            weather = rng.choice(WEATHER)
            season = rng.choice(SEASON)
            occasion = rng.choice(OCCASION)
            activity = rng.choice(ACTIVITY)
        else:
            scene = rng.choice(SCENES)
            people = rng.choice(PEOPLE)
            weather = rng.choice(WEATHER)
            time_of_day = rng.choice(TIME_OF_DAY)
            season = rng.choice(SEASON)
            palette = rng.choice(PALETTE)
            occasion = rng.choice(OCCASION)
            activity = rng.choice(ACTIVITY)
            
            if palette == "purple" and time_of_day == "sunset":
                time_of_day = rng.choice([t for t in TIME_OF_DAY if t != "sunset"])
                
        library.append({
            "id": photo_id,
            "scene": scene,
            "people": people,
            "weather": weather,
            "time_of_day": time_of_day,
            "season": season,
            "palette": palette,
            "occasion": occasion,
            "activity": activity,
            "objective": get_objective(scene, people)
        })
    return library

library = get_mock_library()

# -----------------
# STATE INIT
# -----------------
if "query" not in st.session_state: st.session_state.query = ""
if "mode" not in st.session_state: st.session_state.mode = "Current search"
if "answers" not in st.session_state: st.session_state.answers = {}
if "asked" not in st.session_state: st.session_state.asked = []
if "selected" not in st.session_state: st.session_state.selected = set()
if "start_time" not in st.session_state: st.session_state.start_time = None
if "log_data" not in st.session_state: st.session_state.log_data = []
if "success_msg" not in st.session_state: st.session_state.success_msg = None

def reset_search():
    st.session_state.query = ""
    st.session_state.answers = {}
    st.session_state.asked = []
    st.session_state.selected = set()
    st.session_state.start_time = None
    st.session_state.success_msg = None

def do_search():
    if st.session_state.q_input:
        st.session_state.query = st.session_state.q_input
    st.session_state.answers = {}
    st.session_state.asked = []
    st.session_state.selected = set()
    st.session_state.start_time = time.time()
    st.session_state.success_msg = None

def toggle_select(photo_id):
    if photo_id in st.session_state.selected:
        st.session_state.selected.remove(photo_id)
    else:
        st.session_state.selected.add(photo_id)

def clear_selection():
    st.session_state.selected = set()

def commit_selection():
    if not st.session_state.selected: return
    end_time = time.time()
    elapsed = round(end_time - st.session_state.start_time, 1) if st.session_state.start_time else 0.0
    questions_answered = len([k for k, v in st.session_state.answers.items() if v is not None])
    
    first_id = list(st.session_state.selected)[0]
    
    for photo_id in st.session_state.selected:
        st.session_state.log_data.append({
            "query": st.session_state.query,
            "mode": st.session_state.mode,
            "questions_answered": questions_answered,
            "seconds_to_success": elapsed,
            "photo_id": photo_id,
            "timestamp": time.strftime("%H:%M:%S")
        })
    
    st.session_state.success_msg = f"Found {first_id} in {elapsed}s with {questions_answered} clarifying question(s)."
    clear_selection()

def answer_q(attr, value):
    st.session_state.answers[attr] = value
    if attr not in st.session_state.asked:
        st.session_state.asked.append(attr)

def remove_answer(attr):
    if attr in st.session_state.answers:
        del st.session_state.answers[attr]
    if attr in st.session_state.asked:
        st.session_state.asked.remove(attr)

# -----------------
# CSS INJECTION
# -----------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto:wght@400;500;700&display=swap');

header[data-testid="stHeader"], 
[data-testid="stToolbar"], 
[data-testid="stSidebar"], 
[data-testid="stSidebarCollapsedControl"], 
footer, 
#MainMenu {
    display: none !important;
}

.stApp {
    background-color: #FFFFFF !important;
    font-family: 'Google Sans', 'Google Sans Text', Roboto, Inter, system-ui, sans-serif !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Header */
.st-key-top_header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background: #FFFFFF;
    border-bottom: 1px solid #E0E0E0;
    z-index: 100;
    display: flex;
    align-items: center;
}

.header-inner {
    display: flex;
    width: 100%;
    align-items: center;
    padding: 0 16px;
    justify-content: space-between;
}

.header-left, .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
}

.header-logo-text {
    font-size: 22px;
    font-weight: 400;
    color: #202124;
    margin-left: 8px;
}

.concept-pill {
    background: #F1F3F4;
    color: #5F6368;
    font-size: 11px;
    border-radius: 9999px;
    padding: 2px 8px;
    margin-left: 8px;
}

.avatar {
    width: 32px;
    height: 32px;
    background: #7C3AED;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 500;
}

/* Left Nav */
.st-key-left_nav {
    position: fixed;
    top: 64px;
    bottom: 0;
    left: 0;
    width: 256px;
    background: #FFFFFF;
    border-right: 1px solid #E0E0E0;
    padding: 8px;
    z-index: 90;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 16px;
    height: 48px;
    padding: 0 16px;
    border-radius: 9999px;
    color: #202124;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
}
.nav-item:hover {
    background: #F1F3F4;
}
.nav-item.active {
    background: #D3E3FD;
    color: #041E49;
}
.nav-item.active svg {
    fill: #041E49;
}
.nav-item svg {
    fill: #5F6368;
}

/* Main Content Area */
.st-key-main_content {
    margin-left: 256px;
    margin-top: 64px;
    padding: 24px 32px 96px;
}

@media (max-width: 900px) {
    .st-key-left_nav { display: none; }
    .st-key-main_content { margin-left: 0; }
}

/* Search Bar */
.st-key-topbar {
    position: fixed;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: min(720px, 50vw);
    z-index: 101;
}

.st-key-search_form [data-testid="stForm"] {
    background: #E9EEF6 !important;
    border: none !important;
    border-radius: 9999px !important;
    height: 48px !important;
    padding: 0 8px !important;
    display: flex !important;
    align-items: center !important;
    flex-direction: row !important;
}

.st-key-q_input {
    flex-grow: 1 !important;
}
.st-key-q_input [data-testid="stTextInputRootElement"] {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
}
.st-key-q_input input {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 16px !important;
    color: #202124 !important;
}

.st-key-search_form [data-testid="stFormSubmitButton"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #5F6368 !important;
}
.st-key-search_form [data-testid="stFormSubmitButton"] button:hover {
    background: #DDE3EC !important;
}

.st-key-search_btn button {
    opacity: 0 !important;
    width: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Prototype controls */
.st-key-proto {
    position: absolute;
    bottom: 40px;
    left: 8px;
    width: 240px;
}

/* Assistant card */
.st-key-assistant {
    background: #EEF2F9;
    border-radius: 24px;
    padding: 20px 24px;
    margin-bottom: 24px;
    max-width: 100%;
}
.st-key-assistant [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* Chips */
div[class*="st-key-chip_"] button {
    height: 40px !important;
    padding: 0 20px !important;
    border-radius: 9999px !important;
    border: 1px solid #747775 !important;
    background: transparent !important;
    color: #1F1F1F !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
div[class*="st-key-chip_"] button:hover {
    background: rgba(31,31,31,0.08) !important;
    border-color: #747775 !important;
    color: #1F1F1F !important;
}
div[class*="st-key-chip_"]:active button {
    background: #D3E3FD !important;
}
div[class*="st-key-chip_not_sure"] button {
    border-style: dashed !important;
}

/* Applied filters */
div[class*="st-key-applied_"] button {
    background: #D3E3FD !important;
    color: #041E49 !important;
    height: 32px !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0 12px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
div[class*="st-key-applied_"] button:hover {
    background: #C2D7FA !important;
}

/* Photo Grid */
.st-key-photo_grid [data-testid="stVerticalBlock"] {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)) !important;
    gap: 8px !important;
}
div[class*="st-key-tile_"] {
    width: auto !important;
}

/* Action Bar */
.st-key-actionbar {
    position: fixed;
    top: 64px;
    left: 256px;
    right: 0;
    height: 64px;
    background: #EEF2F9;
    z-index: 90;
    padding: 0 32px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #E0E0E0;
}
@media (max-width: 900px) {
    .st-key-actionbar { left: 0; }
}
.st-key-commit_btn button {
    background: #1A73E8 !important;
    color: white !important;
    border-radius: 9999px !important;
    height: 40px !important;
    padding: 0 24px !important;
    border: none !important;
    font-weight: 500 !important;
}
.st-key-commit_btn button:hover {
    background: #1967D2 !important;
}

/* Hidden elements */
.hide { display: none !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------
# ICONS & SVGS
# -----------------
def svg_icon(path, color="#5F6368", size=24):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="{path}"/></svg>'

MENU_ICON = "M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"
SEARCH_ICON = "M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
CLEAR_ICON = "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
HELP_ICON = "M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"
SETTINGS_ICON = "M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.06-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.73,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.06,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 C9.64,21.83,9.83,22,10.08,22h3.84c0.24,0,0.43-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.49-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"
APPS_ICON = "M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z"
SPARKLE_SVG = '<svg width="20" height="20" viewBox="0 0 24 24"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1A73E8"/><stop offset="100%" stop-color="#8E24AA"/></linearGradient></defs><path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4L12 2z" fill="url(#g)"/></svg>'

# -----------------
# HEADER & SHELL
# -----------------
with st.container(key="top_header"):
    st.markdown(f'''
    <div class="header-inner">
        <div class="header-left">
            {svg_icon(MENU_ICON)}
            <span class="header-logo-text">Photos</span>
            <span class="concept-pill">Concept</span>
        </div>
        <div class="header-right">
            {svg_icon(HELP_ICON)}
            {svg_icon(SETTINGS_ICON)}
            {svg_icon(APPS_ICON)}
            <div class="avatar">A</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with st.container(key="topbar"):
    with st.form(key="search_form", clear_on_submit=False):
        c1, c2, c3 = st.columns([1, 10, 1])
        with c1:
            st.form_submit_button(label="🔍", help="Search")
        with c2:
            st.text_input("Search", key="q_input", label_visibility="collapsed", placeholder="Search your photos")
        with c3:
            if st.form_submit_button(label="✕", help="Clear"):
                reset_search()
                st.rerun()
        
        st.form_submit_button(label="submit", on_click=do_search)

st.markdown('<style>.st-key-search_form [data-testid="column"] {width: auto !important; min-width: 0 !important;}</style>', unsafe_allow_html=True)

with st.container(key="left_nav"):
    st.markdown(f'''
    <a href="#" class="nav-item" title="Not part of this prototype">{svg_icon("M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z")} Photos</a>
    <a href="#" class="nav-item active">{svg_icon(SEARCH_ICON, "#041E49")} Explore</a>
    <a href="#" class="nav-item" title="Not part of this prototype">{svg_icon("M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z")} Sharing</a>
    <a href="#" class="nav-item" title="Not part of this prototype">{svg_icon("M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-8 12.5v-9l6 4.5-6 4.5z")} Library</a>
    <a href="#" class="nav-item" title="Not part of this prototype">{svg_icon("M13.83 4.83l-1.42-1.42L11 4.83 13.83 7.66l1.41-1.41-1.41-1.42zM12 2c-5.52 0-10 4.48-10 10s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z")} Utilities</a>
    ''', unsafe_allow_html=True)
    
    with st.container(key="proto"):
        st.markdown('<div style="font-size: 11px; color: #5F6368; margin-bottom: 8px;">Try an example</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        def ex_search(q):
            st.session_state.query = q
            st.session_state.q_input = q
            st.session_state.answers = {}
            st.session_state.asked = []
            st.session_state.selected = set()
            st.session_state.start_time = time.time()
            st.session_state.success_msg = None
        
        with col1: st.button("purple sunset", key="ex_1", on_click=ex_search, args=("purple sunset",))
        with col2: st.button("rainy wedding", key="ex_2", on_click=ex_search, args=("rainy wedding",))
        with col3: st.button("foggy mountain", key="ex_3", on_click=ex_search, args=("foggy mountain",))
        
        st.markdown('<div style="font-size: 11px; color: #5F6368; margin-top: 16px;">Prototype mode</div>', unsafe_allow_html=True)
        st.radio("mode", ["Current search", "With Contextual Disambiguation"], key="mode", label_visibility="collapsed")
        
        st.markdown('<div style="position: fixed; bottom: 8px; right: 16px; font-size: 11px; color: #5F6368; z-index: 1000;">Concept prototype for a PM case study. Not affiliated with or endorsed by Google. All photos and data are simulated.</div>', unsafe_allow_html=True)

# -----------------
# SEARCH LOGIC
# -----------------
def get_hints(query):
    query = query.lower()
    hints = {}
    synonyms = {
        "dusk": "sunset", "evening": "sunset",
        "violet": "purple", "pink": "purple",
        "rain": "rainy", "raining": "rainy",
        "fog": "foggy",
        "sea": "beach", "ocean": "beach",
        "hills": "mountain"
    }
    
    vocab = {
        "weather": WEATHER,
        "time_of_day": TIME_OF_DAY,
        "season": SEASON,
        "palette": PALETTE,
        "scene": SCENES,
        "occasion": OCCASION,
        "activity": ACTIVITY,
        "people": PEOPLE
    }
    
    tokens = query.split()
    for attr, values in vocab.items():
        for val in values:
            if val == "none" or val == "alone": continue
            if val in tokens or (val in synonyms and synonyms[val] in tokens):
                hints[attr] = val
                break
        
        for k, v in synonyms.items():
            if k in tokens and v in values:
                if attr not in hints: hints[attr] = v
                
    return hints

def get_candidates(library, query, mode):
    if not query: return library
    
    if mode == "Current search":
        tokens = query.lower().split()
        return [p for p in library if all(t in p["objective"] for t in tokens)], {}, []
    
    # AI Mode
    hints = get_hints(query)
    
    for k, v in st.session_state.answers.items():
        if v is not None:
            hints[k] = v
        elif k in hints:
            del hints[k]
    
    def filter_lib(lib, h):
        return [p for p in lib if all(p.get(k) == v for k, v in h.items())]
    
    drop_order = ["season", "activity", "occasion", "time_of_day", "scene", "palette", "people", "weather"]
    current_hints = hints.copy()
    dropped = []
    
    res = filter_lib(library, current_hints)
    while len(res) == 0 and current_hints:
        for attr in drop_order:
            if attr in current_hints and attr not in st.session_state.answers:
                dropped.append(attr)
                del current_hints[attr]
                break
        else:
            break
        res = filter_lib(library, current_hints)
        
    return res, current_hints, dropped

def calculate_entropy(candidates, unasked_attrs):
    best_attr = None
    max_e = 0
    total = len(candidates)
    if total == 0: return None, 0
    
    for attr in unasked_attrs:
        counts = Counter(p[attr] for p in candidates)
        e = sum(-(count/total) * math.log2(count/total) for count in counts.values())
        if e > max_e:
            max_e = e
            best_attr = attr
    return best_attr, max_e

# -----------------
# UI COMPONENTS
# -----------------
with st.container(key="main_content"):
    if st.session_state.selected:
        with st.container(key="actionbar"):
            c1, c2, c3 = st.columns([1, 8, 2])
            with c1:
                st.button("✕", key="btn_clear_sel", on_click=clear_selection)
            with c2:
                st.markdown(f'<div style="font-size: 16px; font-weight: 500;">{len(st.session_state.selected)} selected</div>', unsafe_allow_html=True)
            with c3:
                st.button("✅ This is it", key="btn_commit", on_click=commit_selection)
                st.markdown('<style>.st-key-btn_commit {float: right;}</style>', unsafe_allow_html=True)

    if st.session_state.success_msg:
        st.markdown(f\'\'\'
        <div style="background: #E6F4EA; color: #137333; padding: 12px 16px; border-radius: 12px; margin-bottom: 24px; display: flex; align-items: center; gap: 8px;">
            {svg_icon("M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z", "#137333")}
            {st.session_state.success_msg}
        </div>
        \'\'\', unsafe_allow_html=True)

    q = st.session_state.query
    if not q:
        st.markdown(\'\'\'
        <div style="text-align: center; margin-top: 120px;">
            <div style="font-size: 22px; color: #202124;">Search your photos</div>
            <div style="font-size: 14px; color: #5F6368; margin-top: 8px;">Try an example from the bottom left, or type your own search.</div>
        </div>
        \'\'\', unsafe_allow_html=True)
    else:
        candidates, current_hints, dropped = get_candidates(library, q, st.session_state.mode)
        
        if st.session_state.mode == "Current search":
            if not candidates:
                st.markdown(f\'\'\'
                <div style="text-align: center; margin-top: 96px;">
                    {svg_icon("M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z", "#9AA0A6", 64)}
                    <div style="font-size: 22px; color: #202124; margin-top: 16px;">No results for "{q}"</div>
                    <div style="font-size: 14px; color: #5F6368; margin-top: 8px;">Try different keywords</div>
                </div>
                \'\'\', unsafe_allow_html=True)
            else:
                st.markdown(f\'\'\'
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px;">
                    <div><span style="font-size: 16px; font-weight: 500; color: #202124;">Sun, 22 Sep</span> <span style="font-size: 12px; color: #5F6368; margin-left: 12px;">{len(candidates)} items</span></div>
                    <div style="font-size: 12px; color: #5F6368;">Select photos to review or share</div>
                </div>
                \'\'\', unsafe_allow_html=True)
                
                with st.container(key="photo_grid"):
                    for p in candidates[:24]:
                        with st.container(key=f"tile_{p['id']}"):
                            bg = p['palette'] if p['palette'] != 'purple' else 'rebeccapurple'
                            svg = f'<svg viewBox="0 0 100 100" preserveAspectRatio="slice"><rect width="100" height="100" fill="{bg}" opacity="0.3"/><circle cx="50" cy="50" r="20" fill="white" opacity="0.5"/></svg>'
                            is_sel = p['id'] in st.session_state.selected
                            sel_html = f\'\'\'
                            <div style="position:relative; width:100%; aspect-ratio:1/1; border-radius:4px; overflow:hidden; background:#F1F3F4; transition: 0.15s;
                                        {f'box-shadow: 0 0 0 3px #1A73E8; padding: 12px; background: #E8F0FE;' if is_sel else ''}">
                                <div style="position:relative; width:100%; height:100%; border-radius:{'8px' if is_sel else '0'}; overflow:hidden;">
                                    <div style="width:100%; height:100%; background-image:url('data:image/svg+xml;utf8,{svg}'); background-size:cover;"></div>
                                </div>
                                <div style="position:absolute; top:8px; left:8px; width:24px; height:24px; border-radius:50%; 
                                            border: 2px solid white; background: {'#1A73E8' if is_sel else 'rgba(0,0,0,0.25)'}; 
                                            display: flex; align-items: center; justify-content: center; z-index: 5;
                                            {'opacity: 0;' if not is_sel else ''}">
                                    {svg_icon("M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z", "white", 16) if is_sel else ""}
                                </div>
                            </div>
                            \'\'\'
                            st.markdown(sel_html, unsafe_allow_html=True)
                            st.markdown(f'<style>.st-key-sel_{p["id"]} button {{ position: absolute; top:0; left:0; width:100%; height:100%; opacity:0; z-index:10; cursor: pointer; }}</style>', unsafe_allow_html=True)
                            st.button(" ", key=f"sel_{p['id']}", on_click=toggle_select, args=(p['id'],))
                    if len(candidates) > 24:
                        st.caption(f"+ {len(candidates)-24} more")
                        
        else:
            with st.container(key="assistant"):
                st.markdown(f\'\'\'
                <div style="display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 700; color: #444746; letter-spacing: 0.5px;">
                    {SPARKLE_SVG} ASSISTANT
                </div>
                \'\'\', unsafe_allow_html=True)
                
                if not current_hints:
                    understood = "I couldn't pin anything down yet. **{}** photos to go through.".format(len(candidates))
                else:
                    parts = []
                    for k, v in current_hints.items():
                        parts.append(f"**{k.replace('_', ' ')}: {v}**")
                    understood = f"I understood {', '.join(parts)}. That leaves **{len(candidates)}** possible photos."
                    
                st.markdown(f'<div style="font-size: 14px; color: #5F6368; margin-top: 8px;">{understood}</div>', unsafe_allow_html=True)
                
                if dropped:
                    st.markdown(f'<div style="font-size: 12px; color: #D93025; margin-top: 4px;">I couldn\'t match {", ".join(dropped)}, so I ignored it.</div>', unsafe_allow_html=True)
                
                q_text_map = {
                    "scene": "Where were you?",
                    "people": "Who was with you?",
                    "weather": "What was the weather like?",
                    "time_of_day": "What time of day was it?",
                    "season": "Which season was it?",
                    "palette": "Which colour stands out in your memory?",
                    "occasion": "Was it a special occasion?",
                    "activity": "What were you doing just before?"
                }
                
                unasked = [a for a in q_text_map.keys() if a not in current_hints and a not in st.session_state.asked]
                best_attr, entropy = calculate_entropy(candidates, unasked)
                
                if len(candidates) <= 6 or len([k for k,v in st.session_state.answers.items() if v is not None]) >= 3 or entropy == 0 or len(st.session_state.asked) >= 3:
                    st.markdown('<div style="font-size: 16px; color: #202124; margin-top: 16px;">Here are my best matches. Tap the photos you were looking for.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="font-size: 28px; font-weight: 500; color: #202124; line-height: 36px; margin-top: 8px;">{q_text_map[best_attr]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size: 12px; color: #5F6368; margin-top: 4px;">Asking so I can narrow down {len(candidates)} photos. Tap \'Not sure\' to skip.</div>', unsafe_allow_html=True)
                    
                    counts = Counter(p[best_attr] for p in candidates)
                    top_vals = [val for val, count in counts.most_common(4)]
                    
                    st.markdown('<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top: 16px;">', unsafe_allow_html=True)
                    cols = st.columns(len(top_vals) + 1)
                    for i, val in enumerate(top_vals):
                        with cols[i]:
                            st.button(f"{val} ({counts[val]})", key=f"chip_{best_attr}_{val}_{len(st.session_state.asked)}", on_click=answer_q, args=(best_attr, val))
                    with cols[-1]:
                        st.button("Not sure", key=f"chip_not_sure_{len(st.session_state.asked)}", on_click=answer_q, args=(best_attr, None))
                    st.markdown('</div>', unsafe_allow_html=True)
                        
            if st.session_state.answers:
                st.markdown('<div style="display:flex; gap:8px; margin-bottom:16px; flex-wrap:wrap;">', unsafe_allow_html=True)
                for k, v in st.session_state.answers.items():
                    if v:
                        st.button(f"{v} ✕", key=f"applied_{k}", on_click=remove_answer, args=(k,))
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(f\'\'\'
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px;">
                <div><span style="font-size: 16px; font-weight: 500; color: #202124;">Sun, 22 Sep</span> <span style="font-size: 12px; color: #5F6368; margin-left: 12px;">{len(candidates)} items</span></div>
                <div style="font-size: 12px; color: #5F6368;">Select photos to review or share</div>
            </div>
            \'\'\', unsafe_allow_html=True)
            
            with st.container(key="photo_grid"):
                for p in candidates[:24]:
                    with st.container(key=f"tile_{p['id']}"):
                        bg = p['palette'] if p['palette'] != 'purple' else 'rebeccapurple'
                        svg = f'<svg viewBox="0 0 100 100" preserveAspectRatio="slice"><rect width="100" height="100" fill="{bg}" opacity="0.3"/><circle cx="50" cy="50" r="20" fill="white" opacity="0.5"/></svg>'
                        is_sel = p['id'] in st.session_state.selected
                        sel_html = f\'\'\'
                        <div style="position:relative; width:100%; aspect-ratio:1/1; border-radius:4px; overflow:hidden; background:#F1F3F4; transition: 0.15s;
                                    {f'box-shadow: 0 0 0 3px #1A73E8; padding: 12px; background: #E8F0FE;' if is_sel else ''}">
                            <div style="position:relative; width:100%; height:100%; border-radius:{'8px' if is_sel else '0'}; overflow:hidden;">
                                <div style="width:100%; height:100%; background-image:url('data:image/svg+xml;utf8,{svg}'); background-size:cover;"></div>
                            </div>
                            <div style="position:absolute; top:8px; left:8px; width:24px; height:24px; border-radius:50%; 
                                        border: 2px solid white; background: {'#1A73E8' if is_sel else 'rgba(0,0,0,0.25)'}; 
                                        display: flex; align-items: center; justify-content: center; z-index: 5;
                                        {'opacity: 0;' if not is_sel else ''}">
                                {svg_icon("M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z", "white", 16) if is_sel else ""}
                            </div>
                        </div>
                        \'\'\'
                        st.markdown(sel_html, unsafe_allow_html=True)
                        st.markdown(f'<style>.st-key-sel_{p["id"]} button {{ position: absolute; top:0; left:0; width:100%; height:100%; opacity:0; z-index:10; cursor: pointer; }}</style>', unsafe_allow_html=True)
                        st.button(" ", key=f"sel_{p['id']}", on_click=toggle_select, args=(p['id'],))
                if len(candidates) > 24:
                    st.caption(f"+ {len(candidates)-24} more")

    with st.expander("Researcher panel (test log)"):
        if st.session_state.log_data:
            df = pd.DataFrame(st.session_state.log_data)
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="test_log.csv", mime="text/csv")
        else:
            st.write("No data yet.")
'''

with open(r"c:\Users\DELL\OneDrive\Desktop\LAST MVP\app.py", "w", encoding="utf-8") as f:
    f.write(app_code)
