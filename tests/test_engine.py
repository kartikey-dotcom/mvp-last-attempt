import pytest
from engine import load_manifest, parse_query, build_predicates, pick_question, apply_answers, baseline_search

@pytest.fixture
def manifest():
    return load_manifest("../assets/photo_manifest.csv") if not load_manifest("assets/photo_manifest.csv") else load_manifest("assets/photo_manifest.csv")

def test_manifest_structure(manifest):
    assert len(manifest) == 48
    
    categories = {}
    for p in manifest:
        categories.setdefault(p['category'], []).append(p)
    
    assert len(categories) == 6
    for cat, photos in categories.items():
        assert len(photos) == 8
        seen = set()
        for p in photos:
            t = (p['shirt'], p['companion'], p['weather'], p['time_of_day'], p['extra'])
            seen.add(t)
        assert len(seen) == 8

def test_disambiguation_max_3_questions(manifest):
    # for every photo, with its category known and truthful answers...
    # at most 2 candidates remain within at most 3 questions
    
    for target in manifest:
        # Category is known
        cat = target['category']
        candidates = [p for p in manifest if p['category'] == cat]
        
        q_count = 0
        answers = []
        skipped = set()
        
        while len(candidates) > 2 and q_count < 3:
            preds = build_predicates(candidates, skipped)
            if not preds:
                break
            best = pick_question(preds, len(candidates))
            if not best:
                break
                
            # answer truthfully
            is_yes = best["fn"](target)
            answers.append({"attr": best["attr"], "key": best["key"], "val": is_yes, "fn": best["fn"]})
            candidates, skipped = apply_answers([p for p in manifest if p['category'] == cat], answers)
            q_count += 1
            
            assert target in candidates
            
        assert len(candidates) <= 2
        assert target in candidates

def test_baseline_search(manifest):
    m1 = baseline_search(manifest, "mountains")
    assert len(m1) == 8
    
    m2 = baseline_search(manifest, "mountains black shirt")
    assert len(m2) == 0
    
    m3 = baseline_search(manifest, "sunset")
    assert len(m3) == 16
    
    m4 = baseline_search(manifest, "cozy cafe")
    assert len(m4) == 0

def test_walkthrough_1(manifest):
    # Query "mountains", target mtn_01 (black shirt, alone)
    # Q1 "Were you with someone?" -> No (3 left) -> Q2 "Were you wearing a black shirt?" -> Yes (1 left: mtn_01)
    target = next(p for p in manifest if p['id'] == 'mtn_01')
    cands, hints, dropped = parse_query("mountains", manifest)
    assert len(cands) == 8
    
    preds = build_predicates(cands, set())
    q1 = pick_question(preds, len(cands))
    assert q1["text"] == "Were you with someone?"
    
    # Answer No
    ans1 = {"attr": q1["attr"], "key": q1["key"], "val": False, "fn": q1["fn"]}
    cands, skipped = apply_answers(cands, [ans1])
    assert len(cands) == 3
    
    preds = build_predicates(cands, skipped)
    q2 = pick_question(preds, len(cands))
    assert q2["text"] == "Were you wearing a black shirt?"
    
    # Answer Yes
    ans2 = {"attr": q2["attr"], "key": q2["key"], "val": True, "fn": q2["fn"]}
    cands, skipped = apply_answers([p for p in manifest if p['category'] == 'mountain'], [ans1, ans2])
    assert len(cands) == 1
    assert cands[0]['id'] == 'mtn_01'

def test_walkthrough_2(manifest):
    # Query "mountains", target mtn_06 (black shirt, group)
    # Q1 "Were you with someone?" -> Yes (5 left) -> Q2 "Were you with just one other person?" -> No (2 left: mtn_03, mtn_06)
    cands, hints, dropped = parse_query("mountains", manifest)
    
    preds = build_predicates(cands, set())
    q1 = pick_question(preds, len(cands))
    ans1 = {"attr": q1["attr"], "key": q1["key"], "val": True, "fn": q1["fn"]}
    cands, skipped = apply_answers(cands, [ans1])
    assert len(cands) == 5
    
    preds = build_predicates(cands, skipped)
    q2 = pick_question(preds, len(cands))
    assert q2["text"] == "Were you with just one other person?"
    
    ans2 = {"attr": q2["attr"], "key": q2["key"], "val": False, "fn": q2["fn"]}
    cands, skipped = apply_answers([p for p in manifest if p['category'] == 'mountain'], [ans1, ans2])
    assert len(cands) == 2
    ids = {p['id'] for p in cands}
    assert ids == {'mtn_03', 'mtn_06'}

def test_walkthrough_3(manifest):
    # Query "cafe", target caf_04
    # Q1 "Were you with someone?" -> No (3 left) -> Q2 "Were you wearing a black shirt?" -> No (2 left: caf_04, caf_08)
    cands, hints, dropped = parse_query("cafe", manifest)
    assert len(cands) == 8
    
    preds = build_predicates(cands, set())
    q1 = pick_question(preds, len(cands))
    assert q1["text"] == "Were you with someone?"
    
    ans1 = {"attr": q1["attr"], "key": q1["key"], "val": False, "fn": q1["fn"]}
    cands, skipped = apply_answers(cands, [ans1])
    assert len(cands) == 3
    
    preds = build_predicates(cands, skipped)
    q2 = pick_question(preds, len(cands))
    assert q2["text"] == "Were you wearing a black shirt?"
    
    ans2 = {"attr": q2["attr"], "key": q2["key"], "val": False, "fn": q2["fn"]}
    cands, skipped = apply_answers([p for p in manifest if p['category'] == 'cafe'], [ans1, ans2])
    assert len(cands) == 2
    ids = {p['id'] for p in cands}
    assert ids == {'caf_04', 'caf_08'}

def test_walkthrough_4(manifest):
    # Query "asdf" shows all 48 and starts with the best-splitting question
    cands, hints, dropped = parse_query("asdf", manifest)
    assert len(cands) == 48
    
    preds = build_predicates(cands, set())
    q1 = pick_question(preds, len(cands))
    assert q1 is not None
