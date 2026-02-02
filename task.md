# Stock Market Dashboard Data Visualization (Streamlit)

- [x] **Project Setup / Foundation**
    - [/] Set up Python virtual environment (User to handle env creation, I provide requirements)
    - [x] Create `requirements.txt` (streamlit, pandas, plotly)
    - [x] Create main application file `app.py`
    - [x] Create `.streamlit/config.toml` for dark theme
    - [x] Initialize Git repository

- [x] **Data Processing Layer (Python)**
    - [x] Implement data loader using `pandas`
    - [x] Add caching with `@st.cache_data` for performance
    - [x] Implement data transformation logic (Date parsing, comma removal for numbers, Index grouping)
    - [x] Implement calculations for all 9 Charts

- [x] **UI Implementation (Streamlit)**
    - [x] **App Layout**
        - [x] Configure `st.set_page_config` (Title, Layout, Dark Theme)
        - [x] Dark theme CSS styling applied
        - [x] Sidebar filters removed (showing all data by default)
    - [x] **Dashboard Components**
        - [x] Nifty Total Return Index with 40-Week SMA
        - [x] Nifty Total Return Index with Price Channels
        - [x] Nifty Total Return Index vs 10-Year Bond Index
        - [x] Nifty vs Gold (Ratio + 40w SMA)
        - [x] Mid Cap vs Nifty (Mid Cap / Nifty + 40w SMA)
        - [x] Small Cap vs Nifty (Small Cap / Nifty + 40w SMA)
        - [x] Market Breadth Analysis (3 subplots: Nifty, Sectors above SMA, Broad indices above SMA)
        - [x] Sector Average Drawdown from 52-Week High
        - [x] Inter Market Relative Strength Matrix
    - [x] **Data View**
        - [x] (Removed per user request)

- [x] **Workflow & Deployment**
    - [x] Verify local execution (`streamlit run app.py`)
    - [x] Commit `Data.csv` and code to GitHub
    - [x] Deploy to Streamlit Community Cloud
    - [x] Document update process (Replace CSV -> Run Local -> Push)

- [x] **Enhancements (2 Feb 2026)**
    - [x] Time period filter buttons (5 Years, 10 Years, All Data)
    - [x] Rolling indicators computed on full data before slicing for accuracy
    - [x] Relative Strength Matrix excluded from time filtering (always uses all data)
    - [x] Disclaimer added at top of dashboard
    - [x] Descriptive captions added below each chart header
    - [x] Updated Relative Strength Matrix description with detailed example
