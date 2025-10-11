import streamlit as st
import pandas as pd
import random
from main import FinalData
# --- Data Preparation (Mocking the relevant data structure from the parsing) ---

# Mock data representing the item name and description
# In a real app, this would be the output of your ParseCsv function
MOCK_FINAL_DATA = {
    "Mystic Forge": {"item_description": "A legendary artifact that allows you to transform items. Beware the randomness!"},
    "Crimson Blade": {"item_description": "A razor-sharp sword imbued with fire magic. Deals critical damage."},
    "Shield of the Aegis": {"item_description": "A sturdy shield capable of blocking all non-magical attacks. Grants increased defense."},
    "Elixir of Swiftness": {"item_description": "A potent potion that temporarily doubles your movement and attack speed."},
    "Scroll of Teleportation": {"item_description": "Consumes one charge to instantly move to a previously visited location."},
    "Ring of Eternal Frost": {"item_description": "An ancient ring that continuously chills the air around you, slowing nearby enemies."},
    "Glimmering Dust": {"item_description": "Rare material used to upgrade equipment and reveal hidden enchantments."},
    "Shadow Cloak": {"item_description": "A garment woven from pure shadow, granting temporary invisibility to the wearer."},
    "Scepter of Dominance": {"item_description": "Wielded by ancient kings, this scepter increases the power of all your spells."},
    "Golden Compass": {"item_description": "Points toward the nearest treasure or objective. Never loses its direction."}
}

# Store the data in session state to prevent reprocessing on every rerun
if 'card_data' not in st.session_state:
    st.session_state['card_data'] = FinalData

# --- Streamlit App Layout and Logic ---

def display_cards(data_to_display):
    """Displays card name and description in a Streamlit container."""
    
    # Use st.container() for grouping the card display
    with st.container(border=True):
        st.markdown(f"### 🃏 Card: **{data_to_display['item_name']}**")
        st.write(f"**Description:** {data_to_display['item_description']}")

def app():
    st.title("Card Data Explorer and Search 🔍")
    
    # 1. Search Capability Input
    st.sidebar.header("Search Cards")
    search_query = st.sidebar.text_input(
        "Enter card name or part of description:",
        key="search_input"
    ).lower()

    # --- Filtering Logic ---
    
    # Get all card names and descriptions for display/search
    all_cards = [
        {"item_name": name, "item_description": data["item_description"]}
        for name, data in st.session_state['card_data'].items()
    ]

    if search_query:
        # Filter the cards based on the search query
        st.header("Search Results")
        
        filtered_cards = [
            card for card in all_cards
            if search_query in card['item_name'].lower() or search_query in card['item_description'].lower()
        ]
        
        if filtered_cards:
            st.info(f"Displaying {len(filtered_cards)} matching cards.")
            for card in filtered_cards:
                display_cards(card)
        else:
            st.warning("No cards matched your search query.")
            
    else:
        # 2. Display 5 Random Cards (when no search query is active)
        st.header("5 Random Cards")
        
        # Get 5 random cards from the full list
        # Using random.sample to get unique random items
        if len(all_cards) >= 5:
            random_cards = random.sample(all_cards, 5)
        else:
            # Fallback if there are fewer than 5 cards
            random_cards = all_cards 
            st.warning(f"Only found {len(all_cards)} cards. Displaying all of them.")
            
        # Display the random cards
        for card in random_cards:
            display_cards(card)

# Run the Streamlit application
if __name__ == "__main__":
    app()