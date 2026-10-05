import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update columns in search form
content = content.replace(
    'c1, c2, c3 = st.columns([1.5, 12, 1.5], vertical_alignment="center", gap="small")',
    'c1, c2, c3 = st.columns([1, 12, 1], vertical_alignment="center", gap="collapse")'
)

# 2. Add specific CSS to fix the search button and hide the extra submit button
css_append = """
/* Fix for search bar icons getting half hidden */
.st-key-topbar [data-testid="column"] button {
    padding: 0 !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    min-height: 36px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.st-key-topbar [data-testid="column"] button:hover {
    background: #E8EAED !important;
    border-radius: 50% !important;
}
.st-key-submit_btn {
    display: none !important;
}
"""

if '.st-key-submit_btn' not in content:
    # insert before the end of the topbar css
    content = content.replace('.st-key-topbar button:hover {', css_append + '\\n.st-key-topbar button:hover {')

# 3. Update the menu button to look cleaner
content = content.replace(
    'if st.button("☰", key="menu_btn", help="Main Menu"):',
    'if st.button("☰", key="menu_btn", help="Main Menu (Home)"): '
)
menu_css = """
.st-key-menu_btn button p {
    font-size: 24px !important;
    line-height: 1 !important;
    padding-bottom: 2px !important;
}
"""
if 'font-size: 24px !important;' not in content:
    content = content.replace('.st-key-menu_btn button {', menu_css + '\\n.st-key-menu_btn button {')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
