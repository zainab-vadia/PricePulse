import streamlit as st
import pandas as pd
import random
# Import the new, clean function from main.py
from main import ParseCsv 
import altair as alt

# --- Data Loading and Initialization ---

# Use st.cache_data to ensure the heavy loading/parsing only runs once
@st.cache_data 
def get_processed_data_for_streamlit():
    """Wrapper to load data only once."""
    return ParseCsv()

# Load and unpack the data using caching and populate session state
if 'raw_df' not in st.session_state:
    raw_df, consolidated_data = get_processed_data_for_streamlit()
    #print(raw_df['item_name'])
    st.session_state['raw_df'] = raw_df
    
    # Prepare a simpler summary list for card display and searching
    st.session_state['item_summary'] = [
        {"name": name, 
         "description": data.get("item_description"),
         "image_url": data.get("image_url")}
        for name, data in consolidated_data.items()
    ]
    
    st.session_state['selected_item'] = None



# --- 2. Visualization Function (No changes required) ---

# --- Callback Function for Button Press ---
def select_item_for_graph(item_name):
    """Sets the session state when a 'View Graph' button is clicked."""
    st.session_state['selected_item'] = item_name

# --- 2. Visualization Function ---

def plot_price_history(df_raw, item_name):
    """Generates an Altair line chart for the price history of a selected item."""
    
    # Filter the raw data for the selected item (using lowercase 'item_name' as per previous fix)
    df_filtered = df_raw[df_raw['item_name'] == item_name].copy()
    
    # Check if there is data to plot for the item
    if df_filtered.empty:
        st.warning(f"No price history found in the data for: {item_name}")
        return
        
    # Aggregate to ensure only one price point per day (using the minimum price)
    df_plot = df_filtered.groupby('price_date')['current_price'].min().reset_index()

    st.markdown(f"### Price History for: **{item_name}**")
    
    # Create the Altair chart
    chart = alt.Chart(df_plot).mark_line(point=True).encode(
        x=alt.X('price_date', title='Date', axis=alt.Axis(format='%Y-%m-%d')),
        y=alt.Y('current_price', title='Price ($)'),
        tooltip=['price_date', alt.Tooltip('current_price', format='$,.2f')]
    ).properties(
        title=f"Price Trend over Time"
    ).interactive() 

    st.altair_chart(chart, use_container_width=True)

# --- 3. Streamlit Card Display Function ---

def display_cards(card_data, item_name):
    """
    Displays card info and includes a button with an on_click callback.
    """
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])

        with col1:
            if card_data.get('image_url'):
                st.image(card_data['image_url'], caption=item_name, width=100)
            else:
                st.write("[No Image URL]")
        
        with col2:
            st.markdown(f"### 🃏 **{item_name}**")
            st.write(f"**Description:** {card_data['description']}")
            
            # FIX: Use on_click callback instead of manual state change + st.rerun()
            st.button(
                f"View Price Graph", 
                key=f"btn_{item_name}",
                on_click=select_item_for_graph, # The function to call on click
                args=(item_name,)              # The arguments to pass to the function
            ) 

# --- 4. Main Application ---

def app():
    st.title("Card Data Explorer and Price Tracker 📈")
    
    # --- Price History Graph Section ---
    if st.session_state['selected_item']:
        st.sidebar.header("Selected Item")
        plot_price_history(st.session_state['raw_df'], st.session_state['selected_item'])
        
        # This button is simpler and can use the old method because it's the only one active
        if st.button("⬅️ Back to Card List"):
            st.session_state['selected_item'] = None
            st.rerun()

        st.markdown("---")
    
    # --- Card List and Search Section ---
    
    st.sidebar.header("Search Cards")
    search_query = st.sidebar.text_input(
        "Enter card name or part of description:",
        key="search_input"
    ).lower()

    all_cards = st.session_state['item_summary']

    # Display logic
    if search_query:
        # Search Results logic
        st.header("Search Results")
        
        filtered_cards = [
            card for card in all_cards
            if search_query in card['name'].lower() or search_query in card['description'].lower()
        ]
        
        if filtered_cards:
            st.info(f"Displaying {len(filtered_cards)} matching cards.")
            for card in filtered_cards:
                display_cards(card, card['name'])
        else:
            st.warning("No cards matched your search query.")
            
    elif not st.session_state['selected_item']:
        # Random Cards logic
        st.header("5 Random Cards")
        
        if len(all_cards) >= 5:
            random_cards = random.sample(all_cards, 5)
        else:
            random_cards = all_cards 
            st.warning(f"Only found {len(all_cards)} cards. Displaying all of them.")
            
        for card in random_cards:
            display_cards(card, card['name'])

# Run the Streamlit application
if __name__ == "__main__":
    app()
