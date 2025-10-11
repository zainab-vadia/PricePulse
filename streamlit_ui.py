import streamlit as st
import pandas as pd
import random
from main import ParseCsv 
import altair as alt

# --- Configuration and Local Path (Adjust This!) ---
GROCERY_IMAGE_PATH = "images/grocery.jpeg" 
LOGO_IMAGE_PATH = "logo.png" 
FAVICON_PATH = "logo.png" 
NUMBER_OF_RECOMMENDATIONS = 6 

# --- Custom CSS for Styling (MODIFIED FOR IMAGE SIZE FIX) ---
#CUSTOM_CARD_CSS = # --- Custom CSS for Styling (MODIFIED FOR IMAGE SIZE FIX) ---
CUSTOM_CARD_CSS = """
<style>
/* 1. Set the Primary Color for the Pink Button */
:root {
    --primary-color: #ff00ff; /* Bright Magenta/Pink for the Details button */
}

# --- Custom CSS for Styling (FINAL IMAGE SIZE FIX) ---
<style>
/* ... (Keep your other CSS rules for root, h3, p, etc.) ... */

/* 3. Style the Card Container (Rounded Corners, Fixed Height) */
div[data-testid*="stVerticalBlock"] > .stContainer {
    border-radius: 15px; 
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1); 
    overflow: hidden; 
    height: 400px; 
    display: flex; 
    flex-direction: column; 
    justify-content: space-between;
    /* CRITICAL: Ensure the overall card has NO internal top padding */
    padding: 0 0 10px 0 !important; 
}

/* 4. Style the Image Container (Wrapper: div[data-testid="stImage"]) */
div[data-testid="stImage"] {
    /* CRITICAL: Aggressively remove all internal/external spacing */
    margin: 0 !important; 
    padding: 0 !important;
    flex-shrink: 0;
    max_width:100%;
    /* NEW: Remove any border-radius/borders on the container itself */
    border-radius: 0 !important; 
    border: none !important;
}
</style>
"""
# --- Data Loading and Initialization (No Change Needed Here) ---

@st.cache_data 
def get_processed_data_for_streamlit():
    """Wrapper to load data only once."""
    return ParseCsv()

if 'raw_df' not in st.session_state:
    raw_df, consolidated_data = get_processed_data_for_streamlit()
    st.session_state['raw_df'] = raw_df
    
    st.session_state['item_summary'] = [
        {"name": name, 
         "description": data.get("item_description"),
         "image_url": data.get("image_url")} 
        for name, data in consolidated_data.items()
    ]
    
    st.session_state['selected_item'] = None


# --- Callback Function for Button Press (No Change Needed Here) ---
def select_item_for_graph(item_name):
    st.session_state['selected_item'] = item_name

# --- 2. Visualization Function (No Change Needed Here) ---
def plot_price_history(df_raw, item_name):
    df_filtered = df_raw[df_raw['item_name'] == item_name].copy()
    
    if df_filtered.empty:
        st.warning(f"No price history found in the data for: {item_name}")
        return
        
    # Group by date, taking the minimum price found on that date
    df_plot = df_filtered.groupby('price_date')['current_price'].min().reset_index()

    # 1. Calculate Min/Max Prices and find corresponding rows
    min_price = df_plot['current_price'].min()
    max_price = df_plot['current_price'].max()
    
    # Get the data point rows for the min and max prices
    # Use .head(1) in case of ties for the min/max price on different dates
    df_min = df_plot[df_plot['current_price'] == min_price].head(1)
    df_max = df_plot[df_plot['current_price'] == max_price].head(1)
    
    # Combine min and max data points for the text layer
    df_extremes = pd.concat([df_min, df_max]).drop_duplicates(keep='first').reset_index(drop=True)

    st.markdown(f"### Price History for: **{item_name}**")
    
    # Base Line Chart
    line_chart = alt.Chart(df_plot).mark_line(point=True).encode(
        x=alt.X('price_date', title='Date', axis=alt.Axis(format='%Y-%m-%d')),
        y=alt.Y('current_price', title='Price ($)'),
        tooltip=['price_date', alt.Tooltip('current_price', format='$,.2f')]
    )
    
    # Extreme Price Text Layer: Marks the min/max points with their price value
    text_layer = alt.Chart(df_extremes).mark_text(
        align='left',
        baseline='bottom', # Place text above the point
        dy=-5, # Offset text slightly above the point
        color='darkred'
    ).encode(
        x=alt.X('price_date'),
        y=alt.Y('current_price'),
        # Show price as text label
        text=alt.Text('current_price', format='$,.2f'),
        tooltip=['price_date', alt.Tooltip('current_price', format='$,.2f')]
    ).properties(
        # Update the main chart title to show min/max summary
        title=[
            "Price Trend over Time",
            f"Min: ${min_price:.2f}",
            f"Max: ${max_price:.2f}"
        ]
    )
    # Combine the layers
    chart = (line_chart + text_layer).interactive() 
    st.altair_chart(chart, use_container_width=True)


