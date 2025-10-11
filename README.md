# 🥦 Inflation Insight Dashboard

### *Your personal window into Canada’s inflation trends*

This Streamlit web app visualizes grocery price trends using data parsed from a CSV file.  
It allows users to search for grocery items, explore historical price data, and access store links — all in a clean, modern interface.

---

## 🚀 Features
- **Interactive Search:** Quickly find items by name or description.  
- **Dynamic Charts:** Explore price trends over time with interactive Altair visualizations.  
- **Shop Links:** Directly open relevant store or product pages.  
- **Modern UI:** Fully custom CSS for cards, buttons, and layout.

---

## 🗂️ Project Structure
```
📦 inflation-insight-dashboard/
├── main.py                # Contains ParseCsv() for reading and preparing data
├── app.py                 # Main Streamlit application
├── images/
│   ├── grocery.jpeg
│   ├── name.png
│   └── ...
├── logo.png               # App logo and favicon
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/inflation-insight-dashboard.git
   cd inflation-insight-dashboard
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit
   pip install pandas
   ```

---

## ▶️ Run the App

Start the Streamlit app:
```bash
streamlit run app.py
```

Then open the URL provided in the terminal (usually `http://localhost:8501/`).

---

## 📊 How It Works

1. **Data Loading**
   - Uses `ParseCsv()` from `main.py` to load and preprocess CSV data.  
   - Returns:
     - `raw_df`: Raw data with price history.
     - `consolidated_data`: Summary info for each item.

2. **Dashboard Flow**
   - Displays logo, search bar, and recommended cards.
   - Each card includes:
     - Image + Description  
     - “Details” button → shows price history  
     - “Shop Now” button → opens external link  

3. **Visualization**
   - Altair line chart of historical prices with min/max highlights.  
   - Interactive hover tooltips.

---

## 🧩 Customization
You can modify constants at the top of `app.py`:
- **`NUMBER_OF_RECOMMENDATIONS`** → how many random cards show by default  
- **`ShopLinks`** → add or update store URLs  
- **Images/Logos** → replace files under `images/`  

To change theme or layout, edit the `CUSTOM_CARD_CSS` string.

---

## 🧾 License
This project is licensed under the **MIT License**.

---

## 💡 Credits
Built with ❤️ using [Streamlit](https://streamlit.io/), [Altair](https://altair-viz.github.io/), and [Pandas](https://pandas.pydata.org/).
