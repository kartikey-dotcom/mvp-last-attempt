import pathlib

app_path = pathlib.Path('app.py')
content = app_path.read_text(encoding='utf-8')

# 1. CSS
old_css_start = 'CSS = """\\n<style>'
old_css_end = '</style>\\n"""\\nst.markdown(CSS, unsafe_allow_html=True)'

start_idx = content.find('CSS = """')
end_idx = content.find('st.markdown(CSS, unsafe_allow_html=True)') + len('st.markdown(CSS, unsafe_allow_html=True)')

css_new = """CSS = \"\"\"
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto:wght@400;500;700&display=swap');

[data-testid="stDecoration"], 
header[data-testid="stHeader"], 
[data-testid="stToolbar"], 
[data-testid="stStatusWidget"], 
footer, 
#MainMenu {
    display: none !important;
}

.stApp, .stApp p, .stApp label, .stApp span, [data-testid="stMarkdownContainer"] {
    background-color: #FFFFFF !important;
    font-family: Roboto, Inter, 'Google Sans', 'Google Sans Text', system-ui, sans-serif !important;
    color: #202124 !important;
    font-size: 14px;
    line-height: 20px;
}

[data-testid="stCaptionContainer"], .help-text {
    color: #5F6368 !important;
}

.block-container {
    padding: 24px 32px 96px !important;
    max-width: 1100px !important;
    margin: 0 auto;
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
    z-index: 1000;
    display: flex;
    align-items: center;
    padding: 0 16px;
}

.header-inner {
    display: flex;
    width: 100%;
    align-items: center;
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

/* Sidebar overrides */
[data-testid="stSidebar"] {
    width: 256px !important;
    min-width: 256px !important;
    max-width: 256px !important;
    background-color: #FFFFFF !important;
    border-right: 1px solid #E0E0E0 !important;
}
.stSidebarContent, [data-testid="stSidebar"] > div:first-child {
    padding-top: 72px !important;
}
[data-testid="stSidebarNav"], [data-testid="stSidebarHeader"], [data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

/* Sidebar Nav Items HTML block */
.sidebar-nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    height: 48px;
    padding: 0 12px;
    border-radius: 9999px;
    color: #202124 !important;
    text-decoration: none !important;
    font-size: 14px;
    font-weight: 500;
}
.sidebar-nav-item:hover { background: #F1F3F4 !important; }
.sidebar-nav-item.active { background: #D3E3FD !important; color: #041E49 !important; }
.sidebar-nav-item.active svg { fill: #041E49 !important; }
.sidebar-nav-item svg { fill: #202124 !important; }

/* Divider */
.sidebar-divider { border-top: 1px solid #E1E3E1; margin: 16px 8px; }
.sidebar-section-title { font-size: 11px; font-weight: 600; letter-spacing: 0.6px; color: #5F6368; padding: 0 12px; margin-bottom: 12px; text-transform: uppercase; }

/* Prototype Controls */
[data-testid="stRadio"] label p { color: #202124 !important; font-size: 14px !important; }
[data-testid="stToggle"] label p { color: #202124 !important; font-size: 14px !important; }
div[data-baseweb="radio"] div[data-checked="true"], div[data-baseweb="checkbox"] div[data-checked="true"] {
    background-color: #1A73E8 !important;
    border-color: #1A73E8 !important;
}

/* Search Bar Pill */
.st-key-topbar {
    position: fixed;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: min(720px, 46vw);
    height: 48px;
    z-index: 1001;
}
.st-key-search_form [data-testid="stForm"] {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    background-color: #E9EEF6 !important;
    border-radius: 9999px !important;
    height: 48px !important;
    padding: 0 8px !important;
    border: none !important;
    width: 100% !important;
}
.st-key-search_form [data-testid="stForm"]:focus-within {
    background-color: #FFFFFF !important;
    border: 1px solid #DADCE0 !important;
    box-shadow: 0 1px 3px rgba(60,64,67,.30), 0 4px 8px 3px rgba(60,64,67,.15) !important;
}
.st-key-search_form .stTextInput div[data-baseweb="input"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
.st-key-search_form .stTextInput input {
    color: #202124 !important;
    font-size: 16px !important;
    background-color: transparent !important;
    -webkit-text-fill-color: #202124 !important;
}
.st-key-search_form .stTextInput input::placeholder {
    color: #5F6368 !important;
    -webkit-text-fill-color: #5F6368 !important;
}
.st-key-search_form .stTextInput input:focus {
    outline: none !important;
    box-shadow: none !important;
}
.st-key-search_form .stButton button, .st-key-search_form .stFormSubmitButton button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #5F6368 !important;
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.st-key-search_form .stButton button:hover, .st-key-search_form .stFormSubmitButton button:hover {
    background-color: rgba(32, 33, 36, 0.08) !important;
    color: #202124 !important;
}
/* Hide the stray submit button */
.st-key-submit_btn,
.st-key-submit_btn button {
    display: none !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
}
.st-key-topbar [data-testid="column"] { padding: 0 !important; width: auto !important; flex: 0 1 auto !important; }
.st-key-topbar [data-testid="column"]:nth-child(2) { flex: 1 1 auto !important; }

/* Assistant card */
.st-key-assistant {
    background: #EEF2F9;
    border-radius: 24px;
    padding: 20px 24px;
    margin-bottom: 24px;
    max-width: 100%;
}
.st-key-assistant [data-testid="stVerticalBlock"] { gap: 0 !important; }

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
div[class*="st-key-chip_"]:active button { background: #D3E3FD !important; }
div[class*="st-key-chip_not_sure"] button { border-style: dashed !important; }

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
div[class*="st-key-applied_"] button:hover { background: #C2D7FA !important; }

/* Photo Grid */
.st-key-photo_grid [data-testid="stVerticalBlock"] {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)) !important;
    gap: 8px !important;
}
div[class*="st-key-tile_"] { width: auto !important; }

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
@media (max-width: 900px) { .st-key-actionbar { left: 0; } }
.st-key-commit_btn button {
    background: #1A73E8 !important;
    color: white !important;
    border-radius: 9999px !important;
    height: 40px !important;
    padding: 0 24px !important;
    border: none !important;
    font-weight: 500 !important;
}
.st-key-commit_btn button:hover { background: #1967D2 !important; }

/* Light Expanders for Researcher Tools */
[data-testid="stExpander"] {
    background: #F8FAFD !important;
    border: 1px solid #E1E3E1 !important;
    border-radius: 16px !important;
}
[data-testid="stExpander"] summary {
    height: 48px !important;
    background: transparent !important;
    color: #202124 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] summary:hover { background: #F1F3F4 !important; }
[data-testid="stExpander"] summary svg { fill: #5F6368 !important; }
/* Table background */
[data-testid="stDataFrame"] { background: #FFFFFF !important; border: 1px solid #E1E3E1 !important; }

.hide { display: none !important; }
</style>
\"\"\"
st.markdown(CSS, unsafe_allow_html=True)"""
content = content[:start_idx] + css_new + content[end_idx:]

