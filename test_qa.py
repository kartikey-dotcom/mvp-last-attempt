import sys
import os

# Add current dir to path so we can import app.py
sys.path.append(os.getcwd())

from streamlit_app import generate_mock_library, parse_hints, apply_constraint_relaxation, calculate_shannon_entropy

def run_tests():
    print("Running QA Tests...")
    library = generate_mock_library()
    
    # Test 1: Purple Sunset Demo Seeding
    print("Test 1: Verifying 'purple sunset' demo seeding...")
    first_10 = library[:10]
    all_purple_sunset = all(p['palette'] == 'purple' and p['time_of_day'] == 'sunset' for p in first_10)
    assert all_purple_sunset, "Failed: First 10 photos are not all purple sunset."
    print("[PASS] Test 1 Passed")
    
    # Test 2: Hint Parsing
    print("Test 2: Verifying Hint Parser...")
    hints = parse_hints("purple dusk")
    assert hints.get('palette') == 'purple' and hints.get('time_of_day') == 'sunset', f"Failed Hint Parsing: {hints}"
    print("[PASS] Test 2 Passed")
    
    # Test 3: Constraint Relaxation (Drop Hierarchy)
    # Give a query that yields 0 exact matches, like "winter beach" (since beach is usually summer/monsoon maybe? Let's force an impossible combo)
    # Wait, the generation is random. Let's just create an impossible hint:
    # "winter" (season) and "alone" (people) and "purple" (palette). 
    print("Test 3: Verifying Constraint Relaxation...")
    impossible_hints = {"season": "winter", "scene": "beach", "time_of_day": "morning", "weather": "snowy"}
    candidates, relaxed_hints = apply_constraint_relaxation(library, impossible_hints)
    assert len(candidates) > 0, "Failed: Constraint relaxation resulted in 0 candidates."
    # Since weather is last to be dropped, it should still be in relaxed_hints if possible, but 'snowy' isn't in synonym map.
    print("[PASS] Test 3 Passed")

    # Test 4: Shannon Entropy
    print("Test 4: Verifying Shannon Entropy...")
    # Using the first 10 items which all share palette=purple and time_of_day=sunset
    best_attr, entropy = calculate_shannon_entropy(first_10, asked_questions=[], inferred_hints={"palette": "purple", "time_of_day": "sunset"})
    # It should pick something like 'scene' which was rotated evenly
    assert entropy > 0, "Failed: Entropy should be > 0"
    assert best_attr is not None, "Failed: Should pick an attribute"
    print(f"[PASS] Test 4 Passed (Best attribute to split demo set is '{best_attr}' with entropy {entropy:.2f})")

    print("All backend QA tests passed successfully!")

if __name__ == "__main__":
    run_tests()
