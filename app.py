import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import math
from itertools import combinations
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

#####################################################################

# If the app doesn't run, try changing dir then running from commandline.
# cd "/Users/daranjjohnson/Library/CloudStorage/GoogleDrive-daranjjohnson@gmail.com/My Drive/PROFESSIONAL/Projects/py_streamlit_apps/mmm_with_mta"

# It might work to just run it.
# Use the --server.headless true if you don't want it to open in a browser.
# streamlit run app.py --server.headless true

# Better to create virtual environment (in this case, with Python 3.13).
# /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m venv streamlit_env

# Activate it.
# source streamlit_env/bin/activate

# Verify the version.
# python --version  # Should show 3.13

# Now run app streamlit - this forces it to use
# the Python version from your active virtual environment.
# python -m streamlit run app.py

# Use the --server.headless true if you don't want it to open in a browser.
# python -m streamlit run app.py --server.headless true

# There is a commandline file: run_streamlit.sh that can be run from the terminal
# with './run_streamlit.sh'

# We created the file with the following steps:
#  nano run_streamlit.sh
# An interface pops up. Type these lines in the interface:
# #!/bin/zsh
# cd "/Users/daranjjohnson/Library/CloudStorage/GoogleDrive-daranjjohnson@gmail.com/My Drive/PROFESSIONAL/Projects/daranjjohnson/20250920 Streamlit App - MMM with MTA"
# source streamlit_env/bin/activate
# python -m streamlit run app.py
# Press Ctrl + O to save and Enter to confirm, then Ctrl x to exit the interface.
# Now the flie is created and saved.
# Then the following was run to make it executable:
# chmod +x run_streamlit.sh
# Finally - to run the commands in the file that start the app
# type the following in the commandline:
# ./run_streamlit.sh

#####################################################################

