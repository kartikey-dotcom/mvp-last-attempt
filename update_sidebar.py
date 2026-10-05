import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ICONS
icons = {
    'PHOTOS': 'M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z',
    'UPDATES': 'M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2zm-2 1H8v-6c0-2.48 1.51-4.5 4-4.5s4 2.02 4 4.5v6z',
    'ALBUMS': 'M22 4h-4V2H6v2H2v16h20V4zM6 4h12v12H6V4zm-2 14V6H2v12h2zm16-2V6h2v10h-2zm-6-7.5l-3 4-2-2.5L7 15h10l-3.5-4.5z',
    'DOCUMENTS': 'M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z',
    'PHONE': 'M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z',
    'STAR': 'M22 9.24l-7.19-.62L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27 1-4.28-3.32-2.88 4.38-.38L12 6.1l1.71 4.04 4.38.38-3.32 2.88 1 4.28L12 15.4z',
    'PIN': 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',
    'PLAY': 'M10 16.5l6-4.5-6-4.5v9zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z',
    'CLOCK': 'M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z',
    'ARCHIVE': 'M20.54 5.23l-1.39-1.68C18.88 3.21 18.47 3 18 3H6c-.47 0-.88.21-1.16.55L3.46 5.23C3.17 5.57 3 6.02 3 6.5V19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6.5c0-.48-.17-.93-.46-1.27zM6.24 5h11.52l.83 1H5.42l.82-1zM5 19V8h14v11H5zm8-5.5l5-5h-3.5V7h-3v1.5H8l5 5z',
    'LOCK': 'M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM9 6c0-1.66 1.34-3 3-3s3 1.34 3 3v2H9V6zm9 14H6V10h12v10zm-6-3c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z',
    'BIN': 'M15 4V3H9v1H4v2h1v13c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V6h1V4h-5zm2 15H7V6h10v13z',
    'CLOUD': 'M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.36 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4s1.79-4 4-4h.71C7.37 7.69 9.48 6 12 6c3.04 0 5.5 2.46 5.5 5.5v.5H19c1.66 0 3 1.34 3 3s-1.34 3-3 3z',
    'CHEVRON': 'M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z'
}

# Add icons to app.py
icons_code = "\\n".join([f"{k}_ICON = '{v}'" for k, v in icons.items()])
content = re.sub(r'(CLEAR_ICON = ".*?")', r'\1\n' + icons_code, content)

# CSS Update for sidebar
css_old = """[data-testid="stSidebar"] {
    width: 256px !important;
    min-width: 256px !important;
    max-width: 256px !important;
    background-color: #FFFFFF !important;
    border-right: 1px solid #E0E0E0 !important;
}"""
css_new = """[data-testid="stSidebar"] {
    width: 256px !important;
    min-width: 256px !important;
    max-width: 256px !important;
    background-color: #F8FAFD !important;
    border-right: none !important;
}"""
content = content.replace(css_old, css_new)

# Modify sidebar-nav-item CSS
css_old_nav = """.sidebar-nav-item {
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
.sidebar-nav-item svg { fill: #202124 !important; }"""
css_new_nav = """.sidebar-nav-item {
    display: flex;
    align-items: center;
    gap: 16px;
    height: 48px;
    padding: 0 16px;
    border-radius: 9999px;
    color: #444746 !important;
    text-decoration: none !important;
    font-size: 14px;
    font-weight: 500;
    margin: 2px 12px;
    cursor: pointer;
}
.sidebar-nav-item:hover { background: #E1E3E1 !important; color: #1F1F1F !important; }
.sidebar-nav-item.active { background: #C2E7FF !important; color: #001D35 !important; }
.sidebar-nav-item.active svg { fill: #001D35 !important; }
.sidebar-nav-item svg { fill: #444746 !important; width: 20px; height: 20px; }
.sidebar-nav-item.with-chevron { position: relative; }
.sidebar-nav-item.with-chevron .chevron { position: absolute; left: -10px; top: 14px; width: 20px; height: 20px; fill: #444746; }

.sidebar-logo {
    padding: 12px 24px 16px 20px;
    display: flex;
    align-items: center;
    font-size: 22px;
    color: #5F6368;
    font-family: 'Google Sans', 'Product Sans', sans-serif;
    gap: 4px;
}
.sidebar-logo span { color: #5F6368; }
.google-colored span:nth-child(1) { color: #4285F4; }
.google-colored span:nth-child(2) { color: #EA4335; }
.google-colored span:nth-child(3) { color: #FBBC05; }
.google-colored span:nth-child(4) { color: #4285F4; }
.google-colored span:nth-child(5) { color: #34A853; }
.google-colored span:nth-child(6) { color: #EA4335; }

.sidebar-section-title { font-size: 14px; font-weight: 600; color: #444746; padding: 20px 24px 8px; }
.sidebar-divider { border-top: 1px solid #C7C7C7; margin: 16px 24px; }
.storage-bar-container { padding: 0 28px 24px; }
.storage-bar { width: 100%; height: 4px; background: #D3E3FD; border-radius: 2px; margin-top: 8px; margin-bottom: 8px; }
.storage-bar-fill { width: 10%; height: 100%; background: #0A56D1; border-radius: 2px; }
.storage-text { font-size: 12px; color: #444746; }
"""
content = content.replace(css_old_nav, css_new_nav)

