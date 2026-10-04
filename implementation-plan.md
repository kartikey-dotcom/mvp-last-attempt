# Implementation Plan: Progressive Contextual Disambiguation MVP

This document breaks down the development of the Streamlit MVP into logical, testable phases based on the requirements defined in the `problemStatement.md` and the system design in `architecture.md`.

---

## Phase 1: Environment Setup & Data Model
**Goal:** Establish the foundation, manage state, and generate the mock photo library.

1. **Environment Initialization:**
   - Create `app.py` and import `streamlit`, `pandas`, `random`, and `math`.
   - Set up basic Streamlit page config (title, layout).
2. **Session State Initialization (`st.session_state`):**
   - Initialize variables: `mock_library`, `search_mode`, `current_query`, `inferred_hints`, `asked_questions`, `candidate_photos`, `start_time`, `log_data`, and `search_submitted`.
3. **Mock Library Generator:**
   - Create `generate_mock_library(seed=11)` to return 72 deterministic mock photos.
   - Implement the `Photo Schema` (id, scene, people, weather, time_of_day, season, palette, occasion, activity, objective).
   - Enforce the **Demo Seeding Rule:** Ensure the first 10 photos explicitly have `palette=purple` and `time_of_day=sunset` while rotating through scenes.

---

## Phase 2: Core UI Scaffolding & Baseline Search
**Goal:** Build the primary interface and implement the "old way" of searching.

1. **Sidebar UI:**
   - Add a toggle radio for mode switching: "Current search (baseline)" vs "With Contextual Disambiguation".
   - Implement the "Reset session" button to clear `st.session_state`.
   - Ensure **Mode Switching Retention**: If the toggle is changed, immediately re-process the existing `current_query`.
2. **Search Input UI (Decoupled Logic):**
   - Implement the search bar using `st.form` (or strict boolean tracking) so that clicking answer chips later doesn't inadvertently re-trigger a blank or duplicate search.
3. **Baseline Search Engine:**
   - Write the basic filtering logic: split the query into lowercase tokens and return photos where the `objective` list contains ALL tokens.
4. **Photo Grid UI Component:**
   - Build a reusable function to render a 6-column photo grid. Cap the grid at 18 photos and display a "+ N more" caption if the results exceed 18.
   - Each item should display the `palette` as a colored box, the scene `emoji`, the `id`, and a dummy "✅ This is it" button (to be wired up later).

---

## Phase 3: Hint Parser & Constraint Relaxation
**Goal:** Parse natural language into structured attributes for the AI Disambiguation mode.

1. **Synonym Mapper:**
   - Create a dictionary to map common natural language terms to the exact enum values (e.g., "dusk" -> `time_of_day=sunset`, "sea" -> `scene=beach`).
2. **Query Hint Extraction:**
   - Parse the user's query against the synonym mapper and extract the `inferred_hints` dictionary.
3. **Constraint Relaxation Logic:**
   - If filtering `mock_library` by the `inferred_hints` results in 0 photos, begin dropping hints to find matches.
   - Enforce the **Drop Hierarchy**: `Season -> Activity -> Occasion -> Time of Day -> Scene -> Palette -> People -> Weather`.
   - Populate `candidate_photos` with the relaxed subset.

---

## Phase 4: Decision Engine (Entropy) & Question UI
**Goal:** Determine the best follow-up question and present it to the user.

1. **Shannon Entropy Calculator:**
   - Write a function `calculate_shannon_entropy(candidate_photos)` that iterates over unasked attributes.
   - Calculate $H = -\sum (p \times \log_2 p)$ for each attribute and return the attribute with the highest entropy score.
2. **Question Wording & Reason:**
   - Map attributes to their human-readable strings (e.g., Scene -> "Where were you?", Season -> "Which season was it?", Occasion -> "Was it a special occasion?").
   - Under each question add a reason line: "Asking so I can narrow down N photos. Tap Not sure to skip."
3. **Disambiguation UI rendering:**
   - Render the chat bubble acknowledging the parsed hints (e.g., *"I understood palette: purple... That leaves X possible photos."*).
   - Display the bolded question text based on the highest entropy attribute, followed by the reason line.
   - Extract the top 4 most common values for that attribute in the remaining `candidate_photos`.
   - Render 5 tappable Streamlit buttons (Chips): The 4 values + "Not sure". Ensure you specify `on_click` callbacks and unique button keys for all chips to prevent double-click issues.

---

## Phase 5: Interaction Loop & Stop Conditions
**Goal:** Connect the user's answers to the data state and handle edge cases gracefully.

1. **Handling User Answers & Never-Zero Rule:**
   - When a chip is clicked, append the chosen attribute value to `inferred_hints` and add the attribute to `asked_questions`.
   - **Never-Zero Rule**: Ensure that rendering options for chips only uses values present in the remaining `candidate_photos` so a chip click can never produce zero results.
   - If "Not sure" is clicked, just add the attribute to `asked_questions` so it is ignored in future entropy calculations.
2. **Implementing Stop Conditions & Reset:**
   - Before calculating entropy, check if:
     - 6 or fewer `candidate_photos` remain.
     - 3 questions have been asked total.
     - The highest remaining entropy is 0.
   - If any condition is met, **bypass the Question UI entirely** and render the Results Grid.
   - **New Search Reset**: Ensure that submitting a new search explicitly clears the previous answers, asked list, and timer.

---

## Phase 6: Logging & Success Metrics
**Goal:** Track the invisible metrics for testing the efficacy of the MVP.

1. **Timer Management:**
   - Start a timer (record `start_time` in session state) the moment a user submits a search query.
2. **Success Trigger:**
   - When the user clicks "✅ This is it" on a photo card, stop the timer. Ensure these buttons have unique keys and `on_click` callbacks.
3. **Data Recording:**
   - Append a row to the `log_data` Pandas DataFrame.
   - Log structure: `[query, mode, questions_answered, seconds_to_success, photo_id, timestamp]`.
4. **Final Polish:**
   - Display a green success banner indicating the time taken.
   - Expose a "Download CSV" button in the sidebar using the `st.download_button` component for the collected `log_data`.

---

## Phase 7: Deployment (Streamlit Cloud)
**Goal:** Package and deploy the app so it can be shared and tested.

1. **Packaging:**
   - Create a `requirements.txt` containing `streamlit` and `pandas`.
   - Create a `README.md` explaining the project and how to run it.
2. **Deployment Steps:**
   - Push the `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
   - Log into Streamlit Community Cloud (share.streamlit.io).
   - Click "New app", connect the GitHub repo, select the branch and `app.py` as the main file.
   - Click "Deploy" and wait for the build to finish.

---

## Phase 8: Acceptance Testing
**Goal:** Verify all requirements against the 10 tests outlined in the spec.

1. **Verification:**
   - Run through all 10 acceptance tests (e.g., verifying the purple sunset demo works, checking constraint relaxation, confirming state persistence).
   - Fix any issues identified during this QA pass.