# 2. Header and Search form
import re
header_old = r'with st\.container\(key="top_header"\):.*?with st\.container\(key="topbar"\):.*?st\.markdown\(\'<style>\.st-key-search_form.*?unsafe_allow_html=True\)'
header_new = """with st.container(key="top_header"):
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
    with st.form(key="search_form", border=False, clear_on_submit=False):
        c1, c2, c3 = st.columns([1, 12, 1], vertical_alignment="center", gap="small")
        with c1:
            st.form_submit_button("", icon=":material/search:", type="tertiary", on_click=do_search)
        with c2:
            st.text_input("Search", key="q_input", label_visibility="collapsed", placeholder="Search your photos")
        with c3:
            if st.session_state.q_input:
                if st.form_submit_button("", icon=":material/close:", type="tertiary"):
                    reset_search()
                    st.rerun()
            else:
                st.write("")
        st.form_submit_button("submit", on_click=do_search, key="submit_btn")
"""
content = re.sub(header_old, header_new, content, flags=re.DOTALL)

sidebar_block_old = r'with st\.container\(key="left_nav"\):.*?# SEARCH LOGIC'
sidebar_block_new = """with st.sidebar:
    st.markdown(f'''
    <a href="#" class="sidebar-nav-item" title="Not part of this prototype">{svg_icon(MENU_ICON)} Photos</a>
    <a href="#" class="sidebar-nav-item active">{svg_icon(SEARCH_ICON, "#041E49")} Explore</a>
    <a href="#" class="sidebar-nav-item" title="Not part of this prototype">{svg_icon(HELP_ICON)} Sharing</a>
    <a href="#" class="sidebar-nav-item" title="Not part of this prototype">{svg_icon(APPS_ICON)} Library</a>
    <a href="#" class="sidebar-nav-item" title="Not part of this prototype">{svg_icon(SETTINGS_ICON)} Utilities</a>
    <div class="sidebar-divider"></div>
    <div class="sidebar-section-title">Prototype Controls</div>
    ''', unsafe_allow_html=True)
    
    st.radio("Search mode", ["Current search", "With Contextual Disambiguation"], key="mode", label_visibility="collapsed")
    has_key = bool(GEMINI_API_KEY)
    st.toggle("AI assist", value=has_key, key="ai_on", disabled=not has_key)
    st.markdown('<div class="help-text" style="font-size: 11px;">AI assist sends your search text to Google\\'s Gemini API.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="help-text" style="margin-top: 32px; font-size: 11px;">Concept prototype for a PM case study. Not affiliated with or endorsed by Google. All photos and data are simulated.</div>', unsafe_allow_html=True)

# -----------------
# SEARCH LOGIC"""
content = re.sub(sidebar_block_old, sidebar_block_new, content, flags=re.DOTALL)

