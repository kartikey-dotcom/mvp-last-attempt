import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS block for search bar and empty state centering
# Locate the CSS block
css_match = re.search(r'(?s)CSS = """(.*?)"""\nst\.markdown\(CSS, unsafe_allow_html=True\)', content)
if css_match:
    css_content = css_match.group(1)
    
    # Fix the search form CSS completely
    old_search_css = re.search(r'(?s)/\* Search Bar Pill \*/.*?/\* Assistant card \*/', css_content)
    if old_search_css:
        new_search_css = """/* Search Bar Pill */
.st-key-topbar {
    position: fixed !important;
    top: 8px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(720px, 46vw) !important;
    height: 48px !important;
    z-index: 1001 !important;
}
.st-key-search_form [data-testid="stForm"] {
    background-color: #F1F3F4 !important;
    border-radius: 9999px !important;
    border: 1px solid transparent !important;
    padding: 0 16px !important;
    height: 48px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}
.st-key-search_form [data-testid="stForm"]:focus-within {
    background-color: #FFFFFF !important;
    border: 1px solid #DADCE0 !important;
    box-shadow: 0 1px 3px rgba(60,64,67,.30), 0 4px 8px 3px rgba(60,64,67,.15) !important;
}
.st-key-search_form [data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    align-items: center !important;
}
.st-key-search_form [data-testid="column"] {
    padding: 0 !important;
    width: auto !important;
    flex: 0 1 auto !important;
}
.st-key-search_form [data-testid="column"]:nth-child(2) {
    flex: 1 1 auto !important;
    width: 100% !important;
}
.st-key-search_form input {
    background-color: transparent !important;
    border: none !important;
    color: #202124 !important;
    font-size: 16px !important;
}
.st-key-search_form input::placeholder { color: #5F6368 !important; }
.st-key-search_form div[data-baseweb="input"], .st-key-search_form div[data-baseweb="base-input"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
.st-key-search_form button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #5F6368 !important;
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.st-key-search_form button:hover {
    background-color: rgba(32, 33, 36, 0.08) !important;
    color: #202124 !important;
}
/* Hide the stray submit button */
.st-key-submit_btn {
    display: none !important;
}

/* Center the Examples Block in the Empty State */
.st-key-examples_block [data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
}
.st-key-examples_block [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {
    display: flex !important;
    justify-content: center !important;
}

/* Assistant card */\n"""
        css_content = css_content.replace(old_search_css.group(0), new_search_css)
        content = content.replace(css_match.group(1), css_content)

# 2. Update Search form in Python
old_search_form = """with st.container(key="topbar"):
    with st.form(key="search_form", border=False, clear_on_submit=False):
        c1, c2, c3 = st.columns([1, 12, 1], vertical_alignment="center", gap="small")
        with c1:
            st.form_submit_button("", icon=":material/search:", type="tertiary", on_click=do_search)
        with c2:
            st.text_input("Search", key="q_input", label_visibility="collapsed", placeholder="Search your photos")
        with c3:
            if st.session_state.get("q_input"):
                if st.form_submit_button("", icon=":material/close:", type="tertiary"):
                    reset_search()
                    st.rerun()
            else:
                st.write("")
        st.form_submit_button("submit", on_click=do_search, key="submit_btn")"""

new_search_form = """with st.container(key="topbar"):
    with st.form(key="search_form", border=False, clear_on_submit=False):
        c1, c2, c3 = st.columns([1, 12, 1], vertical_alignment="center", gap="small")
        with c1:
            st.form_submit_button("🔍", on_click=do_search)
        with c2:
            st.text_input("Search", key="q_input", label_visibility="collapsed", placeholder="Search your photos")
        with c3:
            if st.session_state.get("q_input"):
                if st.form_submit_button("✕"):
                    reset_search()
                    st.rerun()
            else:
                st.write("")
        st.form_submit_button("submit", on_click=do_search, key="submit_btn")"""

content = content.replace(old_search_form, new_search_form)

# 3. Fix Empty state chips
old_empty_state_chips = """        cols = st.columns(4, gap="small")
        with cols[0]: st.button("purple sunset", key="ex_1", on_click=ex_search, args=("purple sunset",), use_container_width=True)
        with cols[1]: st.button("rainy wedding", key="ex_2", on_click=ex_search, args=("rainy wedding",), use_container_width=True)
        with cols[2]: st.button("foggy mountain", key="ex_3", on_click=ex_search, args=("foggy mountain",), use_container_width=True)
        with cols[3]: st.button("cozy dinner with Rohan", key="ex_4", on_click=ex_search, args=("cozy dinner with Rohan",), use_container_width=True)"""

new_empty_state_chips = """        with st.container(key="examples_block"):
            cols = st.columns([1.5, 2, 2, 2, 2, 1.5], gap="small")
            with cols[1]: st.button("purple sunset", key="ex_1", on_click=ex_search, args=("purple sunset",))
            with cols[2]: st.button("rainy wedding", key="ex_2", on_click=ex_search, args=("rainy wedding",))
            with cols[3]: st.button("foggy mountain", key="ex_3", on_click=ex_search, args=("foggy mountain",))
            with cols[4]: st.button("cozy dinner with Rohan", key="ex_4", on_click=ex_search, args=("cozy dinner with Rohan",))"""

content = content.replace(old_empty_state_chips, new_empty_state_chips)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