# --- 3. Streamlit Card Display Function (SLIGHTLY MODIFIED) ---

def display_cards(card_data, item_name, col):
    """
    Displays card info in a 3-column format, relying heavily on global CSS for styling.
    """
    with col: 
        # The inner container wrapper is necessary for the CSS styling to apply
        with st.container(): 
            
            # The use_container_width=True is essential here.
            if ("example" in card_data['image_url']):
                st.image(GROCERY_IMAGE_PATH, width=1000, caption="") 
            else:
                st.image(card_data['image_url'], width=1000, caption="") 

            # Use a div wrapper for the content to apply consistent padding via CSS
            st.markdown('<div class="card-content-wrapper">', unsafe_allow_html=True)
            
            # Item Name (Bold and Large)
            st.markdown(f"**{item_name}**") 
            # Description (Smaller and Gray)
            st.markdown(f"{card_data['description']}")
            
            # Details Button 
            st.button(
                "Details", 
                key=f"btn_{item_name}",
                on_click=select_item_for_graph, 
                args=(item_name,),
                use_container_width=True 
            )
            
            st.markdown('</div>', unsafe_allow_html=True)


# --- 4. Main Application ---

def app():
    # Inject Custom CSS at the start
    st.markdown(CUSTOM_CARD_CSS, unsafe_allow_html=True)

    # Set the page configuration
    st.set_page_config(
        page_title="Card Data Explorer",
        page_icon=FAVICON_PATH,
        layout="wide",
    )
    
    # --- Logo and Centered Search Bar Section (No change) ---
    col_logo, col_search_center, col_spacer = st.columns([1, 2, 1])
    with col_logo:
        try:
             st.image(LOGO_IMAGE_PATH, width=100)
        except:
             st.markdown("## **LOGO**") 
             
    with col_search_center:
        search_query = st.text_input(
            "Card Search", 
            placeholder="Search cards...",
            key="search_input",
            label_visibility="collapsed" 
        ).lower()

    st.markdown("---")
    
    # --- Price History Graph Section (No change) ---
    if st.session_state['selected_item']:
        plot_price_history(st.session_state['raw_df'], st.session_state['selected_item'])
        
        if st.button("⬅️ Back to Card List"):
            st.session_state['selected_item'] = None
            st.rerun() 

        st.markdown("---")
    
    # --- Card List and Search Results Section (No change) ---
    all_cards = st.session_state['item_summary']
    
    if search_query:
        st.header(f"Search Results for: '{search_query}'")
        
        filtered_cards = [
            card for card in all_cards
            if search_query in card['name'].lower() or search_query in card['description'].lower()
        ]
        
        if filtered_cards:
            st.info(f"Displaying {len(filtered_cards)} matching cards.")
            card_cols = st.columns(3)
            for i, card in enumerate(filtered_cards):
                display_cards(card, card['name'], card_cols[i % 3])
        else:
            st.warning("No cards matched your search query.")
            
    elif not st.session_state['selected_item']:
        st.header("Top Recommendations ✨")
        
        if len(all_cards) >= NUMBER_OF_RECOMMENDATIONS:
            random_cards = random.sample(all_cards, NUMBER_OF_RECOMMENDATIONS)
        else:
            random_cards = all_cards 
            st.warning(f"Only found {len(all_cards)} cards. Displaying all of them.")
            
        card_cols = st.columns(3)
        for i, card in enumerate(random_cards):
            display_cards(card, card['name'], card_cols[i % 3])

# Run the Streamlit application
if __name__ == "__main__":
    app()
