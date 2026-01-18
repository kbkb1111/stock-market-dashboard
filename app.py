import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, span, div {
        color: #fafafa !important;
    }
    .stDataFrame {
        background-color: #262730;
    }
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    [data-testid="stHeader"] {
        background-color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

# Index Categories
SECTOR_INDICES = ['Auto', 'Bank', 'Energy', 'FMCG', 'Infra', 'IT', 'Media', 'Metal', 'Pharma', 'Realty']
BROAD_INDICES = ['Nifty Next 50', 'Nifty 100', 'Nifty 200', 'Nifty 500', 'Mid Cap 50', 'Mid Cap', 'Small Cap']

# Dark chart theme settings
CHART_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='#0e1117',
    plot_bgcolor='#0e1117',
    font=dict(color='#fafafa'),
    xaxis=dict(
        gridcolor='#333333',
        linecolor='#555555',
        tickcolor='#fafafa',
        title_font=dict(color='#fafafa'),
        tickfont=dict(color='#fafafa')
    ),
    yaxis=dict(
        gridcolor='#333333',
        linecolor='#555555',
        tickcolor='#fafafa',
        title_font=dict(color='#fafafa'),
        tickfont=dict(color='#fafafa')
    ),
    legend=dict(font=dict(color='#fafafa'))
)

@st.cache_data
def load_data():
    """Load and transform the CSV data."""
    df = pd.read_csv('Data.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
    # Remove commas from numbers (e.g., "7,751.60" -> "7751.60")
    df['Spot'] = df['Spot'].astype(str).str.replace(',', '', regex=False)
    df['Spot'] = pd.to_numeric(df['Spot'], errors='coerce')
    # Pivot: rows = Date, columns = Index names, values = Spot prices
    df_pivot = df.pivot(index='Date', columns='Index', values='Spot')
    df_pivot = df_pivot.sort_index()
    return df_pivot

# Load Data
df = load_data()

# Use all data (no filtering)
df_filtered = df

# Main Title
st.title("Stock Market Dashboard")
st.markdown(f"**Data Range:** {df_filtered.index.min().strftime('%d-%b-%Y')} to {df_filtered.index.max().strftime('%d-%b-%Y')}")

# ============================================
# Chart 1: Trend Analysis (Nifty TRI + 40w SMA)
# ============================================
st.header("Trend Analysis")
if 'Nifty TRI' in df_filtered.columns:
    df_chart1 = df_filtered[['Nifty TRI']].copy()
    df_chart1['40w SMA'] = df_chart1['Nifty TRI'].rolling(window=40).mean()

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_chart1.index, y=df_chart1['Nifty TRI'], name='Nifty TRI', line=dict(color='#00BFFF')))
    fig1.add_trace(go.Scatter(x=df_chart1.index, y=df_chart1['40w SMA'], name='40w SMA', line=dict(color='#FF6347', dash='dash')))
    fig1.update_layout(title='Nifty TRI with 40-Week SMA', xaxis_title='Date', yaxis_title='Value', height=400, **CHART_LAYOUT)
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Nifty TRI data not available")

# ============================================
# Chart 2: Price Channels (26w High / 52w Low)
# ============================================
st.header("Price Channels")
if 'Nifty TRI' in df_filtered.columns:
    df_chart2 = df_filtered[['Nifty TRI']].copy()
    df_chart2['26w High'] = df_chart2['Nifty TRI'].shift(1).rolling(window=26).max()
    df_chart2['52w Low'] = df_chart2['Nifty TRI'].shift(1).rolling(window=52).min()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_chart2.index, y=df_chart2['Nifty TRI'], name='Nifty TRI', line=dict(color='#00BFFF')))
    fig2.add_trace(go.Scatter(x=df_chart2.index, y=df_chart2['26w High'], name='26w High', line=dict(color='#32CD32', dash='dot')))
    fig2.add_trace(go.Scatter(x=df_chart2.index, y=df_chart2['52w Low'], name='52w Low', line=dict(color='#FF4500', dash='dot')))
    fig2.update_layout(title='Nifty TRI Price Channels', xaxis_title='Date', yaxis_title='Value', height=400, **CHART_LAYOUT)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Nifty TRI data not available")