# 3. do_search updates (add pending_query)
do_search_old = """def do_search():
    if st.session_state.q_input:
        st.session_state.query = st.session_state.q_input
    st.session_state.answers = {}
    st.session_state.asked = []
    st.session_state.selected = set()
    st.session_state.start_time = time.time()
    st.session_state.success_msg = None
    st.session_state.selected_anchor = None
    st.session_state.agent_trace = []"""
do_search_new = """def do_search():
    if st.session_state.q_input:
        st.session_state.pending_query = st.session_state.q_input
    st.session_state.answers = {}
    st.session_state.asked = []
    st.session_state.selected = set()
    st.session_state.start_time = time.time()
    st.session_state.success_msg = None
    st.session_state.selected_anchor = None
    st.session_state.agent_trace = []"""
content = content.replace(do_search_old, do_search_new)

# 4. get_hints update
hints_fn_old = """def get_hints(query):
    query = query.lower()
    hints = {}
    synonyms = {
        "dusk": "sunset", "evening": "sunset",
        "violet": "purple", "pink": "purple",
        "rain": "rainy", "raining": "rainy",
        "fog": "foggy",
        "sea": "beach", "ocean": "beach",
        "hills": "mountain"
    }"""
hints_fn_new = """def get_hints(query):
    query = query.lower()
    import re
    query = re.sub(r'[,\.]', '', query)
    hints = {}
    synonyms = {
        "dusk": "sunset", "evening": "sunset",
        "violet": "purple", "pink": "purple",
        "rain": "rainy", "raining": "rainy",
        "fog": "foggy",
        "sea": "beach", "ocean": "beach",
        "hills": "mountain",
        "dinner": "restaurant", "lunch": "restaurant", "food": "restaurant",
        "cafe": "restaurant", "café": "restaurant", "dessert": "restaurant", "desserts": "restaurant", "restaurant": "restaurant",
        "candle": "night", "candlelight": "night", "night": "night", "evening-out": "night",
        "marriage": "wedding", "wedding": "wedding",
        "vacation": "trip", "holiday": "trip", "trip": "trip",
        "birthday": "birthday"
    }"""
content = content.replace(hints_fn_old, hints_fn_new)

