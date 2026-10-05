with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('[data-testid="stSidebarNav"], [data-testid="stSidebarHeader"], [data-testid="stSidebarCollapsedControl"]', '[data-testid="stSidebarNav"], [data-testid="stSidebarHeader"]')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
