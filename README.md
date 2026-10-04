# Photos Concept: Contextual Disambiguation

Concept prototype for a PM case study demonstrating progressive contextual disambiguation in a photo search experience. This simulates the experience of a user searching for photos, getting zero immediate results, and interacting with a guided Q&A agent to find exactly what they were looking for.

*Not affiliated with or endorsed by Google. All photos and data are simulated.*

## Features
- Simulated 72-photo mock library with rich metadata.
- Demo seeded to perfectly demonstrate a "purple sunset" flow.
- Exact match vs Disambiguation modes.
- Calculates Shannon entropy across remaining photo candidates to ask the single best question.
- Fully implemented using Streamlit with custom Material Design UI/UX injections.

## Setup & Secrets
To enable the AI-assisted "Guided Recall" features, you need a free Gemini API key:
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. Create a `.streamlit/secrets.toml` file in this directory and add:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
   *Note: This file is ignored by git and will never be committed.*

## Running Locally

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deploying to Streamlit Community Cloud

1. Ensure the code is pushed to a public GitHub repository. The repository must include `app.py` and `requirements.txt`.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app**.
4. Select the GitHub repository, branch, and specify `app.py` as the Main file path.
5. In the advanced settings or app settings, add your `GEMINI_API_KEY` under the Secrets section in TOML format:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
6. Click **Deploy!**
