import re
import os

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace get_candidates
pattern_get_cand = re.compile(r'def get_candidates\(.*?return candidates, hints, dropped', re.DOTALL)
new_get_cand = """def get_candidates(library, query, mode):
    if mode == "Current search":
        return engine.baseline_search(library, query), {}, []
    else:
        return engine.parse_query(query, library)"""
content = re.sub(pattern_get_cand, new_get_cand, content)

# Replace calculate_entropy and agent_step
pattern_agent = re.compile(r'def calculate_entropy\(.*?\n\ndef agent_step\(.*?\n\n', re.DOTALL)
content = re.sub(pattern_agent, "\n\n", content)

# Replace the assistant block
pattern_assistant = re.compile(r'                q_text_map = \{.*?st\.markdown\(\'</div>\', unsafe_allow_html=True\)', re.DOTALL)
new_assistant = """                
                state = AgentState(
                    query=q, hints=current_hints, answered=st.session_state.answers, 
                    asked=st.session_state.asked, selected_anchor=st.session_state.get("selected_anchor"),
                    candidates=candidates, steps=st.session_state.get("agent_trace", []), ai_used=st.session_state.get("ai_used")
                )
                
                # New Yes/No Engine
                answers_list = st.session_state.get("answers_list", [])
                candidates, skipped_attrs = engine.apply_answers(candidates, answers_list)
                
                if len(candidates) <= 2 or len(st.session_state.get("answers_list", [])) >= 8:
                    st.markdown('<div style="font-size: 16px; color: #202124; margin-top: 16px;">Here are my best matches. Tap the photo you were looking for.</div>', unsafe_allow_html=True)
                else:
                    preds = engine.build_predicates(candidates, skipped_attrs)
                    best_pred = engine.pick_question(preds, len(candidates))
                    
                    if not best_pred:
                        st.markdown('<div style="font-size: 16px; color: #202124; margin-top: 16px;">Here are my best matches. Tap the photo you were looking for.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="font-size: 28px; font-weight: 500; color: #202124; line-height: 36px; margin-top: 8px;">{best_pred["text"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size: 12px; color: #5F6368; margin-top: 4px;">Asking so I can narrow down {len(candidates)} photos. Tap \\'Not sure\\' to skip.</div>', unsafe_allow_html=True)
                        
                        st.markdown('<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top: 16px;">', unsafe_allow_html=True)
                        ans_idx = len(answers_list)
                        st.button("Yes", key=f"ans_{ans_idx}_yes", type="primary", on_click=answer_q, args=(best_pred, True))
                        st.button("No", key=f"ans_{ans_idx}_no", on_click=answer_q, args=(best_pred, False))
                        st.button("Not sure", key=f"ans_{ans_idx}_notsure", on_click=answer_q, args=(best_pred, None))
                        st.markdown('</div>', unsafe_allow_html=True)"""
content = re.sub(pattern_assistant, new_assistant, content)

# Replace answer_q callback
pattern_answer_q = re.compile(r'def answer_q\(.*?\n    st\.session_state\.answers\[attr\] = val', re.DOTALL)
new_answer_q = """def answer_q(pred, val):
    if "answers_list" not in st.session_state:
        st.session_state.answers_list = []
    
    st.session_state.answers_list.append({
        "attr": pred["attr"],
        "key": pred["key"],
        "val": val,
        "fn": pred["fn"],
        "label": pred["label"]
    })"""
content = re.sub(pattern_answer_q, new_answer_q, content)

# Replace applied answers UI
pattern_applied = re.compile(r'if st\.session_state\.answers or st\.session_state\.get\("selected_anchor"\):.*?st\.markdown\(\'</div>\', unsafe_allow_html=True\)', re.DOTALL)
new_applied = """            if st.session_state.get("answers_list") or st.session_state.get("selected_anchor"):
                st.markdown('<div style="display:flex; gap:8px; margin-bottom:16px; flex-wrap:wrap; align-items:center;">', unsafe_allow_html=True)
                for i, ans in enumerate(st.session_state.get("answers_list", [])):
                    if ans["val"] is True:
                        lbl = ans["label"]
                    elif ans["val"] is False:
                        lbl = f"Not {ans['label'].lower()}"
                    else:
                        lbl = "Skipped"
                    st.button(f"{lbl} ✕", key=f"applied_{i}_{ans['key']}", on_click=remove_answer, args=(i,))
                    
                if st.session_state.get("selected_anchor"):
                    st.button(f"Similar to {st.session_state.selected_anchor} ✕", key="applied_anchor", on_click=clear_anchor)
                    
                if st.session_state.get("answers_list"):
                    st.button("Undo last answer", key="undo_ans", on_click=undo_answer)
                    st.button("Start over", key="reset_ans", on_click=start_over_answers)
                st.markdown('</div>', unsafe_allow_html=True)"""
content = re.sub(pattern_applied, new_applied, content)

# Helper functions for UI
helpers = """def remove_answer(idx):
    st.session_state.answers_list.pop(idx)

def undo_answer():
    if st.session_state.answers_list:
        st.session_state.answers_list.pop()

def start_over_answers():
    st.session_state.answers_list = []
"""
content = content.replace("def remove_answer(attr):", helpers + "def OLD_remove_answer(attr):")

# Fix bg_style in render_tile
pattern_bg = re.compile(r"bg_style = f\"background-image:url\('https://picsum\.photos/seed/\{p\['id'\]\}/400/400'\); background-size:cover;\"")
new_bg = "b64 = get_image_base64(p['id'], p['category'], p['shirt'], p['companion'])\n    bg_style = f\"background-image:url('data:image/jpeg;base64,{b64}'); background-size:cover;\""
content = re.sub(pattern_bg, new_bg, content)

# Add Researcher Photo Inspector
pattern_researcher = re.compile(r'with st\.expander\("Researcher tools"\):.*?st\.dataframe\(df_logs, use_container_width=True\)', re.DOTALL)
new_researcher = """with st.expander("Researcher tools"):
    t1, t2 = st.tabs(["Logs", "Photo Inspector"])
    with t1:
        if os.path.exists("logs.csv"):
            df_logs = pd.read_csv("logs.csv")
            st.dataframe(df_logs, use_container_width=True)
    with t2:
        st.markdown("### Photo Inspector")
        manifest = engine.load_manifest()
        missing_count = sum(1 for p in manifest if not os.path.exists(f"assets/photos/{p['id']}.jpg"))
        if missing_count > 0:
            st.error(f"{missing_count} of 48 photos are placeholders. Replace them before user testing.")
        
        st.dataframe(pd.DataFrame(manifest), use_container_width=True)"""
content = re.sub(pattern_researcher, new_researcher, content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated app.py")
