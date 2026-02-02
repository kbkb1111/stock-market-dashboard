# Stock Market Dashboard

A comprehensive Indian stock market analysis dashboard built with Streamlit and Plotly.

**[View Live Dashboard](https://kbkb1111-stock-market-dashboard.streamlit.app/)**

## Disclaimer

This is not financial advice. This is a personal analytical project for educational purposes only.

## Features

- **Time Period Filter** - Radio buttons to toggle between 5 Years, 10 Years, and All Data views
- **Chart Descriptions** - Each visual includes a short caption explaining what it shows and how to interpret it
- **Nifty Total Return Index with 40-Week SMA** - Trend analysis with moving average
- **Nifty Total Return Index with Price Channels** - 26-week high / 52-week low bands
- **Nifty Total Return Index vs 10-Year Bond Index** - Equity-bond relative strength
- **Nifty vs Gold** - Equity-gold relative strength
- **Mid Cap vs Nifty** - Mid cap relative performance
- **Small Cap vs Nifty** - Small cap relative performance
- **Market Breadth Analysis** - Sectors and broad indices above 40w SMA
- **Sector Drawdown** - Average distance from 52-week highs
- **Relative Strength Matrix** - Inter-sector comparison heatmap (always uses full data, unaffected by time filter)

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Local Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Updating Data

1. Replace `Data.csv` with updated data
2. Run locally to verify
3. Push to GitHub (auto-deploys to Streamlit Cloud)

## Changelog

### 2 Feb 2026
- Added time period filter buttons (5 Years, 10 Years, All Data) that filter all charts except the Relative Strength Matrix
- Rolling indicators (40w SMA, 52w high/low, etc.) are computed on the full dataset before slicing, ensuring accuracy at the start of filtered ranges
- Added disclaimer at the top of the dashboard
- Added short descriptive captions below each chart header explaining the visual and how to interpret it
- Updated Relative Strength Matrix description with detailed explanation and example
- Fixed stale data on Streamlit Cloud: `@st.cache_data` now uses the CSV file's modification time as a cache key, so the cache automatically refreshes when `Data.csv` is updated
