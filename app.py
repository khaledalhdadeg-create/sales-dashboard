import streamlit as st

# Page Configuration
st.set_page_config(page_title="stc Sales Incentive Calculator", layout="wide", page_icon="📱")

# Custom CSS for stc Branding & Modern UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #F8F9FA;
    }
    
    .stc-header {
        background: linear-gradient(135deg, #4F008C 0%, #33005A 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(79, 0, 140, 0.2);
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stc-header h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        margin: 0;
        font-size: 24px;
    }
    .stc-header p {
        color: #E2D1F0;
        margin: 5px 0 0 0;
        font-size: 13px;
    }
    .stc-badge {
        background-color: #FF007A;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
    }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 2px solid #EFEFEF;
    }
    
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #EBE2F2;
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border-top: 4px solid #4F008C;
    }
    div[data-testid="stMetricValue"] {
        color: #4F008C !important;
        font-weight: 800;
    }
    
    h2, h3 {
        color: #4F008C !important;
        font-weight: 700;
    }
    
    .total-card {
        background: linear-gradient(135deg, #FF007A 0%, #C4005E 100%);
        color: white;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(255, 0, 122, 0.25);
    }
    .total-card h2 {
        color: white !important;
        margin: 0;
        font-size: 34px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
    <div class="stc-header">
        <div>
            <h1>stc | Sales Incentive Calculator</h1>
            <p>Interactive commission & bonus calculation dashboard</p>
        </div>
        <div class="stc-badge">Sales Incentive</div>
    </div>
""", unsafe_allow_html=True)

# Admin Sidebar Controls
st.sidebar.markdown("<h2 style='color: #4F008C;'>⚙️ Admin Target Settings</h2>", unsafe_allow_html=True)
target_ga_voice = st.sidebar.number_input("Target GA Voice:", value=100)
target_ga_data = st.sidebar.number_input("Target GA Data:", value=50)
target_renew_voice = st.sidebar.number_input("Target Renewal Voice:", value=40)
target_renew_data = st.sidebar.number_input("Target Renewal Data:", value=30)
target_zeed = st.sidebar.number_input("Target Zeed:", value=20)

st.sidebar.markdown("---")
st.sidebar.info("💡 Note: Employee inputs achievement figures below to calculate total incentive payout.")

# Employee Inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1️⃣ Sales Achievement")
    ach_ga_voice = st.number_input("Achieved GA Voice:", min_value=0, value=100)
    ach_ga_data = st.number_input("Achieved GA Data:", min_value=0, value=45)
    ach_renew_voice = st.number_input("Achieved Renewal Voice:", min_value=0, value=32)
    ach_renew_data = st.number_input("Achieved Renewal Data:", min_value=0, value=15)
    ach_zeed = st.number_input("Achieved Zeed:", min_value=0, value=20)

with col2:
    st.markdown("### 2️⃣ Operational KPIs (20%)")
    kpi1 = st.slider("KPI-1: STC Care (%)", 0, 100, 85) / 100
    kpi2 = st.slider("KPI-2: W&P (%)", 0, 100, 80) / 100
    kpi3 = st.slider("KPI-3: Accessories (%)", 0, 100, 90) / 100
    kpi4 = st.slider("KPI-4: MNP (%)", 0, 100, 70) / 100

# Calculate KPI Earned Weight
kpi1_w = (kpi1 * 0.05) if kpi1 >= 0.60 else 0
kpi2_w = (kpi2 * 0.05) if kpi2 >= 0.75 else 0
kpi3_w = (kpi3 * 0.05) if kpi3 >= 0.75 else 0
kpi4_w = (kpi4 * 0.05) if kpi4 >= 0.75 else 0
total_kpi_weight = kpi1_w + kpi2_w + kpi3_w + kpi4_w

# Raw Achievement %
raw_ach = {
    'GA Voice': ach_ga_voice / target_ga_voice if target_ga_voice > 0 else 0,
    'GA Data': ach_ga_data / target_ga_data if target_ga_data > 0 else 0,
    'Renew Voice': ach_renew_voice / target_renew_voice if target_renew_voice > 0 else 0,
    'Renew Data': ach_renew_data / target_renew_data if target_renew_data > 0 else 0,
    'Zeed': ach_zeed / target_zeed if target_zeed > 0 else 0,
}

# Weighted Achievement %
weighted_ach = {k: (v * 0.8) + total_kpi_weight for k, v in raw_ach.items()}

# Bonus Matrix Calculation
def get_bonus(prod, ach_pct):
    if ach_pct < 0.9: return 0
    bonus_table = {
        'GA Voice': {0.9: 25, 1.0: 30, 1.1: 35, 1.2: 40},
        'GA Data': {0.9: 15, 1.0: 20, 1.1: 25, 1.2: 30},
        'Renew Voice': {0.9: 10, 1.0: 15, 1.1: 20, 1.2: 25},
        'Renew Data': {0.9: 15, 1.0: 20, 1.1: 25, 1.2: 30},
        'Zeed': {0.9: 5, 1.0: 10, 1.1: 15, 1.2: 20},
    }
    rates = bonus_table.get(prod, {})
    earned = 0
    for threshold in sorted(rates.keys()):
        if ach_pct >= threshold:
            earned = rates[threshold]
    return earned

total_bonus = sum(get_bonus(p, weighted_ach[p]) for p in raw_ach)

st.markdown("---")
st.markdown("### 💰 Summary & Payout")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric("Earned KPI Weight", f"{total_kpi_weight*100:.1f}%")
with res_col2:
    st.metric("Bonus Scheme Payout", f"{total_bonus} KD")

st.markdown("<br>", unsafe_allow_html=True)

# Final Total Payout Card
st.markdown(f"""
    <div class="total-card">
        <p style="margin: 0; font-size: 15px; opacity: 0.9;">Total Estimated Payout</p>
        <h2>{total_bonus} KD</h2>
    </div>
""", unsafe_allow_html=True)
