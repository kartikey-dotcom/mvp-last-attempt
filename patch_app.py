import sys

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_old = """.st-key-topbar button {
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
}"""
css_new = """.st-key-topbar button {
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
.st-key-menu_btn button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    width: 40px !important;
    height: 40px !important;
    color: #5F6368 !important;
}
.st-key-menu_btn button:hover {
    background: rgba(32, 33, 36, 0.08) !important;
    border-radius: 50% !important;
}
"""
content = content.replace(css_old, css_new)

# 2. Update columns in topbar
cols_old = """c1, c2, c3 = st.columns([1, 12, 1], vertical_alignment="center", gap="small")"""
cols_new = """c1, c2, c3 = st.columns([1.5, 12, 1.5], vertical_alignment="center", gap="small")"""
content = content.replace(cols_old, cols_new)

# 3. Hamburger menu clickable -> replace top_header container
header_old = """with st.container(key="top_header"):
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
    ''', unsafe_allow_html=True)"""
header_new = """with st.container(key="top_header"):
    c1, c2, c3 = st.columns([1, 15, 4], vertical_alignment="center")
    with c1:
        if st.button("☰", key="menu_btn", help="Main Menu"):
            st.session_state.query = ""
            st.session_state.show_home = True
            if "q_input" in st.session_state: st.session_state.q_input = ""
            st.rerun()
    with c2:
        st.markdown('<div style="display:flex; align-items:center; margin-top:-4px;"><span class="header-logo-text" style="margin-left:0;">Photos</span><span class="concept-pill">Concept</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div class="header-right" style="justify-content: flex-end; margin-top:-4px;">
            {svg_icon(HELP_ICON)}
            {svg_icon(SETTINGS_ICON)}
            {svg_icon(APPS_ICON)}
            <div class="avatar">A</div>
        </div>
        ''', unsafe_allow_html=True)"""
content = content.replace(header_old, header_new)

# 4. Empty state logic -> if show_home is True, show library grid
empty_logic_old = """    q = st.session_state.query
    if not q:
        st.markdown(f'''
        <div style="display: flex; flex-direction: column; align-items: center; padding-top: 12vh; text-align: center;">"""
empty_logic_new = """    q = st.session_state.query
    if not q and not st.session_state.get("show_home", False):
        st.markdown(f'''
        <div style="display: flex; flex-direction: column; align-items: center; padding-top: 12vh; text-align: center;">"""
content = content.replace(empty_logic_old, empty_logic_new)

# Handle the elif for show_home
elif_logic = """            with cols[3]: st.button("foggy mountain", key="ex_3", on_click=ex_search, args=("foggy mountain",))
            with cols[4]: st.button("cozy dinner with Rohan", key="ex_4", on_click=ex_search, args=("cozy dinner with Rohan",))
    else:
        candidates, current_hints, dropped = get_candidates(library, q, st.session_state.mode)"""
elif_logic_new = """            with cols[3]: st.button("foggy mountain", key="ex_3", on_click=ex_search, args=("foggy mountain",))
            with cols[4]: st.button("cozy dinner with Rohan", key="ex_4", on_click=ex_search, args=("cozy dinner with Rohan",))
    elif not q and st.session_state.get("show_home", False):
        st.markdown(f'''
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px;">
            <div><span style="font-size: 16px; font-weight: 500; color: #202124;">Sun, 22 Sep</span> <span style="font-size: 12px; color: #5F6368; margin-left: 12px;">{len(library)} items</span></div>
            <div style="font-size: 12px; color: #5F6368;">Select photos to review or share</div>
        </div>
        ''', unsafe_allow_html=True)
        with st.container(key="photo_grid"):
            for p in library[:24]:
                with st.container(key=f"tile_{p['id']}"):
                    render_tile(p)
            if len(library) > 24:
                st.caption(f"+ {len(library)-24} more")
    else:
        candidates, current_hints, dropped = get_candidates(library, q, st.session_state.mode)"""
content = content.replace(elif_logic, elif_logic_new)

