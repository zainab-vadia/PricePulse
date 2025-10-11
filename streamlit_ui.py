import streamlit as st
import pandas as pd
import random
from main import ParseCsv 
import altair as alt
import hashlib
import json
import os

# --- Authentication Configuration ---
USERS_FILE = "users.json"

# --- User Management Functions ---
def init_users_file():
    """Initialize users file if it doesn't exist"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)

def load_users():
    """Load users from JSON file"""
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user"""
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = hash_password(password)
    save_users(users)
    return True, "Registration successful!"

def authenticate_user(username, password):
    """Authenticate user credentials"""
    users = load_users()
    if username not in users:
        return False
    return users[username] == hash_password(password)

# --- Authentication Pages ---
def login_page():
    """Display login page"""
    st.markdown("""
    <style>
    /* Background gradient - Green theme */
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom input styling */
    .stTextInput > div > div > input {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid #d0d0d0;
        border-radius: 0;
        padding: 10px 5px;
        font-size: 16px;
        color: #666;
    }
    
    .stTextInput > div > div > input:focus {
        border-bottom: 2px solid #11998e;
        box-shadow: none;
    }
    
    /* Custom button styling */
    .stButton > button {
        width: 100%;
        background-color: #f0f0f0;
        color: #333;
        border: 2px solid #333;
        border-radius: 25px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #e0e0e0;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login box
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        # Title
        st.markdown("<h1 style='text-align: center; color: #000; margin-bottom: 40px; margin-top: 80px; font-size: 42px;'>Login</h1>", unsafe_allow_html=True)
        
        # Username input
        username = st.text_input("Username", key="login_username", label_visibility="visible")
        
        # Password input
        password = st.text_input("Password", type="password", key="login_password", label_visibility="visible")
        
        # Forgot password link (non-functional, just for UI)
        st.markdown("<p style='color: #999; font-size: 14px; margin-top: -10px;'>Forget Password?</p>", unsafe_allow_html=True)
        
        # Login button
        if st.button("Login", key="login_btn"):
            if username and password:
                if authenticate_user(username, password):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
        
        # Signup link
        st.markdown("<p style='text-align: center; color: #333; margin-top: 20px;'>Not a Member? <a href='#' style='color: #11998e; text-decoration: none; font-weight: bold;'>Signup</a></p>", unsafe_allow_html=True)
        
        # Invisible button for signup functionality
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_b:
            if st.button("Sign Up Here", key="goto_register"):
                st.session_state['show_register'] = True
                st.rerun()

def register_page():
    """Display registration page"""
    st.markdown("""
    <style>
    /* Background gradient - Green theme */
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom input styling */
    .stTextInput > div > div > input {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid #d0d0d0;
        border-radius: 0;
        padding: 10px 5px;
        font-size: 16px;
        color: #666;
    }
    
    .stTextInput > div > div > input:focus {
        border-bottom: 2px solid #11998e;
        box-shadow: none;
    }
    
    /* Custom button styling */
    .stButton > button {
        width: 100%;
        background-color: #f0f0f0;
        color: #333;
        border: 2px solid #333;
        border-radius: 25px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #e0e0e0;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        # Title
        st.markdown("<h1 style='text-align: center; color: #000; margin-bottom: 40px; margin-top: 80px; font-size: 42px;'>Sign Up</h1>", unsafe_allow_html=True)
        
        username = st.text_input("Username", key="register_username")
        password = st.text_input("Password", type="password", key="register_password")
        password_confirm = st.text_input("Confirm Password", type="password", key="register_password_confirm")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("Create Account", use_container_width=True):
                if username and password and password_confirm:
                    if len(username) < 3:
                        st.error("Username must be at least 3 characters")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    elif password != password_confirm:
                        st.error("Passwords do not match")
                    else:
                        success, message = register_user(username, password)
                        if success:
                            st.success(message)
                            st.info("Please login with your new credentials")
                            st.session_state['show_register'] = False
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields")
        
        with col_btn2:
            if st.button("Back to Login", use_container_width=True):
                st.session_state['show_register'] = False
                st.rerun()

# --- Configuration and Local Path (Adjust This!) ---
GROCERY_IMAGE_PATH = "images/grocery.jpeg" 
LOGO_IMAGE_PATH = "logo.png" 
FAVICON_PATH = "logo.png" 
NUMBER_OF_RECOMMENDATIONS = 6
ShopLinks = {} 
ShopLinks["walmart"]="https://retaillink.login.wal-mart.com/"
ShopLinks["electronics,entertainment,home"] = "https://smarterhouse.org/appliances-energy/home-electronics"

# --- Custom CSS for Styling (MODIFIED FOR IMAGE SIZE FIX) ---
CUSTOM_CARD_CSS = """
<style>
/* 1. Set the Primary Color for the Pink Button */
:root {
    --primary-color: #ff00ff; /* Bright Magenta/Pink for the Details button */
}

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
    max-width:100%;
    /* NEW: Remove any border-radius/borders on the container itself */
    border-radius: 0 !important; 
    border: none !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {
    visibility: hidden;
}
[data-testid="stStatusWidget"] {
    visibility: hidden;
}
.stMainBlockContainer{
    padding: 0;
}
</style>
"""

# --- Data Loading and Initialization (No Change Needed Here) ---

@st.cache_data 
def get_processed_data_for_streamlit():
    """Wrapper to load data only once."""
    return ParseCsv()

def init_session_state():
    """Initialize session state for data"""
    if 'raw_df' not in st.session_state:
        raw_df, consolidated_data = get_processed_data_for_streamlit()
        st.session_state['raw_df'] = raw_df
        
        st.session_state['item_summary'] = [
            {"name": name, 
             "description": data.get("item_description"),
             "image_url": data.get("image_url"),
             "link_to_buy": data.get("link_to_buy"),
             "store": data.get("store")} 
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
            f"Lowest price over time: ${min_price:.2f}",
            f"Highest price over time: ${max_price:.2f}"
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
            col_details, col_shop = st.columns([1, 1])
            
            with col_details:
                # Details Button (Existing functionality)
                st.button(
                    "Details", 
                    key=f"btn_details_{item_name}", # Unique key updated
                    on_click=select_item_for_graph, 
                    args=(item_name,),
                    use_container_width=True 
                )
            
            ShopUrl = card_data['link_to_buy']
            #print(card_data['store'])
            if not ShopUrl:
                if card_data['store'].lower() in ShopLinks:
                    ShopUrl = ShopLinks[card_data['store'].lower()]
                else:
                    ShopUrl = "https://www.example.com"
            #print(ShopUrl)
            with col_shop:
                # NEW: Shop Now Button (Using st.link_button)
                st.link_button(
                    f"🛒 Shop Now",
                    url=ShopUrl,
                    use_container_width=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)


# --- 4. Main Application ---

def app():
    
    # Inject Custom CSS at the start
    st.markdown(CUSTOM_CARD_CSS, unsafe_allow_html=True)
    
    # --- Logo and Centered Search Bar Section (No change) ---
    # Add logout button in top right
    col_spacer1, col_spacer2, col_logout = st.columns([6, 1, 1])
    with col_logout:
        if st.button("Logout"):
            st.session_state['authenticated'] = False
            st.session_state['username'] = None
            st.rerun()
    
    padding, col_logo, col_search_center, col_spacer = st.columns([0.2,1, 3, 0.5])
    with col_logo:
        try:
             st.image(LOGO_IMAGE_PATH, width=200)
             st.image("images/name.png", width=150)
        except:
             st.markdown("## **LOGO**") 
             
    with col_search_center:
        search_query = st.text_input(
            "Card Search", 
            placeholder="Search items or description...",
            key="search_input",
            label_visibility="collapsed" 
        ).lower()
        st.markdown(
            f"<br></br> <p style='text-align: center; color: #555555;'>Your personal window into Canada's inflation trends | Welcome, {st.session_state.get('username', 'User')}!</p>", 
            unsafe_allow_html=True
            )
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
        st.header("Top Recommendations For You✨")
        
        if len(all_cards) >= NUMBER_OF_RECOMMENDATIONS:
            random_cards = random.sample(all_cards, NUMBER_OF_RECOMMENDATIONS)
        else:
            random_cards = all_cards 
            st.warning(f"Only found {len(all_cards)} cards. Displaying all of them.")
            
        card_cols = st.columns(3)
        for i, card in enumerate(random_cards):
            display_cards(card, card['name'], card_cols[i % 3])

# --- Main Entry Point ---
# Set the page configuration FIRST (must be before any other Streamlit commands)
st.set_page_config(
    page_title="Card Data Explorer",
    page_icon="🛒",
    layout="wide",
)

def main():
    # Initialize authentication state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False
    
    # Route to appropriate page
    if not st.session_state['authenticated']:
        if st.session_state['show_register']:
            register_page()
        else:
            login_page()
    else:
        # Initialize data only after authentication
        init_session_state()
        app()

# Run the Streamlit application
if __name__ == "__main__":
    main()
