# Stock Market Dashboard Implementation Plan (Streamlit)

## Goal Description
Create a personal Stock Market Dashboard using **Streamlit** to visualize historical index data. The dashboard will support a workflow where data is updated locally in CSV format, verified locally, and then pushed to GitHub to trigger an automatic update on the deployed version (Streamlit Community Cloud).

## User Review Required
> [!IMPORTANT]
> - **Data Privacy**: The data will be hosted in a public GitHub repository (unless you use a private repo with Streamlit auth). Ensure `Data.csv` does not contain sensitive personal info.
> - **Deployment**: We will use Streamlit Community Cloud, which connects directly to your GitHub account.
> - **No Raw Data**: The final dashboard will NOT show raw data tables.

## Implemented Features

### Tech Stack
- **Language**: Python
- **Framework**: Streamlit
- **Data Manipulation**: Pandas
- **Visualization**: Plotly (interactive charts with dark theme)

### Architecture

#### `app.py` (Main Entry Point)
- **Settings**: `st.set_page_config(layout="wide")`
- **Theme**: Full dark theme via CSS injection and `.streamlit/config.toml`
- **No Sidebar Filters**: All data displayed by default (filters removed per user request)
- **Main Area**:
  - Title & Data Range display
  - 9 Charts (see below)
  - *Note: No raw data table displayed.*

#### Data Layer (inline in `app.py`)
- `load_data()` function decorated with `@st.cache_data`.
- Reads `Data.csv` using `pd.read_csv`.
- Parses dates: `pd.to_datetime(df['Date'], format='%d-%b-%y')`.
- **Handles comma-separated numbers**: Removes commas before converting to numeric (e.g., "7,751.60" → 7751.60).
- Pivots data: rows = Date, columns = Index names, values = Spot prices.
- **Index Categorization**:
  - **Sector Indices**: Auto, Bank, Energy, FMCG, Infra, IT, Media, Metal, Pharma, Realty (10 total)
  - **Broad Indices**: Nifty Next 50, Nifty 100, Nifty 200, Nifty 500, Mid Cap 50, Mid Cap, Small Cap (7 total)

#### Charts Implementation

- **Trend Analysis**
  - **Metric**: Nifty TRI (Total Return Index)
  - **Overlays**: 40-week Simple Moving Average (SMA)
  - **Logic**: `df['Nifty TRI'].rolling(window=40).mean()`

- **Price Channels**
  - **Metric**: Nifty TRI
  - **Overlays**:
    - **26-Week High**: Previous 26 weeks high (excluding current week)
      - Logic: `df['Nifty TRI'].shift(1).rolling(window=26).max()`
    - **52-Week Low**: Previous 52 weeks low (excluding current week)
      - Logic: `df['Nifty TRI'].shift(1).rolling(window=52).min()`

- **Nifty vs 10-Year Bond**
  - **Metric**: Ratio = `Nifty TRI` / `S&P 10 Yr index`
  - **Overlays**: 40-week SMA of the Ratio

- **Nifty vs Gold**
  - **Metric**: Ratio = `Nifty` / `GoldBees`
  - **Overlays**: 40-week SMA

- **Mid Cap vs Nifty**
  - **Metric**: Ratio = `Mid Cap` / `Nifty`
  - **Overlays**: 40-week SMA
  - *Note: Inverted from original plan to show Mid Cap relative strength*

- **Small Cap vs Nifty**
  - **Metric**: Ratio = `Small Cap` / `Nifty`
  - **Overlays**: 40-week SMA
  - *Note: Inverted from original plan to show Small Cap relative strength*

- **Market Breadth Analysis**
  - **Layout**: 3 vertical subplots
  - **Subplot 1 (Top)**: Nifty Price
  - **Subplot 2 (Middle)**: Number of Sector Indices (10) trading above their 40-week SMA
  - **Subplot 3 (Bottom)**: Number of Broad Indices (7) trading above their 40-week SMA
  - **NaN Handling**: Uses `.fillna(False)` for proper comparison

- **Sector Average Drawdown from 52-Week High**
  - **Metric**: Average Drawdown of Sector Indices
  - **Logic**:
    - For each Sector Index: `Drawdown = (Close - 52WeekMax) / 52WeekMax`
    - 52-Week Max excludes current week: `.shift(1).rolling(window=52).max()`
    - Drawdown capped at 0 (no positive values): `.clip(upper=0)`
    - **Average**: Mean of all 10 sector drawdowns
  - *Interpretation*: 0 = all sectors at highs, negative = sectors below highs

- **Inter Market Relative Strength Matrix**
  - **Type**: Heatmap + Rankings Table
  - **Entities**: 10 Sector Indices (Row vs Column)
  - **Logic**:
    - For each pair (Row A, Col B):
      - `Ratio = Price(A) / Price(B)`
      - `Condition = Ratio > RollingSMA(Ratio, 40)`
      - `Cell Value`: 1 (Y) if True, 0 (N) if False
    - **Score**: Sum of row values
    - **Score 4W Ago**: Calculation for 4 weeks prior
    - **Change**: Current Score - Score 4W Ago
    - **Rank**: Dense rank by Current Score (descending)
  - **Visuals**: Green/Red heatmap with Y/N labels, rankings table with color gradients

### Dark Theme Configuration

#### CSS Injection (in `app.py`)
```css
.stApp { background-color: #0e1117; color: #fafafa; }
[data-testid="stSidebar"] { background-color: #262730; }
```

#### Chart Theme (`CHART_LAYOUT` dict)
- `paper_bgcolor`: #0e1117
- `plot_bgcolor`: #0e1117
- `gridcolor`: #333333
- `font color`: #fafafa

#### `.streamlit/config.toml`
```toml
[theme]
base = "dark"
primaryColor = "#FF6347"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
```

### Deployment Workflow
1. **Local Update**:
   - User replaces `Data.csv` in the local folder
   - Run `python -m streamlit run app.py`
   - Check dashboard for correctness
2. **Publish**:
   - Git add, commit, and push changes to GitHub
   - Streamlit Cloud detects the commit and auto-updates the app

## Verification Plan

### Manual Verification (Local)
1. **Data Integrity**: Check if the latest date in the CSV appears in the app
2. **Visuals**: Ensure all 9 charts render correctly with dark theme
3. **Requirement Check**: Confirm NO raw data tables are visible

### Deployment Verification
1. Push a minor change and verify the Streamlit app updates online