# Fix Sidebar Content
sidebar_old = """with st.sidebar:
    st.markdown(f'''
    <a href="#" class="sidebar-nav-item" title="Not part of this prototype">{svg_icon(MENU_ICON)} Photos</a>
    <a href="#" class="sidebar-nav-item active">{svg_icon(SEARCH_ICON, "#041E49")} Explore</a>
    <a href="#" class="sidebar-nav-item" title="Not part of this prototype">{svg_icon(HELP_ICON)} Sharing</a>
    <a href="#" class="sidebar-nav-item" title="Not part of this prototype">{svg_icon(APPS_ICON)} Library</a>
    <a href="#" class="sidebar-nav-item" title="Not part of this prototype">{svg_icon(SETTINGS_ICON)} Utilities</a>
    <div class="sidebar-divider"></div>
    <div class="sidebar-section-title">Prototype Controls</div>
    ''', unsafe_allow_html=True)
    
    st.radio("Search mode", ["Current search", "With Contextual Disambiguation"], key="mode", label_visibility="collapsed")"""

sidebar_new = """with st.sidebar:
    st.markdown(f'''
    <div class="sidebar-logo">
        <strong class="google-colored" style="font-weight: 500;">
            <span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span>
        </strong>
        <span style="font-weight: 400; margin-left:2px;">Photos</span>
    </div>
    
    <a href="#" class="sidebar-nav-item active">{svg_icon(PHOTOS_ICON)} Photos</a>
    <a href="#" class="sidebar-nav-item">{svg_icon(UPDATES_ICON)} Updates</a>
    
    <div class="sidebar-section-title">Collections</div>
    <a href="#" class="sidebar-nav-item">{svg_icon(ALBUMS_ICON)} Albums</a>
    <a href="#" class="sidebar-nav-item with-chevron">
        <svg class="chevron" viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
        {svg_icon(DOCUMENTS_ICON)} Documents
    </a>
    <a href="#" class="sidebar-nav-item" style="line-height:1.2;">{svg_icon(PHONE_ICON)} <span>Screenshots and<br>recordings</span></a>
    <a href="#" class="sidebar-nav-item">{svg_icon(STAR_ICON)} Favourites</a>
    <a href="#" class="sidebar-nav-item">{svg_icon(PIN_ICON)} Places</a>
    <a href="#" class="sidebar-nav-item">{svg_icon(PLAY_ICON)} Videos</a>
    <a href="#" class="sidebar-nav-item">{svg_icon(CLOCK_ICON)} Recently added</a>
    <a href="#" class="sidebar-nav-item">{svg_icon(ARCHIVE_ICON)} Archive</a>
    <a href="#" class="sidebar-nav-item">{svg_icon(LOCK_ICON)} Locked Folder</a>
    <a href="#" class="sidebar-nav-item">{svg_icon(BIN_ICON)} Bin</a>
    
    <div class="sidebar-divider"></div>
    <a href="#" class="sidebar-nav-item" style="margin-bottom:0;">{svg_icon(CLOUD_ICON)} Storage</a>
    <div class="storage-bar-container">
        <div class="storage-bar">
            <div class="storage-bar-fill"></div>
        </div>
        <div class="storage-text">12.8 GB of 5 TB used</div>
    </div>
    <div class="sidebar-section-title" style="margin-top: 16px;">Prototype Controls</div>
    ''', unsafe_allow_html=True)
    
    st.radio("Search mode", ["Current search", "With Contextual Disambiguation"], key="mode", label_visibility="collapsed")"""

content = content.replace(sidebar_old, sidebar_new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with sidebar!")