# Set page config
st.set_page_config(
    page_title="MMM + MTA Analytics Platform",
    page_icon="\U0001f4ca",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .main { padding: 1rem 2rem; background: linear-gradient(180deg, #fafbfc 0%, #ffffff 100%); }
    .main-header {
        font-size: 2.8rem; font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 1rem; letter-spacing: -0.5px;
    }
    .sub-header { font-size: 1rem; color: #6b7280; text-align: center; margin-bottom: 2.5rem; font-weight: 400; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
        padding: 0.75rem; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border: 1px solid #e5e7eb;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px; padding: 0 24px; background: white; border-radius: 8px;
        border: 1px solid #e5e7eb; color: #4b5563; font-weight: 500; font-size: 14px;
        letter-spacing: 0.3px; transition: all 0.3s ease; box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #f3f4f6 0%, #ffffff 100%); border-color: #9ca3af;
        transform: translateY(-1px); box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important; border: none !important;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2) !important;
    }
    .metric-container {
        background: white; padding: 1.5rem; border-radius: 12px; margin: 0.75rem 0;
        border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.06); transition: all 0.3s ease;
    }
    .metric-container:hover { box-shadow: 0 4px 6px rgba(0,0,0,0.1); transform: translateY(-2px); }
    [data-testid="metric-container"] {
        background: white; padding: 1.25rem; border-radius: 10px;
        border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.06); transition: all 0.2s ease;
    }
    [data-testid="metric-container"]:hover { box-shadow: 0 3px 6px rgba(0,0,0,0.1); transform: translateY(-1px); }
    [data-testid="metric-container"] label { font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #1f2937; font-family: 'Roboto Mono', monospace; }
    .css-1d391kg, .st-emotion-cache-1d391kg { background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%); border-right: 1px solid #e5e7eb; }
    .sidebar .sidebar-content { background: transparent; }
    .stSelectbox > div > div { background: white; border-radius: 8px; border: 1px solid #d1d5db; transition: all 0.2s ease; }
    .stSelectbox > div > div:hover { border-color: #9ca3af; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        padding: 0.6rem 1.5rem; border-radius: 8px; font-weight: 600; font-size: 14px;
        letter-spacing: 0.3px; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3); }
    .stCheckbox { font-size: 14px; color: #4b5563; }
    .stSlider > div > div { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); }
    .stSlider [data-baseweb="slider-track"] { background: #e5e7eb; }
    .stSlider [data-baseweb="slider-track-filled"] { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); }
    .dataframe { border: 1px solid #e5e7eb !important; border-radius: 8px !important; overflow: hidden; }
    .dataframe thead th { background: #f8f9fa !important; font-weight: 600 !important; color: #374151 !important; text-transform: uppercase; font-size: 12px !important; letter-spacing: 0.5px; padding: 12px !important; }
    .dataframe tbody tr:hover { background: #f3f4f6 !important; }
    .js-plotly-plot { border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); overflow: hidden; }
    .stSpinner > div { color: #667eea; }
    h1 { font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem; }
    h2 { font-size: 1.8rem; font-weight: 600; color: #374151; margin-top: 1.5rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #e5e7eb; }
    h3 { font-size: 1.3rem; font-weight: 600; color: #4b5563; margin-top: 1rem; margin-bottom: 0.75rem; }
    .info-box { background: linear-gradient(135deg, #f3f4f6 0%, #ffffff 100%); border-left: 4px solid #667eea; padding: 1rem 1.5rem; border-radius: 8px; margin: 1rem 0; }
    .stAlert { border-radius: 8px; border: 1px solid; font-size: 14px; }
    hr { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #e5e7eb 50%, transparent 100%); margin: 2rem 0; }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 2rem; }
    .custom-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #e5e7eb; margin-bottom: 1.5rem; }
    .custom-card-title { font-size: 1.1rem; font-weight: 600; color: #374151; margin-bottom: 0.75rem; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    .loading { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def generate_synthetic_data():
    np.random.seed(123)
    start_date = datetime(2023, 1, 1)
    end_date   = datetime(2024, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='W')
    n = len(dates)

    facebook   = np.random.uniform(0, 10000, n)
    affiliates = np.random.uniform(0, 5000,  n)
    search     = np.random.uniform(0, 3000,  n)
    display    = np.random.uniform(0, 2000,  n)

    base  = 11000 + np.sin(2 * np.pi * np.arange(1, n + 1) / 52) * 10
    noise = np.random.normal(0, 5, n)
    sales = base + 0.3*facebook + 0.4*affiliates + 0.5*search + 0.6*display + noise

    return pd.DataFrame({
        'date': dates,
        'week': dates.isocalendar().week,
        'year': dates.year,
        'Facebook':   facebook,
        'Affiliates': affiliates,
        'Search':     search,
        'Display':    display,
        'sales':      np.round(sales, 1),
    })


@st.cache_data
def generate_customer_journey_data(df, customers_per_week=500):
    np.random.seed(123)
    all_journeys = []

    for _, row in df.iterrows():
        week_date   = row['date']
        n_customers = np.random.poisson(customers_per_week)
        customer_ids = [f"CUST_{week_date.strftime('%Y%m%d')}_{j:04d}" for j in range(1, n_customers + 1)]

        journeys, conversions, revenues = [], [], []
        for _ in range(n_customers):
            journey_length = np.random.choice([1, 2, 3, 4], p=[0.4, 0.35, 0.2, 0.05])
            if journey_length == 1:
                channel = np.random.choice(['Facebook', 'Search', 'Display', 'Affiliates'], p=[0.4, 0.35, 0.15, 0.1])
            elif journey_length == 2:
                channel = np.random.choice(
                    ['Facebook > Search', 'Display > Search', 'Facebook > Display',
                     'Affiliates > Search', 'Search > Facebook', 'Display > Facebook'],
                    p=[0.3, 0.25, 0.2, 0.1, 0.1, 0.05])
            elif journey_length == 3:
                channel = np.random.choice(
                    ['Facebook > Display > Search', 'Display > Facebook > Search',
                     'Facebook > Affiliates > Search', 'Display > Affiliates > Search',
                     'Search > Facebook > Display', 'Affiliates > Facebook > Search'],
                    p=[0.25, 0.2, 0.2, 0.15, 0.1, 0.1])
            else:
                channel = np.random.choice(
                    ['Facebook > Display > Affiliates > Search',
                     'Display > Facebook > Affiliates > Search',
                     'Facebook > Search > Display > Affiliates',
                     'Display > Search > Facebook > Affiliates'],
                    p=[0.4, 0.3, 0.2, 0.1])

            journeys.append(channel)

            if 'Search' in channel:              conv_rate = 0.8
            elif 'Facebook' in channel and 'Search' in channel: conv_rate = 0.75
            elif 'Display'  in channel and 'Search' in channel: conv_rate = 0.7
            elif len(channel.split(' > ')) == 1: conv_rate = 0.4
            else:                                conv_rate = 0.6

            conversion = np.random.binomial(1, conv_rate)
            conversions.append(conversion)

            if conversion == 1:
                base_rev = 150
                if 'Facebook'   in channel: base_rev *= 1.2
                if 'Search'     in channel: base_rev *= 1.3
                if 'Affiliates' in channel: base_rev *= 1.1
                if 'Display'    in channel: base_rev *= 1.05
                if len(channel.split(' > ')) > 2: base_rev *= 1.1
                revenues.append(round(max(0, np.random.normal(base_rev, base_rev * 0.3)), 2))
            else:
                revenues.append(0)

        all_journeys.append(pd.DataFrame({
            'Customer_ID': customer_ids,
            'Path':        journeys,
            'Conversion':  conversions,
            'Revenue':     revenues,
            'Date':        week_date,
        }))

    return pd.concat(all_journeys, ignore_index=True)


# ── Transform helpers ──────────────────────────────────────────────────────────

def apply_adstock(spend, decay_rate):
    """Geometric adstock: captures advertising carryover effects week-over-week"""
    adstocked    = np.zeros_like(spend, dtype=float)
    adstocked[0] = spend[0]
    for t in range(1, len(spend)):
        adstocked[t] = spend[t] + decay_rate * adstocked[t - 1]
    return adstocked


def apply_hill_saturation(spend, alpha, K):
    """Hill saturation: captures diminishing returns as spend increases"""
    return spend ** alpha / (spend ** alpha + K ** alpha)


def preprocess_channels(data, transform_params=None):
    """Apply adstock then Hill saturation to all channel columns.

    Pass transform_params from a prior training call to reuse fitted K values
    (required for consistent scaling at prediction/scenario time).
    Returns (transformed_data, fitted_params).
    """
    channels      = ['Facebook', 'Affiliates', 'Search', 'Display']
    default_decays = {'Facebook': 0.7, 'Affiliates': 0.3, 'Search': 0.2, 'Display': 0.5}

    data_out      = data.copy()
    fitted_params = {}

    for ch in channels:
        decay     = default_decays[ch]
        adstocked = apply_adstock(data_out[ch].values, decay)

        if transform_params is not None:
            alpha = transform_params[ch]['alpha']
            K     = transform_params[ch]['K']
        else:
            alpha   = 2.0
            nonzero = adstocked[adstocked > 0]
            K       = float(np.percentile(nonzero, 50)) if len(nonzero) > 0 else 1.0

        fitted_params[ch] = {'decay': decay, 'alpha': alpha, 'K': K}
        data_out[ch]      = apply_hill_saturation(adstocked, alpha, K)

    return data_out, fitted_params


# ── MTA methods ────────────────────────────────────────────────────────────────

def calculate_markov_attribution(customer_data):
    """Markov chain attribution using removal effects.

    Builds a transition probability matrix, then for each channel computes
    how much conversion probability drops when that channel is removed.
    Attribution = each channel's removal effect as a fraction of the total.
    """
    paths       = customer_data['Path'].tolist()
    conversions = customer_data['Conversion'].tolist()

    channels   = sorted({ch for path in paths for ch in path.split(' > ')})
    all_states = ['(start)'] + channels + ['(conv)', '(null)']
    idx        = {s: i for i, s in enumerate(all_states)}
    n          = len(all_states)

    counts = np.zeros((n, n))
    for path, conv in zip(paths, conversions):
        ch_list = path.split(' > ')
        counts[idx['(start)'], idx[ch_list[0]]] += 1
        for k in range(len(ch_list) - 1):
            counts[idx[ch_list[k]], idx[ch_list[k + 1]]] += 1
        counts[idx[ch_list[-1]], idx['(conv)' if conv else '(null)']] += 1

    row_sums            = counts.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = counts / row_sums

    absorbing = [idx['(conv)'], idx['(null)']]
    transient = [i for i in range(n) if i not in absorbing]

    def conv_prob(matrix):
        Q = matrix[np.ix_(transient, transient)]
        R = matrix[np.ix_(transient, absorbing)]
        try:
            N = np.linalg.inv(np.eye(len(transient)) - Q)
        except np.linalg.LinAlgError:
            N = np.linalg.pinv(np.eye(len(transient)) - Q)
        B = N @ R
        return B[transient.index(idx['(start)']), 0]

    base   = conv_prob(T)
    removal = {}
    for ch in channels:
        T_mod = T.copy()
        ch_i  = idx[ch]
        for i in range(n):
            if i != ch_i and T_mod[i, ch_i] > 0:
                T_mod[i, idx['(null)']] += T_mod[i, ch_i]
                T_mod[i, ch_i]           = 0.0
        T_mod[ch_i, :] = 0.0
        T_mod[ch_i, idx['(null)']] = 1.0
        removal[ch] = max(0.0, base - conv_prob(T_mod))

    total       = sum(removal.values()) or 1.0
    total_convs = sum(conversions)
    return pd.DataFrame([
        {'channel_name': ch, 'total_conversions': removal[ch] / total * total_convs,
         'fraction': removal[ch] / total}
        for ch in channels
    ])


def calculate_equal_weight_attribution(customer_data):
    """Equal weight (linear) attribution: splits conversion credit evenly across all touchpoints"""
    paths       = customer_data['Path'].tolist()
    conversions = customer_data['Conversion'].tolist()

    channels    = sorted({ch for path in paths for ch in path.split(' > ')})
    attribution = {ch: 0.0 for ch in channels}
    for path, conv in zip(paths, conversions):
        if conv:
            ch_list = path.split(' > ')
            credit  = 1.0 / len(ch_list)
            for ch in ch_list:
                attribution[ch] += credit

    total = sum(attribution.values()) or 1.0
    return pd.DataFrame([
        {'channel_name': ch, 'total_conversions': attribution[ch],
         'fraction': attribution[ch] / total}
        for ch in channels
    ])


def calculate_shapley_attribution(customer_data):
    """Shapley value attribution.

    Treats each channel as a player in a cooperative game. The value v(S) is
    estimated as the conversion rate of paths containing only channels in S.
    Each channel's Shapley value is its average marginal contribution across
    all possible orderings — the theoretically fairest credit allocation.
    """
    paths       = customer_data['Path'].tolist()
    conversions = customer_data['Conversion'].tolist()

    channels = sorted({ch for path in paths for ch in path.split(' > ')})
    n        = len(channels)

    subset_stats: dict = {}
    for path, conv in zip(paths, conversions):
        key = frozenset(path.split(' > '))
        if key not in subset_stats:
            subset_stats[key] = {'conversions': 0, 'count': 0}
        subset_stats[key]['conversions'] += conv
        subset_stats[key]['count']       += 1

    def v(S):
        S_frozen = frozenset(S)
        total_conv = total_count = 0
        for key, s in subset_stats.items():
            if key.issubset(S_frozen):
                total_conv  += s['conversions']
                total_count += s['count']
        return total_conv / total_count if total_count > 0 else 0.0

    shapley = {ch: 0.0 for ch in channels}
    for ch in channels:
        others = [c for c in channels if c != ch]
        for k in range(len(others) + 1):
            for subset in combinations(others, k):
                S        = list(subset)
                marginal = v(S + [ch]) - v(S)
                weight   = math.factorial(k) * math.factorial(n - k - 1) / math.factorial(n)
                shapley[ch] += weight * marginal

    total_pos   = sum(max(0.0, sv) for sv in shapley.values()) or 1.0
    total_convs = sum(conversions)
    return pd.DataFrame([
        {'channel_name': ch,
         'total_conversions': max(0.0, shapley[ch]) / total_pos * total_convs,
         'fraction':          max(0.0, shapley[ch]) / total_pos}
        for ch in channels
    ])


def calculate_mta(customer_data, method='markov'):
    """Dispatch to the selected MTA method"""
    if method == 'equal':   return calculate_equal_weight_attribution(customer_data)
    if method == 'markov':  return calculate_markov_attribution(customer_data)
    if method == 'shapley': return calculate_shapley_attribution(customer_data)
    raise ValueError(f"Unsupported MTA method: {method}")


# ── MMM model training ─────────────────────────────────────────────────────────

def train_mmm_models(data):
    """Train MMM models on raw spend with adstock + Hill saturation transforms.

    Runs fully independently of MTA — no attribution weighting applied.
    Returns (models, transformed_data, transform_params). transform_params must
    be passed to preprocess_channels() at scenario/prediction time so K values
    are consistent with training.
    """
    channels = ['Facebook', 'Affiliates', 'Search', 'Display']

    data_transformed, transform_params = preprocess_channels(data)

    features = ['week', 'year'] + channels
    X        = data_transformed[features]
    y        = data_transformed['sales']

    models            = {}
    models['lm']      = LinearRegression()
    models['lm'].fit(X, y)
    models['ridge']   = Ridge(alpha=1.0)
    models['ridge'].fit(X, y)
    models['xgb']     = xgb.XGBRegressor(n_estimators=100, random_state=123, verbosity=0)
    models['xgb'].fit(X, y)

    return models, data_transformed, transform_params


def calculate_incremental_contributions(data, models, model_type):
    """Counterfactual channel contributions: full_pred minus zeroed-channel pred for each channel"""
    channels  = ['Facebook', 'Affiliates', 'Search', 'Display']
    features  = ['week', 'year'] + channels
    model     = models[model_type]

    full_pred     = model.predict(data[features])
    baseline_data = data.copy()
    baseline_data[channels] = 0
    baseline_pred = model.predict(baseline_data[features])

    contributions = {}
    for ch in channels:
        tmp     = data.copy()
        tmp[ch] = 0
        contributions[f'{ch}_contr'] = full_pred - model.predict(tmp[features])

    result                  = data.copy()
    result['full_pred']     = full_pred
    result['baseline_pred'] = baseline_pred
    for key, vals in contributions.items():
        result[key] = vals

    return result


# ── Main app ───────────────────────────────────────────────────────────────────

def main():
    st.markdown('<h1 class="main-header">MMM + MTA Analytics Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Independent Marketing Mix Modeling & Multi-Touch Attribution — each measuring what it does best</p>', unsafe_allow_html=True)

    if 'df' not in st.session_state:
        with st.spinner('Initializing analytics engine...'):
            st.session_state.df            = generate_synthetic_data()
            st.session_state.customer_data = generate_customer_journey_data(st.session_state.df)

    df            = st.session_state.df
    customer_data = st.session_state.customer_data

    # ── Sidebar ───────────────────────────────────────────────────────────────
    st.sidebar.markdown("## Configuration")
    st.sidebar.markdown("---")

    st.sidebar.markdown("### MMM Model")
    model_type = st.sidebar.selectbox(
        "Choose MMM Model:",
        options=['lm', 'ridge', 'xgb'],
        format_func=lambda x: {
            'lm':    'Linear + Adstock + Hill',
            'ridge': 'Ridge + Adstock + Hill',
            'xgb':   'XGBoost + Adstock + Hill',
        }[x],
        help="All models apply geometric adstock (carryover) and Hill saturation (diminishing returns) before fitting"
    )

    st.sidebar.markdown("### MTA Method")
    mta_method = st.sidebar.selectbox(
        "Attribution Model:",
        options=['markov', 'equal', 'shapley'],
        format_func=lambda x: {
            'markov':  'Markov Chain (Removal Effects)',
            'equal':   'Equal Weight',
            'shapley': 'Shapley Values',
        }[x],
        help="Runs independently of MMM. Markov uses removal effects; Shapley values are game-theoretically optimal"
    )

    st.sidebar.markdown("### Display Options")
    show_ci = st.sidebar.checkbox("Show Confidence Bands", value=True)
    st.sidebar.markdown("---")

    # ── Compute ───────────────────────────────────────────────────────────────
    with st.spinner('Running MMM and MTA models independently...'):
        all_mta    = {m: calculate_mta(customer_data, m) for m in ['markov', 'equal', 'shapley']}
        mta_result = all_mta[mta_method]
        models, data_transformed, transform_params = train_mmm_models(df)
        df_pred    = calculate_incremental_contributions(data_transformed, models, model_type)

    # ── Shared constants ──────────────────────────────────────────────────────
    CHANNELS     = ['Facebook', 'Affiliates', 'Search', 'Display']
    CH_COLORS    = {'Facebook': '#1877f2', 'Search': '#ea4335', 'Display': '#00a950', 'Affiliates': '#ff6900'}
    MODEL_LABELS = {
        'lm':    'Linear + Adstock + Hill',
        'ridge': 'Ridge + Adstock + Hill',
        'xgb':   'XGBoost + Adstock + Hill',
    }
    MTA_LABELS = {'markov': 'Markov Chain', 'equal': 'Equal Weight', 'shapley': 'Shapley Values'}

    mmm_total_all = sum(df_pred[f'{ch}_contr'].sum() for ch in CHANNELS)
    total_spend   = df[CHANNELS].sum().sum()
    total_revenue = customer_data['Revenue'].sum()
    total_convs   = int(customer_data['Conversion'].sum())

    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Total Spend",   f"${total_spend:,.0f}")
    st.sidebar.metric("Total Revenue", f"${total_revenue:,.0f}")
    st.sidebar.metric("Conversions",   f"{total_convs:,}")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Overview",
        "MMM Results",
        "MTA Results",
        "Triangulation",
        "Channel Deep Dive",
        "Scenario Planning",
    ])

    # =========================================================================
    # TAB 1 — Overview
    # =========================================================================
    with tab1:
        st.markdown("### Platform Overview")

        col1, col2, col3, col4, col5 = st.columns(5)
        conv_rate   = customer_data['Conversion'].mean() * 100
        avg_rev     = customer_data[customer_data['Conversion'] == 1]['Revenue'].mean()
        avg_journey = customer_data['Path'].apply(lambda x: len(x.split(' > '))).mean()
        with col1: st.metric("Customers",    f"{len(customer_data):,}")
        with col2: st.metric("Conversions",  f"{total_convs:,}")
        with col3: st.metric("Conv. Rate",   f"{conv_rate:.1f}%")
        with col4: st.metric("Avg. Revenue", f"${avg_rev:.2f}")
        with col5: st.metric("Avg. Journey", f"{avg_journey:.1f} steps")

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"#### MMM: Channel Sales Contributions")
            st.caption(f"Model: {MODEL_LABELS[model_type]} | Adstock + Hill saturation applied to raw spend")
            ch_contrib = {ch: df_pred[f'{ch}_contr'].sum() for ch in CHANNELS}
            ov_df = pd.DataFrame([
                {'Channel': ch, 'Contribution': ch_contrib[ch]}
                for ch in CHANNELS
            ]).sort_values('Contribution', ascending=False)
            fig = px.bar(ov_df, x='Channel', y='Contribution', color='Channel',
                         color_discrete_map=CH_COLORS,
                         text=ov_df['Contribution'].apply(lambda v: f"${v:,.0f}"),
                         labels={'Contribution': 'Incremental Sales ($)'})
            fig.update_traces(textposition='outside')
            fig.update_layout(height=350, showlegend=False,
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(family='Inter, sans-serif'), xaxis_title='')
            fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### MTA: Attribution Comparison (All 3 Methods)")
            st.caption("Each method assigns conversion credit differently — compare to see where they agree")
            cmp_rows = [
                {'Channel': row['channel_name'], 'Method': MTA_LABELS[m],
                 'Attribution %': round(row['fraction'] * 100, 1)}
                for m, result in all_mta.items()
                for _, row in result.iterrows()
            ]
            fig2 = px.bar(pd.DataFrame(cmp_rows), x='Channel', y='Attribution %',
                          color='Method', barmode='group',
                          color_discrete_map={
                              'Markov Chain': '#667eea',
                              'Equal Weight': '#9ca3af',
                              'Shapley Values': '#764ba2'})
            fig2.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                               font=dict(family='Inter, sans-serif'), xaxis_title='',
                               legend=dict(orientation='h', y=1.02))
            fig2.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="info-box">
            <strong>MMM answers:</strong> How much did each channel's spend <em>cause</em> sales to increase?
            Measured as a counterfactual — what would sales have been if that channel had spent zero?
            Captures long-run brand effects, carryover, and diminishing returns.
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="info-box">
            <strong>MTA answers:</strong> Among customers who converted, how much <em>credit</em>
            does each touchpoint deserve? Captures path sequencing and last-mile dynamics.
            Use for bid optimisation — not for measuring incremental sales lift.
            </div>""", unsafe_allow_html=True)

    # =========================================================================
    # TAB 2 — MMM Results
    # =========================================================================
    with tab2:
        st.markdown(f"### Marketing Mix Model — {MODEL_LABELS[model_type]}")
        st.caption("Runs on raw spend with adstock and Hill saturation. No MTA weighting applied.")

        # A: Contributions over time + ROI cards
        col1, col2 = st.columns([2, 1])
        with col1:
            contrib_rows = [
                {'date': row['date'], 'Channel': ch, 'Contribution': row[f'{ch}_contr']}
                for _, row in df_pred.iterrows() for ch in CHANNELS
            ]
            fig = px.area(pd.DataFrame(contrib_rows), x='date', y='Contribution', color='Channel',
                          title="Incremental Channel Contributions Over Time",
                          labels={'Contribution': 'Incremental Sales ($)', 'date': 'Date'},
                          color_discrete_map=CH_COLORS)
            fig.update_layout(height=420, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(family='Inter, sans-serif'), hovermode='x unified',
                              legend=dict(orientation='h', y=1.02))
            fig.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
            fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Channel ROI")
            for ch in CHANNELS:
                contrib = df_pred[f'{ch}_contr'].sum()
                roi     = contrib / df[ch].sum() * 100
                pct     = contrib / mmm_total_all * 100
                c       = CH_COLORS[ch]
                st.markdown(
                    f'<div style="border-left:4px solid {c};padding:.7rem 1rem;margin:.4rem 0;'
                    f'background:white;border-radius:0 8px 8px 0;border:1px solid #e5e7eb;border-left:4px solid {c};">'
                    f'<b style="color:#374151">{ch}</b><br>'
                    f'<span style="color:#6b7280;font-size:13px">${contrib:,.0f} ({pct:.1f}% of media)</span><br>'
                    f'<span style="color:#6b7280;font-size:13px">ROI: {roi:.0f}%</span></div>',
                    unsafe_allow_html=True)

        st.markdown("---")

        # B: Model fit + decomposition
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Actual vs Predicted Sales")
            y_true      = data_transformed['sales'].values
            y_pred_vals = df_pred['full_pred'].values
            ss_res = np.sum((y_true - y_pred_vals) ** 2)
            ss_tot = np.sum((y_true - y_true.mean()) ** 2)
            r2   = 1 - ss_res / ss_tot
            rmse = np.sqrt(np.mean((y_true - y_pred_vals) ** 2))
            st.caption(f"R² = {r2:.3f}  |  RMSE = {rmse:.1f}")
            fig_fit = go.Figure()
            fig_fit.add_trace(go.Scatter(x=df_pred['date'], y=y_true, mode='markers',
                                          name='Actual', marker=dict(size=4, color='#374151', opacity=0.6)))
            fig_fit.add_trace(go.Scatter(x=df_pred['date'], y=y_pred_vals, mode='lines',
                                          name='Predicted', line=dict(color='#667eea', width=2)))
            fig_fit.update_layout(height=340, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family='Inter, sans-serif'), hovermode='x unified',
                                   legend=dict(orientation='h', y=1.02))
            fig_fit.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
            fig_fit.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_fit, use_container_width=True)

        with col2:
            st.markdown("#### Sales Decomposition by Year")
            st.caption("Baseline = organic sales with zero media spend")
            tmp = df_pred.copy()
            tmp['year'] = tmp['date'].dt.year
            decomp = tmp.groupby('year').agg(
                Baseline=('baseline_pred', 'sum'),
                **{ch: (f'{ch}_contr', 'sum') for ch in CHANNELS}
            ).reset_index()
            fig_dc = go.Figure()
            fig_dc.add_trace(go.Bar(x=decomp['year'].astype(str), y=decomp['Baseline'],
                                     name='Baseline', marker_color='#e5e7eb'))
            for ch in CHANNELS:
                fig_dc.add_trace(go.Bar(x=decomp['year'].astype(str), y=decomp[ch],
                                         name=ch, marker_color=CH_COLORS[ch]))
            fig_dc.update_layout(barmode='stack', height=340,
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family='Inter, sans-serif'), legend=dict(orientation='h', y=1.02))
            fig_dc.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_dc, use_container_width=True)

        st.markdown("---")

        # C: Adstock & saturation
        st.markdown("#### Adstock Decay & Saturation Curves")
        st.caption("Adstock shows carry-over from prior weeks; saturation shows where spend hits diminishing returns")
        ch_sel = st.selectbox("Select channel:", CHANNELS, key='mmm_ch')

        decay    = transform_params[ch_sel]['decay']
        alpha    = transform_params[ch_sel]['alpha']
        K        = transform_params[ch_sel]['K']
        raw_vals = df[ch_sel].values
        ads_vals = apply_adstock(raw_vals, decay)

        col1, col2 = st.columns(2)
        with col1:
            fig_ads = go.Figure()
            fig_ads.add_trace(go.Bar(x=df['date'], y=raw_vals, name='Raw Spend',
                                      marker_color=CH_COLORS[ch_sel], opacity=0.45))
            fig_ads.add_trace(go.Scatter(x=df['date'], y=ads_vals, mode='lines',
                                          name=f'Adstocked (λ={decay})',
                                          line=dict(color=CH_COLORS[ch_sel], width=2)))
            fig_ads.update_layout(title=f"{ch_sel}: Raw vs Adstocked Spend", height=310,
                                   plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family='Inter, sans-serif'), hovermode='x unified',
                                   legend=dict(orientation='h', y=1.02))
            fig_ads.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
            fig_ads.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_ads, use_container_width=True)

        with col2:
            x_range  = np.linspace(0, ads_vals.max() * 1.5, 300)
            y_range  = apply_hill_saturation(x_range, alpha, K)
            avg_ads  = ads_vals.mean()
            avg_sat  = apply_hill_saturation(avg_ads, alpha, K)
            peak_ads = ads_vals.max()
            peak_sat = apply_hill_saturation(peak_ads, alpha, K)

            fig_sat = go.Figure()
            fig_sat.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines', name='Hill saturation',
                                          line=dict(color=CH_COLORS[ch_sel], width=2)))
            fig_sat.add_trace(go.Scatter(x=[avg_ads], y=[avg_sat], mode='markers',
                                          name=f'Avg spend ({avg_sat*100:.0f}% sat)',
                                          marker=dict(size=12, color=CH_COLORS[ch_sel])))
            fig_sat.add_trace(go.Scatter(x=[peak_ads], y=[peak_sat], mode='markers',
                                          name=f'Peak spend ({peak_sat*100:.0f}% sat)',
                                          marker=dict(size=12, color='#ef4444', symbol='diamond')))
            fig_sat.add_vline(x=K, line_dash='dot', line_color='#9ca3af',
                               annotation_text='50% saturation', annotation_position='top right')
            fig_sat.update_layout(
                title=f"{ch_sel}: Hill Saturation (α={alpha}, K={K:.0f})",
                xaxis_title='Adstocked Spend ($)', yaxis_title='Saturation (0–1)',
                height=310, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter, sans-serif'), legend=dict(orientation='h', y=1.02),
                yaxis=dict(range=[0, 1.05]))
            fig_sat.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
            fig_sat.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_sat, use_container_width=True)

            sat_pct = avg_sat * 100
            if sat_pct > 75:
                st.warning(f"{ch_sel} is at {sat_pct:.0f}% saturation — strong diminishing returns above current spend.")
            elif sat_pct > 50:
                st.info(f"{ch_sel} is at {sat_pct:.0f}% saturation — moderate room to scale.")
            else:
                st.success(f"{ch_sel} is at {sat_pct:.0f}% saturation — significant room to increase spend efficiently.")

    # =========================================================================
    # TAB 3 — MTA Results
    # =========================================================================
    with tab3:
        st.markdown(f"### Multi-Touch Attribution — {MTA_LABELS[mta_method]}")
        st.caption("Runs on customer journey data only. No MMM inputs used.")

        # A: Attribution comparison
        st.markdown("#### Attribution Split by Method")
        col1, col2 = st.columns([2, 1])

        with col1:
            cmp_rows = [
                {'Channel': row['channel_name'], 'Method': MTA_LABELS[m],
                 'Attribution %': round(row['fraction'] * 100, 1)}
                for m, result in all_mta.items()
                for _, row in result.iterrows()
            ]
            fig_cmp = px.bar(pd.DataFrame(cmp_rows), x='Channel', y='Attribution %',
                             color='Method', barmode='group', text='Attribution %',
                             color_discrete_map={
                                 'Markov Chain': '#667eea',
                                 'Equal Weight': '#9ca3af',
                                 'Shapley Values': '#764ba2'},
                             title="All 3 MTA Methods Side by Side")
            fig_cmp.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_cmp.update_layout(height=370, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family='Inter, sans-serif'), legend=dict(orientation='h', y=1.02))
            fig_cmp.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_cmp, use_container_width=True)

        with col2:
            st.markdown(f"#### {MTA_LABELS[mta_method]}")
            for _, row in mta_result.sort_values('fraction', ascending=False).iterrows():
                ch  = row['channel_name']
                pct = row['fraction'] * 100
                c   = CH_COLORS.get(ch, '#667eea')
                st.markdown(
                    f'<div style="border-left:4px solid {c};padding:.7rem 1rem;margin:.4rem 0;'
                    f'background:white;border-radius:0 8px 8px 0;border:1px solid #e5e7eb;border-left:4px solid {c};">'
                    f'<b style="color:#374151">{ch}</b><br>'
                    f'<span style="color:#6b7280;font-size:13px">{pct:.1f}% of attribution</span><br>'
                    f'<span style="color:#6b7280;font-size:13px">{int(row["total_conversions"]):,} attributed conversions</span>'
                    f'</div>',
                    unsafe_allow_html=True)

        st.markdown("---")

        # B: Journey patterns + path length
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Top Journey Patterns")
            jsum = (customer_data.groupby('Path')
                    .agg(Count=('Customer_ID', 'count'), Conv_Rate=('Conversion', 'mean'))
                    .reset_index().sort_values('Count', ascending=False).head(12))
            fig_j = px.bar(jsum, x='Count', y='Path', orientation='h',
                           color='Conv_Rate', color_continuous_scale='Viridis',
                           labels={'Conv_Rate': 'Conv Rate'},
                           title="Top 12 Paths (coloured by conversion rate)")
            fig_j.update_layout(height=420, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                 font=dict(family='Inter, sans-serif'),
                                 yaxis={'categoryorder': 'total ascending'})
            fig_j.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_j, use_container_width=True)

        with col2:
            st.markdown("#### Journey Length Analysis")
            cd2 = customer_data.copy()
            cd2['length'] = cd2['Path'].apply(lambda p: len(p.split(' > ')))
            len_stats = cd2.groupby('length').agg(
                Count=('Customer_ID', 'count'),
                Conv_Rate=('Conversion', 'mean')
            ).reset_index()
            fig_l = make_subplots(rows=1, cols=2, subplot_titles=('Volume', 'Conversion Rate'))
            fig_l.add_trace(go.Bar(x=len_stats['length'].astype(str), y=len_stats['Count'],
                                    marker_color='#667eea', name='Count'), row=1, col=1)
            fig_l.add_trace(go.Bar(x=len_stats['length'].astype(str),
                                    y=(len_stats['Conv_Rate'] * 100).round(1),
                                    marker_color='#764ba2', name='Conv %'), row=1, col=2)
            fig_l.update_layout(height=420, showlegend=False,
                                 plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                 font=dict(family='Inter, sans-serif'))
            fig_l.update_xaxes(title_text='# Touchpoints')
            fig_l.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_l, use_container_width=True)

        st.markdown("---")

        # C: Touch position + co-occurrence
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Touchpoint Position Analysis")
            pos_rows = []
            for _, row in customer_data.iterrows():
                ch_list = row['Path'].split(' > ')
                n_ch    = len(ch_list)
                for i, ch in enumerate(ch_list):
                    if n_ch == 1:        label = 'Only Touch'
                    elif i == 0:         label = 'First Touch'
                    elif i == n_ch - 1:  label = 'Last Touch'
                    else:                label = 'Middle Touch'
                    pos_rows.append({'Channel': ch, 'Position': label})
            pos_df  = pd.DataFrame(pos_rows)
            pos_sum = pos_df.groupby(['Channel', 'Position']).size().reset_index(name='Count')
            fig_pos = px.bar(pos_sum, x='Channel', y='Count', color='Position', barmode='stack',
                             color_discrete_map={
                                 'Only Touch': '#667eea', 'First Touch': '#10b981',
                                 'Last Touch': '#f59e0b', 'Middle Touch': '#9ca3af'},
                             title="Channel Touchpoint Positions")
            fig_pos.update_layout(height=360, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family='Inter, sans-serif'), legend=dict(orientation='h', y=1.02))
            st.plotly_chart(fig_pos, use_container_width=True)

        with col2:
            st.markdown("#### Channel Co-occurrence Heatmap")
            st.caption("% of journeys where both channels appear together")
            ch_order = ['Facebook', 'Search', 'Display', 'Affiliates']
            comat    = np.zeros((4, 4))
            for path in customer_data['Path']:
                ch_set = set(path.split(' > '))
                for i, c1 in enumerate(ch_order):
                    for j, c2 in enumerate(ch_order):
                        if c1 in ch_set and c2 in ch_set:
                            comat[i, j] += 1
            comat_pct = pd.DataFrame(comat / len(customer_data) * 100, index=ch_order, columns=ch_order)
            fig_hm    = px.imshow(comat_pct, text_auto='.1f', color_continuous_scale='Blues',
                                   title="Co-occurrence (% of all journeys)")
            fig_hm.update_layout(height=360, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family='Inter, sans-serif'))
            st.plotly_chart(fig_hm, use_container_width=True)

    # =========================================================================
    # TAB 4 — Triangulation
    # =========================================================================
    with tab4:
        st.markdown("### MMM vs MTA Triangulation")
        st.caption(f"MMM model: {MODEL_LABELS[model_type]}  |  MTA method: {MTA_LABELS[mta_method]}")

        comp_rows = []
        for ch in CHANNELS:
            mmm_pct = df_pred[f'{ch}_contr'].sum() / mmm_total_all * 100
            mta_row = mta_result[mta_result['channel_name'] == ch]
            mta_pct = float(mta_row['fraction'].iloc[0]) * 100 if len(mta_row) > 0 else 0
            gap     = mmm_pct - mta_pct
            if abs(gap) <= 8:
                signal, interp, badge = (
                    "Agreement",
                    "Both models align — high confidence in this channel's value",
                    "#10b981")
            elif gap > 8:
                signal, interp, badge = (
                    "MMM > MTA",
                    "Channel creates demand not visible in journeys (brand lift, halo, awareness)",
                    "#3b82f6")
            else:
                signal, interp, badge = (
                    "MTA > MMM",
                    "Channel captures existing demand more than it creates it (re-targeting, last-click bias)",
                    "#f59e0b")
            comp_rows.append({'Channel': ch, 'MMM %': round(mmm_pct, 1), 'MTA %': round(mta_pct, 1),
                               'Gap': round(gap, 1), 'Signal': signal,
                               'Interpretation': interp, 'badge': badge})
        comp_df = pd.DataFrame(comp_rows)

        col1, col2 = st.columns([3, 2])
        with col1:
            fig_tri = go.Figure()
            fig_tri.add_trace(go.Bar(name='MMM %', x=comp_df['Channel'], y=comp_df['MMM %'],
                                      marker_color='#667eea',
                                      text=comp_df['MMM %'].apply(lambda v: f"{v:.1f}%"),
                                      textposition='outside'))
            fig_tri.add_trace(go.Bar(name=f'MTA % ({MTA_LABELS[mta_method]})',
                                      x=comp_df['Channel'], y=comp_df['MTA %'],
                                      marker_color='#764ba2',
                                      text=comp_df['MTA %'].apply(lambda v: f"{v:.1f}%"),
                                      textposition='outside'))
            fig_tri.update_layout(barmode='group', height=420,
                                   title="Channel Attribution Share: MMM vs MTA",
                                   plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family='Inter, sans-serif'),
                                   yaxis_title='Share of Attribution (%)',
                                   legend=dict(orientation='h', y=1.02))
            fig_tri.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_tri, use_container_width=True)

        with col2:
            st.markdown("#### Signal per Channel")
            for _, row in comp_df.iterrows():
                st.markdown(
                    f'<div style="border-left:4px solid {row["badge"]};padding:.7rem 1rem;margin:.4rem 0;'
                    f'background:white;border-radius:0 8px 8px 0;border:1px solid #e5e7eb;border-left:4px solid {row["badge"]};">'
                    f'<b style="color:#374151">{row["Channel"]} &mdash; {row["Signal"]}</b><br>'
                    f'<span style="color:#6b7280;font-size:12px">{row["Interpretation"]}</span><br>'
                    f'<span style="color:#9ca3af;font-size:11px">MMM: {row["MMM %"]:.1f}% | MTA: {row["MTA %"]:.1f}% | Gap: {row["Gap"]:+.1f}pp</span>'
                    f'</div>',
                    unsafe_allow_html=True)

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="custom-card"><div class="custom-card-title">Agreement</div>
            <p style="font-size:13px;color:#6b7280">Both models assign similar credit. Highest-confidence signal.
            Safe to use MMM ROI for budget planning.</p></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="custom-card"><div class="custom-card-title">MMM &gt; MTA</div>
            <p style="font-size:13px;color:#6b7280">Channel drives sales not visible in conversion journeys —
            typically brand awareness, view-through, or offline lift. MTA undercounts this channel.</p></div>""",
            unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="custom-card"><div class="custom-card-title">MTA &gt; MMM</div>
            <p style="font-size:13px;color:#6b7280">Channel appears in converting paths but its incremental lift is lower.
            Likely capturing demand rather than creating it. Investigate with a holdout test before scaling.</p></div>""",
            unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Strategic Recommendations")
        for _, row in comp_df.iterrows():
            ch_roi = df_pred[f"{row['Channel']}_contr"].sum() / df[row['Channel']].sum() * 100
            if row['Signal'] == 'Agreement':
                st.markdown(f"- **{row['Channel']}** ({row['Signal']}): Strong evidence from both models. "
                            f"Use MMM ROI of **{ch_roi:.0f}%** for budget decisions with confidence.")
            elif row['Signal'] == 'MMM > MTA':
                st.markdown(f"- **{row['Channel']}** ({row['Signal']}): Likely undervalued in MTA. "
                            f"Use MMM ROI (**{ch_roi:.0f}%**) for planning; validate with geo holdout test.")
            else:
                st.markdown(f"- **{row['Channel']}** ({row['Signal']}): May be capturing rather than creating demand. "
                            f"Run an incrementality test before scaling beyond current ROI of **{ch_roi:.0f}%**.")

    # =========================================================================
    # TAB 5 — Channel Deep Dive
    # =========================================================================
    with tab5:
        st.markdown("### Channel Deep Dive")
        st.caption("MMM contribution analysis combined with MTA journey insights for one channel")

        ch_dive = st.selectbox("Select channel:", CHANNELS, key='dive_ch')
        color   = CH_COLORS[ch_dive]

        st.markdown("---")
        st.markdown("#### MMM Performance")
        col1, col2, col3, col4 = st.columns(4)
        ch_total = df_pred[f'{ch_dive}_contr'].sum()
        ch_avg   = df_pred[f'{ch_dive}_contr'].mean()
        ch_max   = df_pred[f'{ch_dive}_contr'].max()
        ch_roi   = ch_total / df[ch_dive].sum() * 100
        with col1: st.metric("Total Contribution", f"${ch_total:,.0f}")
        with col2: st.metric("Avg Weekly",          f"${ch_avg:,.0f}")
        with col3: st.metric("Peak Week",            f"${ch_max:,.0f}")
        with col4: st.metric("ROI",                  f"{ch_roi:.0f}%")

        # Time series with CI and trend
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(
            x=df_pred['date'], y=df_pred[f'{ch_dive}_contr'], mode='lines',
            name=f'{ch_dive} Contribution',
            line=dict(width=3, color=color), fill='tozeroy',
            fillcolor=f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.1)'))
        if show_ci:
            y_v = df_pred[f'{ch_dive}_contr']
            y_m = y_v.rolling(4, center=True).mean()
            y_s = y_v.rolling(4, center=True).std()
            fig_ts.add_trace(go.Scatter(x=df_pred['date'], y=y_m + 1.96 * y_s, mode='lines',
                                         line_color='rgba(0,0,0,0)', showlegend=False))
            fig_ts.add_trace(go.Scatter(x=df_pred['date'], y=y_m - 1.96 * y_s, mode='lines',
                                         fill='tonexty', line_color='rgba(0,0,0,0)',
                                         name='95% Band',
                                         fillcolor=f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15)'))
        z = np.polyfit(range(len(df_pred)), df_pred[f'{ch_dive}_contr'], 1)
        fig_ts.add_trace(go.Scatter(x=df_pred['date'], y=np.poly1d(z)(range(len(df_pred))),
                                     mode='lines', name='Trend',
                                     line=dict(dash='dash', width=2, color='gray')))
        fig_ts.update_layout(
            title=f"{ch_dive} Incremental Contribution Over Time",
            xaxis_title='Date', yaxis_title='Incremental Sales ($)', height=400,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif'), hovermode='x unified',
            legend=dict(orientation='h', y=1.02))
        fig_ts.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
        fig_ts.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        st.plotly_chart(fig_ts, use_container_width=True)

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### MMM Insights")
            monthly = df_pred.groupby(df_pred['date'].dt.month)[f'{ch_dive}_contr'].mean()
            peak_m  = monthly.idxmax()
            low_m   = monthly.idxmin()
            eff     = ch_total / df[ch_dive].sum()
            trend   = np.polyfit(range(len(df_pred)), df_pred[f'{ch_dive}_contr'], 1)[0]
            vol     = df_pred[f'{ch_dive}_contr'].std() / df_pred[f'{ch_dive}_contr'].mean() * 100
            st.markdown(
                f'<div class="custom-card"><div class="custom-card-title">Seasonality & Efficiency</div>'
                f'<ul style="margin:0;padding-left:1.2rem;color:#6b7280;font-size:13px">'
                f'<li>Peak Month: {peak_m} &nbsp;|&nbsp; Low Month: {low_m}</li>'
                f'<li>Seasonal variation: {((monthly.max()-monthly.min())/monthly.mean()*100):.1f}%</li>'
                f'<li>Spend efficiency: ${eff:.2f} per $1 spent</li>'
                f'<li>Weekly trend: ${trend:.2f} per week</li>'
                f'<li>Volatility (CV): {vol:.1f}%</li>'
                f'</ul></div>',
                unsafe_allow_html=True)

        with col2:
            st.markdown("#### MTA Journey Insights")
            ch_journeys = customer_data[customer_data['Path'].str.contains(ch_dive)]
            first_mask  = customer_data['Path'].apply(lambda p: p.split(' > ')[0]) == ch_dive
            last_mask   = customer_data['Path'].apply(lambda p: p.split(' > ')[-1]) == ch_dive
            only_mask   = customer_data['Path'] == ch_dive
            first_cr    = customer_data[first_mask]['Conversion'].mean() * 100 if first_mask.sum() > 0 else 0
            last_cr     = customer_data[last_mask]['Conversion'].mean() * 100 if last_mask.sum() > 0 else 0
            only_cr     = customer_data[only_mask]['Conversion'].mean() * 100 if only_mask.sum() > 0 else 0
            overall_cr  = ch_journeys['Conversion'].mean() * 100 if len(ch_journeys) > 0 else 0
            mta_frac    = mta_result[mta_result['channel_name'] == ch_dive]
            mta_pct_ch  = float(mta_frac['fraction'].iloc[0]) * 100 if len(mta_frac) > 0 else 0
            mmm_pct_ch  = ch_total / mmm_total_all * 100
            st.markdown(
                f'<div class="custom-card"><div class="custom-card-title">Journey Performance</div>'
                f'<ul style="margin:0;padding-left:1.2rem;color:#6b7280;font-size:13px">'
                f'<li>Present in {len(ch_journeys):,} journeys ({len(ch_journeys)/len(customer_data)*100:.1f}% of all)</li>'
                f'<li>Overall conv. rate when present: {overall_cr:.1f}%</li>'
                f'<li>Conv. rate as first touch: {first_cr:.1f}%</li>'
                f'<li>Conv. rate as last touch: {last_cr:.1f}%</li>'
                f'<li>Conv. rate as only channel: {only_cr:.1f}%</li>'
                f'<li>MTA share: {mta_pct_ch:.1f}% &nbsp;|&nbsp; MMM share: {mmm_pct_ch:.1f}%</li>'
                f'</ul></div>',
                unsafe_allow_html=True)

    # =========================================================================
    # TAB 6 — Scenario Planning
    # =========================================================================
    with tab6:
        st.markdown("### Scenario Planning & Budget Optimisation")
        st.markdown("""<div class="info-box">
        <strong>Pure MMM-based forecasting.</strong> Adjust budget multipliers to simulate spend scenarios.
        Adstock and Hill saturation transforms are applied consistently with the trained model —
        so diminishing returns are baked into every forecast.
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("#### Budget Multipliers")
            mults = {
                'Facebook':   st.slider("Facebook",   0.0, 3.0, 1.0, 0.1),
                'Affiliates': st.slider("Affiliates", 0.0, 3.0, 1.0, 0.1),
                'Search':     st.slider("Search",     0.0, 3.0, 1.0, 0.1),
                'Display':    st.slider("Display",    0.0, 3.0, 1.0, 0.1),
            }
            st.markdown("---")
            orig_spend = {ch: df[ch].sum() for ch in CHANNELS}
            new_spend  = {ch: orig_spend[ch] * mults[ch] for ch in CHANNELS}
            tot_orig   = sum(orig_spend.values())
            tot_new    = sum(new_spend.values())
            st.metric("Original Budget", f"${tot_orig:,.0f}")
            st.metric("Scenario Budget", f"${tot_new:,.0f}")
            st.metric("Budget Change",   f"{((tot_new - tot_orig) / tot_orig * 100):+.1f}%")

        with col2:
            df_scen = df.copy()
            for ch in CHANNELS:
                df_scen[ch] = df_scen[ch] * mults[ch]
            df_scen_t, _ = preprocess_channels(df_scen, transform_params)

            features  = ['week', 'year'] + CHANNELS
            scen_pred = models[model_type].predict(df_scen_t[features])
            orig_pred = models[model_type].predict(data_transformed[features])

            # Forecast chart
            st.markdown("#### Sales Forecast: Scenario vs Baseline")
            fig_sc = go.Figure()
            fig_sc.add_trace(go.Scatter(x=df['date'], y=scen_pred, mode='lines',
                                         name='Scenario', line=dict(width=3, color='#667eea'),
                                         fill='tozeroy', fillcolor='rgba(102,126,234,0.1)'))
            fig_sc.add_trace(go.Scatter(x=df['date'], y=orig_pred, mode='lines',
                                         name='Baseline', line=dict(width=2, dash='dash', color='#9ca3af')))
            fig_sc.add_trace(go.Scatter(x=df['date'], y=df['sales'], mode='markers',
                                         name='Actual', marker=dict(size=4, color='#374151', opacity=0.4)))
            fig_sc.update_layout(height=360, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family='Inter, sans-serif'), hovermode='x unified',
                                  legend=dict(orientation='h', y=1.02))
            fig_sc.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
            fig_sc.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            st.plotly_chart(fig_sc, use_container_width=True)

            # ROI metrics
            tot_scen  = scen_pred.sum()
            tot_base  = orig_pred.sum()
            incr_s    = tot_scen - tot_base
            incr_sp   = tot_new - tot_orig
            marg_roi  = (incr_s / abs(incr_sp)) * 100 if incr_sp != 0 else 0
            lift      = (tot_scen - tot_base) / tot_base * 100
            ca, cb, cc, cd = st.columns(4)
            with ca: st.metric("Scenario Sales",    f"${tot_scen:,.0f}")
            with cb: st.metric("Incremental Sales", f"${incr_s:,.0f}")
            with cc: st.metric("Marginal ROI",      f"{marg_roi:.1f}%")
            with cd: st.metric("Sales Lift",        f"{lift:+.1f}%")

            st.markdown("---")

            # Saturation position chart
            st.markdown("#### Saturation Position by Channel")
            st.caption("Channels above 75% saturation show strong diminishing returns for additional spend")
            sat_rows = []
            for ch in CHANNELS:
                p        = transform_params[ch]
                orig_ads = apply_adstock(df[ch].values, p['decay'])
                scen_ads = apply_adstock(df_scen[ch].values, p['decay'])
                sat_rows.append({
                    'Channel':  ch,
                    'Original': round(apply_hill_saturation(orig_ads.mean(), p['alpha'], p['K']) * 100, 1),
                    'Scenario': round(apply_hill_saturation(scen_ads.mean(), p['alpha'], p['K']) * 100, 1),
                })
            sat_df = pd.DataFrame(sat_rows)
            fig_sp = go.Figure()
            fig_sp.add_trace(go.Bar(name='Original', x=sat_df['Channel'], y=sat_df['Original'],
                                     marker_color='#9ca3af',
                                     text=sat_df['Original'].apply(lambda v: f"{v:.1f}%"),
                                     textposition='outside'))
            fig_sp.add_trace(go.Bar(name='Scenario', x=sat_df['Channel'], y=sat_df['Scenario'],
                                     marker_color='#667eea',
                                     text=sat_df['Scenario'].apply(lambda v: f"{v:.1f}%"),
                                     textposition='outside'))
            fig_sp.add_hline(y=75, line_dash='dot', line_color='#ef4444',
                              annotation_text='75% — diminishing returns zone')
            fig_sp.add_hline(y=50, line_dash='dot', line_color='#f59e0b',
                              annotation_text='50% — half-saturation')
            fig_sp.update_layout(barmode='group', height=320,
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family='Inter, sans-serif'),
                                  yaxis=dict(range=[0, 115], title='Saturation (%)'),
                                  legend=dict(orientation='h', y=1.02))
            st.plotly_chart(fig_sp, use_container_width=True)

            # Optimisation notes
            st.markdown("#### Optimisation Notes")
            for ch in CHANNELS:
                p        = transform_params[ch]
                scen_ads = apply_adstock(df_scen[ch].values, p['decay'])
                sat_pct  = apply_hill_saturation(scen_ads.mean(), p['alpha'], p['K']) * 100
                mult     = mults[ch]
                if sat_pct > 80:
                    st.markdown(f"- **{ch}** at {sat_pct:.0f}% saturation at {mult:.1f}x — "
                                f"strong diminishing returns; consider reallocating this budget.")
                elif sat_pct < 40 and mult > 1:
                    st.markdown(f"- **{ch}** at {sat_pct:.0f}% saturation at {mult:.1f}x — "
                                f"room to scale further without hitting diminishing returns.")


if __name__ == "__main__":
    main()
