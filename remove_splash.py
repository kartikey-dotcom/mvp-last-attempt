import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We want to remove the splash screen block and just use `if not q:` for the photo grid.
pattern = re.compile(
    r'    if not q and not st\.session_state\.get\("show_home", False\):.*?    elif not q and st\.session_state\.get\("show_home", False\):', 
    re.DOTALL
)

new_block = '    if not q:'

content = re.sub(pattern, new_block, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Splash screen removed.")