# ============================================
# Chart 3: Bond Ratio (Nifty TRI / S&P 10 Yr index)
# ============================================
st.header("Nifty vs 10-Year Bond")
if 'Nifty TRI' in df_filtered.columns and 'S&P 10 Yr index' in df_filtered.columns:
    df_chart3 = pd.DataFrame(index=df_filtered.index)
    df_chart3['Ratio'] = df_filtered['Nifty TRI'] / df_filtered['S&P 10 Yr index']
    df_chart3['40w SMA'] = df_chart3['Ratio'].rolling(window=40).mean()

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_chart3.index, y=df_chart3['Ratio'], name='Nifty TRI / Bond', line=dict(color='#9370DB')))
    fig3.add_trace(go.Scatter(x=df_chart3.index, y=df_chart3['40w SMA'], name='40w SMA', line=dict(color='#FFD700', dash='dash')))
    fig3.update_layout(title='Nifty TRI Relative to 10-Year Bond Index', xaxis_title='Date', yaxis_title='Ratio', height=400, **CHART_LAYOUT)
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Required data (Nifty TRI, S&P 10 Yr index) not available")

# ============================================
# Chart 4: Gold Ratio (Nifty / GoldBees)
# ============================================
st.header("Nifty vs Gold")
if 'Nifty' in df_filtered.columns and 'GoldBees' in df_filtered.columns:
    df_chart4 = pd.DataFrame(index=df_filtered.index)
    df_chart4['Ratio'] = df_filtered['Nifty'] / df_filtered['GoldBees']
    df_chart4['40w SMA'] = df_chart4['Ratio'].rolling(window=40).mean()

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df_chart4.index, y=df_chart4['Ratio'], name='Nifty / Gold', line=dict(color='#FFD700')))
    fig4.add_trace(go.Scatter(x=df_chart4.index, y=df_chart4['40w SMA'], name='40w SMA', line=dict(color='#FF6347', dash='dash')))
    fig4.update_layout(title='Nifty Relative to Gold (GoldBees)', xaxis_title='Date', yaxis_title='Ratio', height=400, **CHART_LAYOUT)
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("Required data (Nifty, GoldBees) not available")

# ============================================
# Chart 5: MidCap Ratio (Mid Cap / Nifty)
# ============================================
st.header("Mid Cap vs Nifty")
if 'Nifty' in df_filtered.columns and 'Mid Cap' in df_filtered.columns:
    df_chart5 = pd.DataFrame(index=df_filtered.index)
    df_chart5['Ratio'] = df_filtered['Mid Cap'] / df_filtered['Nifty']
    df_chart5['40w SMA'] = df_chart5['Ratio'].rolling(window=40).mean()

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=df_chart5.index, y=df_chart5['Ratio'], name='Mid Cap / Nifty', line=dict(color='#20B2AA')))
    fig5.add_trace(go.Scatter(x=df_chart5.index, y=df_chart5['40w SMA'], name='40w SMA', line=dict(color='#FF6347', dash='dash')))
    fig5.update_layout(title='Mid Cap Relative to Nifty', xaxis_title='Date', yaxis_title='Ratio', height=400, **CHART_LAYOUT)
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.warning("Required data (Nifty, Mid Cap) not available")

