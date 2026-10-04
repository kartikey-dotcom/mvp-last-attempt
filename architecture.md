# System Architecture: Progressive Contextual Disambiguation App

This document outlines the detailed architecture and technical design for the Progressive Contextual Disambiguation MVP built with Streamlit.

---

## 1. High-Level Overview

The application is designed as a **single-file Streamlit web app** (`app.py`). It simulates a fallback search mechanism for a photo library by switching from a traditional keyword search to an interactive disambiguation process when zero results are found.

**Key Characteristics:**
- **Stateless (mostly):** Relies on `st.session_state` to maintain the user's progress through the disambiguation flow.
- **No External Database:** Uses an in-memory, deterministically generated Python dictionary to serve as the mock photo library.
- **Analytics Included:** Generates session logs and metrics stored in a Pandas DataFrame, exportable via CSV.

---

## 2. Component Architecture

The app is divided into the following logical components, all residing in `app.py`:

### A. Data Layer (Mock Library)
A deterministic generator creates the exact same 72 photos on every run.
- **Function:** `generate_mock_library(seed=11)`
- **Data Structure:** A list of dictionaries representing photos.
- **Seeding Rule Enforcement:** The first 10 photos are strictly mapped to `palette=purple` and `time_of_day=sunset` to guarantee the MVP demo works perfectly.

### B. Search Engine & Parser
Handles the initial user query and decides the application mode.
- **Baseline Search Engine:** Performs strict substring/token matching against the `objective` list. Returns results only if ALL tokens match.
- **Hint Parser (AI Disambiguation):** 
  - Tokenizes the input and maps terms to specific entity attributes using a hardcoded synonym dictionary.
  - Applies **Constraint Relaxation** if initial parsing yields zero results. Hints are dropped in this specific hierarchy of least-importance to avoid 0 results: `Season -> Weather -> Activity -> Time of Day -> People -> Palette -> Scene`.

### C. Decision Engine (Entropy Calculator)
The core logic for deciding *which* question to ask next when disambiguating.
- **Math Function:** `calculate_shannon_entropy(candidate_photos)`
- **Mechanism:** Iterates over unasked attributes (`scene`, `people`, `weather`, `time_of_day`, `palette`, `activity`) across the remaining candidate photos.
- **Output:** Selects the attribute with the highest entropy $H = -\sum (p \times \log_2 p)$ (the one that most evenly divides the remaining dataset).

### D. UI & Presentation Layer (Streamlit)
Manages the user interface and interactions.
- **Sidebar:** For mode switching, resetting, and exporting data.
- **Search Bar:** Main input triggering the flow.
- **Disambiguation View:** 
  - Shows understood context (e.g., *"I understood palette: purple..."*)
  - Renders the chosen question (e.g., *"What time of day was it?"*).
  - Displays answer chips (top 4 attribute values + "Not sure").
- **Results Grid:** A 6-column photo grid displaying colored cards, emojis, and the final "✅ This is it" selection buttons.

---

## 3. State Management (`st.session_state`)

Because Streamlit reruns the entire script on every interaction, state management is critical. The following keys will be managed in `st.session_state`:

| State Key | Type | Purpose |
| :--- | :--- | :--- |
| `mock_library` | List[Dict] | Caches the 72-photo dataset so it's not regenerated constantly. |
| `search_mode` | String | Tracks if the user is in "Baseline" or "Disambiguation" mode. |
| `current_query` | String | The active search term. |
| `inferred_hints` | Dict | Attributes extracted from the query or answered via questions (e.g., `{"palette": "purple"}`). |
| `asked_questions` | List[String] | Tracks attributes we have already asked about to prevent repetition. |
| `candidate_photos`| List[Dict] | The shrinking subset of photos that match the current `inferred_hints`. |
| `start_time` | Float | Timestamp when the search/disambiguation started. |
| `log_data` | DataFrame | Stores test metrics for CSV export. |

---

## 4. Application Flow

1. **Initialization:**
   - App loads, initializes `st.session_state`.
   - `generate_mock_library()` creates the dataset.

2. **User Input:**
   - User types a query in the main text box.

3. **Routing (Based on Mode):**
   - **If Baseline:** Filters photos by exact token match. Shows results.
   - **If Disambiguation & 0 Results:** 
     - Passes query to the Hint Parser.
     - `candidate_photos` is populated based on parsed hints.
     - Enters the Question Loop.

4. **The Question Loop:**
   - Check **Stop Conditions**: 
     - Are there $\le 6$ photos remaining?
     - Have we asked 3 questions?
     - Is the max entropy $0$?
   - If **Yes** -> Break loop, render Results Grid.
   - If **No** -> Calculate entropy, select next attribute, render Question UI and Answer Chips.

5. **User Answers Question:**
   - User taps a chip -> Updates `inferred_hints` in session state.
   - App reruns, narrowing `candidate_photos`. Back to Step 4.

6. **Success & Logging:**
   - User sees the final grid.
   - User clicks "✅ This is it" on the correct photo.
   - Stop timer, calculate `seconds_to_success`.
   - Append data row to `st.session_state.log_data`.
   - Show success banner.

---

## 5. Security & Edge Cases
- **No Infinite Loops:** The "Max 3 Questions" stop condition and the "Not sure" chip prevent the user from getting stuck.
- **Zero Entropy:** If all remaining photos share the exact same attributes, the entropy will be 0, immediately triggering the display grid instead of asking useless questions.
- **Stateless Refresh:** The "Reset session" button gracefully clears `st.session_state` to allow back-to-back testing.
- **Decoupled Search Logic:** The search bar uses `st.form` (or strict `st.session_state.search_submitted` management) so that clicking an answer chip does NOT re-trigger a new search query.
- **Mode Switching Retention:** If the user toggles `search_mode` in the sidebar mid-session, the `current_query` is not cleared. Instead, the application immediately re-processes the existing query under the new mode's logic.
