import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Insert keyword filtering into get_candidates
old_get = r'def get_candidates\(library, query, mode\):\n\s+llm_result = st\.session_state\.llm_res'

new_get = '''def get_candidates(library, query, mode):
    # 1. INITIAL QUERY & CANDIDATE FILTERING
    if query:
        query_lower = query.lower()
        query_words = set(query_lower.split())
        keyword_filtered = []
        for p in library:
            tags = " ".join(p.get("keyword_tags", [])).lower()
            loc = p.get("location_name", "").lower()
            obj = p.get("primary_object", "").lower()
            
            # Simple semantic/keyword match
            if any(w in tags for w in query_words) or any(w in loc for w in query_words) or any(w in obj for w in query_words):
                keyword_filtered.append(p)
        
        # If we found keyword matches, reduce the initial pool N
        if keyword_filtered:
            library = keyword_filtered

    llm_result = st.session_state.llm_res'''

content = re.sub(old_get, new_get, content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Keyword filtering added.")
