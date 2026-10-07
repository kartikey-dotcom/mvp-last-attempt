import streamlit as st

# --- PART 1: THE DATA STRUCTURE ---
# We use a placeholder image service (picsum) for the mock URLs.
MOCK_PHOTOS_DATABASE = [
    {
        "photo_id": "p1",
        "primary_keyword": "white shirt",
        "context_location": "balcony",
        "action_or_object": "holding a coffee cup",
        "image_url": "https://picsum.photos/seed/ws_bal_1/400/400"
    },
    {
        "photo_id": "p2",
        "primary_keyword": "white shirt",
        "context_location": "mountain",
        "action_or_object": "wearing a backpack",
        "image_url": "https://picsum.photos/seed/ws_mtn_1/400/400"
    },
    {
        "photo_id": "p3",
        "primary_keyword": "white shirt",
        "context_location": "cafe",
        "action_or_object": "reading a book",
        "image_url": "https://picsum.photos/seed/ws_caf_1/400/400"
    },
    {
        "photo_id": "p4",
        "primary_keyword": "white shirt",
        "context_location": "balcony",
        "action_or_object": "looking at sunset",
        "image_url": "https://picsum.photos/seed/ws_bal_2/400/400"
    },
    {
        "photo_id": "p5",
        "primary_keyword": "white shirt",
        "context_location": "mountain",
        "action_or_object": "taking a selfie",
        "image_url": "https://picsum.photos/seed/ws_mtn_2/400/400"
    },
    {
        "photo_id": "p6",
        "primary_keyword": "white shirt",
        "context_location": "street",
        "action_or_object": "holding an umbrella",
        "image_url": "https://picsum.photos/seed/ws_str_1/400/400"
    },
    {
        "photo_id": "p7",
        "primary_keyword": "white shirt",
        "context_location": "cafe",
        "action_or_object": "eating dessert",
        "image_url": "https://picsum.photos/seed/ws_caf_2/400/400"
    },
    {
        "photo_id": "p8",
        "primary_keyword": "white shirt",
        "context_location": "beach",
        "action_or_object": "walking on sand",
        "image_url": "https://picsum.photos/seed/ws_bch_1/400/400"
    }
]


# --- PART 2: THE DYNAMIC DISAMBIGUATION LOGIC ---
def generate_next_question(filtered_photos):
    """
    Analyzes remaining photos and determines the best attribute to ask about next.
    Returns: (question_string, list_of_options, attribute_to_filter_by)
    """
    if not filtered_photos:
        return "I couldn't find any photos matching that.", [], None
        
    if len(filtered_photos) == 1:
        return "Found the exact photo!", [], None

    # Gather unique values for our attributes
    unique_locations = list(set([p["context_location"] for p in filtered_photos]))
    unique_actions = list(set([p["action_or_object"] for p in filtered_photos]))

    # Heuristic: Ask about the attribute that splits the dataset best (most unique options)
    # We prioritize location if it hasn't been disambiguated yet.
    if len(unique_locations) > 1:
        # Ask about location
        options_text = ", ".join(unique_locations[:-1]) + f" or {unique_locations[-1]}" if len(unique_locations) > 1 else unique_locations[0]
        question = f"I found {len(filtered_photos)} photos. Where were you? At a {options_text}?"
        return question, unique_locations, "context_location"
    
    elif len(unique_actions) > 1:
        # If location is already singular (or they all share the same location), ask about action
        current_location = unique_locations[0]
        options_text = ", ".join(unique_actions[:-1]) + f" or {unique_actions[-1]}" if len(unique_actions) > 1 else unique_actions[0]
        question = f"I see {len(filtered_photos)} photos at the {current_location}. What were you doing? {options_text.capitalize()}?"
        return question, unique_actions, "action_or_object"
        
    else:
        # Fallback if both attributes are identical
        return "I found some very similar photos!", [], None


# --- PART 3: THE STREAMLIT UI & SESSION STATE ---
def main():
    st.set_page_config(page_title="Guided Recall MVP", layout="centered")

    st.title("🔍 Guided Recall MVP")
    st.write("Search for **'white shirt'** to see the AI chat flow in action.")

    # Initialize session state for our search flow
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "filtered_photos" not in st.session_state:
        st.session_state.filtered_photos = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Search Bar
    query = st.text_input("Search your photos...", placeholder="e.g., white shirt")

    # Detect a new search
    if query != st.session_state.search_query:
        st.session_state.search_query = query
        # Reset filters on new search
        if query.strip():
            # Simple keyword match for the MVP
            st.session_state.filtered_photos = [
                p for p in MOCK_PHOTOS_DATABASE 
                if query.lower() in p["primary_keyword"].lower()
            ]
        else:
            st.session_state.filtered_photos = None
        st.session_state.chat_history = []

    # Main UI Flow
    if st.session_state.filtered_photos is not None:
        current_photos = st.session_state.filtered_photos
        
        # Render the Photo Grid
        st.subheader("Photo Results")
        if not current_photos:
            st.info("No photos found.")
        else:
            # Display dynamically in columns
            cols = st.columns(4)
            for i, photo in enumerate(current_photos):
                with cols[i % 4]:
                    st.image(photo["image_url"], use_column_width=True)
                    st.caption(f"{photo['context_location'].title()} - {photo['action_or_object'].capitalize()}")
            
            st.divider()
            
            # Display the Conversational Assistant
            question, options, attribute = generate_next_question(current_photos)
            
            # Print prior user selections as chat history (adds to the conversational feel)
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # Display the current AI question
            with st.chat_message("assistant"):
                if len(current_photos) > 1:
                    st.write(question)
                    
                    # Render Options as horizontal buttons
                    button_cols = st.columns(len(options))
                    for idx, opt in enumerate(options):
                        if button_cols[idx].button(opt.title(), key=f"btn_{attribute}_{opt}", use_container_width=True):
                            # 1. Save user selection to chat history
                            st.session_state.chat_history.append({"role": "user", "content": f"I was at the {opt}" if attribute == "context_location" else opt.capitalize()})
                            # 2. Filter the photos
                            st.session_state.filtered_photos = [p for p in current_photos if p[attribute] == opt]
                            # 3. Rerun to update UI
                            st.rerun()
                            
                elif len(current_photos) == 1:
                    st.success(question)  # "Found the exact photo!"
                    st.image(current_photos[0]["image_url"], width=500)

if __name__ == "__main__":
    main()