# ============================================
# Chart 6: SmallCap Ratio (Small Cap / Nifty)
# ============================================
st.header("Small Cap vs Nifty")
if 'Nifty' in df_filtered.columns and 'Small Cap' in df_filtered.columns:
    df_chart6 = pd.DataFrame(index=df_filtered.index)
    df_chart6['Ratio'] = df_filtered['Small Cap'] / df_filtered['Nifty']
    df_chart6['40w SMA'] = df_chart6['Ratio'].rolling(window=40).mean()

    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(x=df_chart6.index, y=df_chart6['Ratio'], name='Small Cap / Nifty', line=dict(color='#BA55D3')))
    fig6.add_trace(go.Scatter(x=df_chart6.index, y=df_chart6['40w SMA'], name='40w SMA', line=dict(color='#FF6347', dash='dash')))
    fig6.update_layout(title='Small Cap Relative to Nifty', xaxis_title='Date', yaxis_title='Ratio', height=400, **CHART_LAYOUT)
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.warning("Required data (Nifty, Small Cap) not available")

# ============================================
# Chart 7: Market Breadth Analysis (3 subplots)
# ============================================
st.header("Market Breadth Analysis")

# Calculate SMAs and count indices above SMA
available_sectors = [idx for idx in SECTOR_INDICES if idx in df_filtered.columns]
available_broad = [idx for idx in BROAD_INDICES if idx in df_filtered.columns]

if available_sectors and available_broad and 'Nifty' in df_filtered.columns:
    # Calculate 40w SMA for each sector index
    sector_above_sma = pd.DataFrame(index=df_filtered.index)
    for sector in available_sectors:
        sma = df_filtered[sector].rolling(window=40).mean()
        sector_above_sma[sector] = (df_filtered[sector] > sma).fillna(False).astype(int)
    sector_count = sector_above_sma.sum(axis=1)

    # Calculate 40w SMA for each broad index
    broad_above_sma = pd.DataFrame(index=df_filtered.index)
    for broad in available_broad:
        sma = df_filtered[broad].rolling(window=40).mean()
        broad_above_sma[broad] = (df_filtered[broad] > sma).fillna(False).astype(int)
    broad_count = broad_above_sma.sum(axis=1)

    # Create subplots
    fig7 = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=('Nifty Price', f'Sectors Above 40w SMA (of {len(available_sectors)})', f'Broad Indices Above 40w SMA (of {len(available_broad)})')
    )

    dates = df_filtered.index.tolist()

    # Subplot 1: Nifty Price
    fig7.add_trace(go.Scatter(x=dates, y=df_filtered['Nifty'].values, name='Nifty', line=dict(color='#00BFFF')), row=1, col=1)

    # Subplot 2: Sector Breadth
    fig7.add_trace(go.Scatter(x=dates, y=sector_count.values, name='Sectors Above SMA', fill='tozeroy', line=dict(color='#32CD32')), row=2, col=1)

    # Subplot 3: Broad Index Breadth
    fig7.add_trace(go.Scatter(x=dates, y=broad_count.values, name='Broad Above SMA', fill='tozeroy', line=dict(color='#FFD700')), row=3, col=1)

    fig7.update_layout(height=700, showlegend=True, **CHART_LAYOUT)
    fig7.update_yaxes(title_text='Price', row=1, col=1)
    fig7.update_yaxes(title_text='Count', range=[0, 10], row=2, col=1)
    fig7.update_yaxes(title_text='Count', range=[0, 7], row=3, col=1)
    st.plotly_chart(fig7, use_container_width=True)
else:
    st.warning("Required sector/broad index data not available")

# ============================================
# Chart 8: Sector Distance from 52-Week High
# ============================================
st.header("Sector Average Drawdown from 52-Week High")

if available_sectors:
    # Calculate drawdown for each sector: (Close - 52WeekMax) / 52WeekMax, capped at 0
    drawdown_df = pd.DataFrame(index=df_filtered.index)
    for sector in available_sectors:
        high_52w = df_filtered[sector].shift(1).rolling(window=52).max()
        drawdown = (df_filtered[sector] - high_52w) / high_52w
        drawdown_df[sector] = drawdown.clip(upper=0)  # Cap at 0 (no positive values)

    # Average of all sector drawdowns (0 = all at highs, negative = below highs)
    avg_drawdown = drawdown_df.mean(axis=1)

    fig8 = go.Figure()
    fig8.add_trace(go.Scatter(x=df_filtered.index.tolist(), y=avg_drawdown.values, name='Average Drawdown', fill='tozeroy', line=dict(color='#FF6347')))
    fig8.update_layout(
        title=f'Sector Average Drawdown from 52-Week Highs ({len(available_sectors)} sectors)',
        xaxis_title='Date',
        yaxis_title='Drawdown (0 = At Highs)',
        height=400,
        **CHART_LAYOUT
    )
    st.plotly_chart(fig8, use_container_width=True)