# 5. Empty State & Pending Query handling
empty_state_old = r'if not st\.session_state\.query:.*?st\.markdown\(\'<div style="font-size: 11px; color: #5F6368; margin-top: 16px;">Try an example from the bottom left, or type your own search.</div>\', unsafe_allow_html=True\)\n    else:'
empty_state_new = """if st.session_state.get("pending_query"):
        st.session_state.query = st.session_state.pending_query
        del st.session_state.pending_query
        
        ph = st.empty()
        with ph.container():
            st.markdown(f'''
            <div style="background: #EEF2F9; border-radius: 24px; padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: center; gap: 12px; transition: opacity 0.15s ease-in;">
                <div style="animation: pulse 1.5s infinite;">{SPARKLE_SVG}</div>
                <div style="font-size: 16px; color: #202124;">Understanding your search...</div>
            </div>
            <div style="height: 4px; width: 100%; background: linear-gradient(90deg, #E8F0FE, #D3E3FD, #E8F0FE); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 4px;"></div>
            <style>
            @keyframes pulse {{ 0% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.5; }} }}
            @keyframes shimmer {{ 0% {{ background-position: 100% 0; }} 100% {{ background-position: -100% 0; }} }}
            </style>
            ''', unsafe_allow_html=True)
        
        res, latency, used = parse_query_with_llm(st.session_state.query)
        st.session_state.llm_res = res
        st.session_state.last_latency = latency
        st.session_state.ai_used = used
        st.rerun()

    if not st.session_state.query:
        st.markdown(f'''
        <div style="display: flex; flex-direction: column; align-items: center; padding-top: 12vh; text-align: center;">
            <div style="width: 96px; height: 96px; background-color: #F0F4F9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px;">
                {svg_icon(SEARCH_ICON, "#1A73E8", 48)}
            </div>
            <div style="font-size: 24px; font-weight: 500; color: #202124; margin-bottom: 8px;">Search your photos</div>
            <div style="font-size: 14px; color: #5F6368; margin-bottom: 32px;">Try describing a moment the way you remember it.</div>
        </div>
        ''', unsafe_allow_html=True)
        
        def ex_search(q):
            st.session_state.q_input = q
            st.session_state.pending_query = q
        
        cols = st.columns(4, gap="small")
        with cols[0]: st.button("purple sunset", key="ex_1", on_click=ex_search, args=("purple sunset",), use_container_width=True)
        with cols[1]: st.button("rainy wedding", key="ex_2", on_click=ex_search, args=("rainy wedding",), use_container_width=True)
        with cols[2]: st.button("foggy mountain", key="ex_3", on_click=ex_search, args=("foggy mountain",), use_container_width=True)
        with cols[3]: st.button("cozy dinner with Rohan", key="ex_4", on_click=ex_search, args=("cozy dinner with Rohan",), use_container_width=True)
    else:"""
content = re.sub(empty_state_old, empty_state_new, content, flags=re.DOTALL)

# 6. Remove double AI call
old_ai_call = """if st.session_state.mode == "With Contextual Disambiguation":
            if st.session_state.get("llm_res") is None:
                res, latency, used = parse_query_with_llm(st.session_state.query)
                st.session_state.llm_res = res
                st.session_state.last_latency = latency
                st.session_state.ai_used = used
            
            if st.session_state.get("llm_res") is not None:"""
new_ai_call = """if st.session_state.mode == "With Contextual Disambiguation":
            if st.session_state.get("llm_res") is not None:"""
content = content.replace(old_ai_call, new_ai_call)

# 7. Researcher panel
expander_idx = content.find('    with st.expander("Prototype Settings (Moved from sidebar)"):')
if expander_idx != -1:
    content = content[:expander_idx] + """    with st.expander("Researcher tools", expanded=False):
        t1, t2, t3 = st.tabs(["Test log", "Agent trace", "Data"])
        with t1:
            if st.session_state.log_data:
                df = pd.DataFrame(st.session_state.log_data)
                st.dataframe(df, use_container_width=True)
                st.download_button("Download CSV", data=df.to_csv(index=False).encode('utf-8'), file_name="test_log.csv", mime="text/csv")
            else:
                st.write("No data yet.")
        with t2:
            if st.session_state.get("agent_trace"):
                st.markdown(f"**Step count:** {len(st.session_state.agent_trace)}")
                st.dataframe(pd.DataFrame(st.session_state.agent_trace), use_container_width=True)
            else:
                st.write("No trace yet.")
        with t3:
            tags_status = "vision model" if PHOTO_TAGS else "simulated"
            st.markdown(f"**Photo tags:** {tags_status}")
            st.markdown(f"**LLM Latency:** {st.session_state.get('last_latency', 0)} ms")
"""

app_path.write_text(content, encoding='utf-8')
