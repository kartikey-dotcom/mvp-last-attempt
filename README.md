# Google Photos Guided Recall (MVP)

A working prototype of a "Guided Recall" search engine for a personal photo library.

## Features
- **48-Photo Curated Library**: 6 categories (Mountain, Beach, Cafe, Concert, Street, Balcony) x 8 photos each, designed to test disambiguation.
- **Current Search (Baseline)**: Simulates a standard keyword search. Requires the user to type exactly the right objective tags to narrow down results.
- **Contextual Disambiguation**: Takes a vague query (e.g. "mountains"), extracts known attributes (category, time of day, weather, companion, shirt colour), and deterministically asks Yes/No/Not sure questions to narrow down the results to the exact photo you want.
- **Live Disambiguation Engine**: Uses binary entropy calculations to ask the mathematically optimal question to split the remaining candidates.
- **Researcher Tools**: A built-in Photo Inspector to verify the test data, and detailed CSV logging to capture task success rate, time, and number of questions asked.

## Running Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run Streamlit: `streamlit run app.py`

## Testing
1. Run `pytest tests/test_engine.py` to verify the deterministic disambiguation logic.