else:
    st.warning("Sector index data not available")

# ============================================
# Chart 9: Inter Market Relative Strength Matrix
# ============================================
st.header("Inter Market Relative Strength Matrix")

if len(available_sectors) >= 2 and len(df_filtered) > 40:
    # Get latest date and date 4 weeks ago
    latest_date = df_filtered.index[-1]
    date_4w_ago_idx = max(0, len(df_filtered) - 5)  # Approximate 4 weeks back
    date_4w_ago = df_filtered.index[date_4w_ago_idx]

    def calculate_rs_matrix(data):
        """Calculate relative strength matrix for given data slice."""
        n = len(available_sectors)
        matrix = pd.DataFrame(0, index=available_sectors, columns=available_sectors)

        for i, row_idx in enumerate(available_sectors):
            for j, col_idx in enumerate(available_sectors):
                if i != j:
                    ratio = data[row_idx] / data[col_idx]
                    sma_40 = ratio.rolling(window=40).mean()
                    # Check if latest ratio > SMA
                    if len(ratio) > 0 and len(sma_40.dropna()) > 0:
                        if ratio.iloc[-1] > sma_40.iloc[-1]:
                            matrix.loc[row_idx, col_idx] = 1
        return matrix

    # Current matrix
    current_matrix = calculate_rs_matrix(df_filtered)

    # Matrix 4 weeks ago
    df_4w_ago = df_filtered.iloc[:date_4w_ago_idx + 1]
    if len(df_4w_ago) > 40:
        past_matrix = calculate_rs_matrix(df_4w_ago)
    else:
        past_matrix = current_matrix.copy()
        past_matrix[:] = 0

    # Calculate scores
    current_scores = current_matrix.sum(axis=1)
    past_scores = past_matrix.sum(axis=1)
    change = current_scores - past_scores

    # Create summary table
    summary_df = pd.DataFrame({
        'Sector': available_sectors,
        'Current Score': current_scores.values,
        'Score 4W Ago': past_scores.values,
        'Change': change.values
    })
    summary_df['Rank'] = summary_df['Current Score'].rank(ascending=False, method='dense').astype(int)
    summary_df = summary_df.sort_values('Rank')

    # Display Matrix as Heatmap
    col1, col2 = st.columns([2, 1])

    with col1:
        # Create heatmap with Y/N labels
        fig9 = go.Figure(data=go.Heatmap(
            z=current_matrix.values,
            x=current_matrix.columns,
            y=current_matrix.index,
            colorscale=[[0, '#FF4136'], [1, '#2ECC40']],
            showscale=False,
            text=current_matrix.replace({0: 'N', 1: 'Y'}).values,
            texttemplate='%{text}',
            textfont={"size": 12}
        ))
        fig9.update_layout(
            title='Relative Strength Matrix (Row vs Column)',
            height=450,
            xaxis_title='Column Index',
            yaxis_title='Row Index',
            **CHART_LAYOUT
        )
        st.plotly_chart(fig9, use_container_width=True)

    with col2:
        st.subheader("Sector Rankings")
        # Style the dataframe
        st.dataframe(
            summary_df.style.background_gradient(subset=['Current Score'], cmap='RdYlGn')
                          .background_gradient(subset=['Change'], cmap='RdYlGn', vmin=-5, vmax=5),
            hide_index=True,
            height=400
        )
else:
    st.warning("Insufficient sector data for matrix calculation (need at least 40 weeks)")

# Footer
st.markdown("---")
st.markdown("*Dashboard updates when Data.csv is modified and app is restarted.*")
