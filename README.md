# Stock Market Dashboard

A comprehensive Indian stock market analysis dashboard built with Streamlit and Plotly.

**[View Live Dashboard](https://kbkb1111-stock-market-dashboard.streamlit.app/)**

## Features

- **Trend Analysis** - Nifty TRI with 40-week SMA
- **Price Channels** - 26-week high / 52-week low bands
- **Nifty vs 10-Year Bond** - Equity-bond relative strength
- **Nifty vs Gold** - Equity-gold relative strength
- **Mid Cap vs Nifty** - Mid cap relative performance
- **Small Cap vs Nifty** - Small cap relative performance
- **Market Breadth Analysis** - Sectors and broad indices above 40w SMA
- **Sector Drawdown** - Average distance from 52-week highs
- **Relative Strength Matrix** - Inter-sector comparison heatmap

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