# 5. Make photos clickable for lightbox.
modal_code = """
@st.dialog("Photo Details")
def view_photo_modal(p):
    scene_map = {"beach": [1, 2], "city": [3], "mountain": [4], "home": [5], "wedding": [6], "restaurant": [7]}
    b64 = None
    if p["scene"] in scene_map:
        num = int(p["id"].split("_")[1])
        photo_idx = scene_map[p["scene"]][num % len(scene_map[p["scene"]])]
        photo_path = f"assets/photos/photo_{photo_idx:02d}.jpg"
        b64 = get_image_base64(photo_path)
    
    if b64:
        st.markdown(f'<img src="data:image/jpeg;base64,{b64}" style="width:100%; border-radius:8px;">', unsafe_allow_html=True)
    else:
        st.markdown(f'<img src="https://picsum.photos/seed/{p["id"]}/800/600" style="width:100%; border-radius:8px;">', unsafe_allow_html=True)
    
    st.write(f"**Scene**: {p['scene']} | **Weather**: {p.get('weather','')} | **Time**: {p.get('time_of_day','')}")

def render_tile"""
content = content.replace("def render_tile", modal_code)

render_tile_old = """    st.markdown(sel_html, unsafe_allow_html=True)
    st.markdown(f'<style>.st-key-sel_{p["id"]} button {{ position: absolute; top:0; left:0; width:100%; height:100%; opacity:0; z-index:10; cursor: pointer; }}</style>', unsafe_allow_html=True)
    st.button(" ", key=f"sel_{p['id']}", on_click=toggle_select, args=(p['id'],))"""
render_tile_new = """    st.markdown(sel_html, unsafe_allow_html=True)
    st.markdown(f'<style>.st-key-view_{p["id"]} button {{ position: absolute; top:0; left:0; width:100%; height:100%; opacity:0; z-index:9; cursor: pointer; }}</style>', unsafe_allow_html=True)
    if st.button(" ", key=f"view_{p['id']}"):
        view_photo_modal(p)
    st.markdown(f'<style>.st-key-sel_{p["id"]} button {{ position: absolute; top:8px; left:8px; width:24px; height:24px; opacity:0; z-index:11; cursor: pointer; border-radius: 50%; }}</style>', unsafe_allow_html=True)
    st.button(" ", key=f"sel_{p['id']}", on_click=toggle_select, args=(p['id'],))"""
content = content.replace(render_tile_old, render_tile_new)

scene_map_old = """    # Match scenes to photo files (01-13 limit)
    scene_map = {"beach": [1,2,3,4,5], "city": [6,7,8], "mountain": [9,10,11], "home": [12,13]}
    if p["scene"] in scene_map:
        num = int(p["id"].split("_")[1])
        photo_idx = scene_map[p["scene"]][num % len(scene_map[p["scene"]])]
        photo_path = f"assets/photos/photo_{photo_idx:02d}.jpg"
        b64 = get_image_base64(photo_path)
        if b64:
            bg_style = f"background-image:url('data:image/jpeg;base64,{b64}'); background-size:cover;"
"""
scene_map_new = """    # Match scenes to photo files
    scene_map = {"beach": [1, 2], "city": [3], "mountain": [4], "home": [5], "wedding": [6], "restaurant": [7]}
    b64 = None
    if p["scene"] in scene_map:
        num = int(p["id"].split("_")[1])
        photo_idx = scene_map[p["scene"]][num % len(scene_map[p["scene"]])]
        photo_path = f"assets/photos/photo_{photo_idx:02d}.jpg"
        b64 = get_image_base64(photo_path)
        if b64:
            bg_style = f"background-image:url('data:image/jpeg;base64,{b64}'); background-size:cover;"
    
    if not b64:
        bg_style = f"background-image:url('https://picsum.photos/seed/{p['id']}/400/400'); background-size:cover;"
"""
content = content.replace(scene_map_old, scene_map_new)

mock_lib_old = """        if i < 13:
            scene = demo_scenes[i]
            palette = "purple"
            time_of_day = "sunset"
            people = rng.choice(PEOPLE)
            weather = rng.choice(WEATHER)
            season = rng.choice(SEASON)
            occasion = rng.choice(OCCASION)
            activity = rng.choice(ACTIVITY)"""
mock_lib_new = """        if i < 13:
            scene = demo_scenes[i]
            palette = "purple"
            time_of_day = "sunset"
            people = rng.choice(PEOPLE)
            weather = rng.choice(WEATHER)
            season = rng.choice(SEASON)
            occasion = rng.choice(OCCASION)
            activity = rng.choice(ACTIVITY)
            
            if i == 0:
                scene, palette, time_of_day, weather = "beach", "purple", "sunset", "cloudy"
            elif i == 1:
                scene, weather, occasion, people = "wedding", "rainy", "wedding", "alone"
            elif i == 2:
                scene, weather = "mountain", "foggy"
            elif i == 3:
                scene, occasion, people, time_of_day = "restaurant", "none", "Rohan", "night"
"""
content = content.replace(mock_lib_old, mock_lib_new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated app.py successfully")
