with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

home_linear = """        with st.container(key="photo_grid"):
            for p in library[:24]:
                with st.container(key=f"tile_{p['id']}"):
                    render_tile(p)"""

home_grid = """        with st.container(key="photo_grid"):
            cols = st.columns(4)
            for i, p in enumerate(library[:24]):
                with cols[i % 4]:
                    with st.container(key=f"tile_{p['id']}"):
                        render_tile(p)"""

search_linear = """                with st.container(key="photo_grid"):
                    for p in candidates[:24]:
                        with st.container(key=f"tile_{p['id']}"):
                            render_tile(p)"""

search_grid = """                with st.container(key="photo_grid"):
                    cols = st.columns(4)
                    for i, p in enumerate(candidates[:24]):
                        with cols[i % 4]:
                            with st.container(key=f"tile_{p['id']}"):
                                render_tile(p)"""

if home_linear in content:
    content = content.replace(home_linear, home_grid)

if search_linear in content:
    content = content.replace(search_linear, search_grid)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
