import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the hardcoded date in both the Home view and Search view
content = content.replace(
    '<div><span style="font-size: 16px; font-weight: 500; color: #202124;">Sun, 22 Sep</span>',
    '<div><span style="font-size: 16px; font-weight: 500; color: #202124;">All Photos</span>'
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Date replaced.")
