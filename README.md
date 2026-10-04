# Progressive Contextual Disambiguation MVP

This is a Streamlit web application that simulates an AI-powered fallback search for a mock Google Photos library. 

When a user searches for something vague that returns zero exact matches (e.g., "solo snowy trip"), the app avoids a "dead-end" by launching into **Contextual Disambiguation Mode**. It asks 1-3 targeted follow-up questions to help narrow down the mock library dynamically based on Shannon Entropy logic.

## Features
- **Deterministic Mock Library:** Generates exactly 72 photos on every run. The first 10 photos always feature `palette=purple` and `time_of_day=sunset` for consistent demo testing.
- **Dual Search Modes:** Toggle between traditional exact-match keyword search (Baseline) and the smart fallback logic (Contextual Disambiguation).
- **Shannon Entropy Engine:** Mathematically decides the most effective follow-up question to split the remaining candidate photos.
- **Performance Analytics:** Logs the time taken to find a photo and allows downloading metrics via a CSV export.

## How to Run Locally

1. **Install Dependencies:**
   Ensure you have Python 3.10+ installed. Then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App:**
   ```bash
   streamlit run app.py
   ```

## Testing the "Purple Sunset" Demo
1. Switch to the **With Contextual Disambiguation** mode in the sidebar.
2. Type `purple dusk` in the search bar and press **Search**.
3. The AI will parse "purple" and "dusk" (mapped to sunset), filtering down to the 10 guaranteed demo photos.
4. It will then dynamically ask follow-up questions to narrow it down further.
5. Click **"✅ This is it"** when you find the photo, and download the CSV logs from the sidebar!
