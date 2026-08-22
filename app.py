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
    
    .status-card {
        padding: 15px 20px;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .status-standard {
        background-color: #E6F4EA;
        color: #137333;
        border: 1px solid #CEEAD6;
    }
    .status-bonus {
        background-color: #FEF7E0;
        color: #B06000;
        border: 1px solid #FEEFC3;
    }
    .status-ineligible {
        background-color: #FCE8E6;
        color: #C5221F;
        border: 1px solid #FAD2CF;
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

# Admin Sidebar Controls with Password Protection (CHV4)
st.sidebar.markdown("<h2 style='color: #4F008C;'>⚙️ Admin Target Settings</h2>", unsafe_allow_html=True)

ADMIN_PASSWORD = "CHV4"
admin_pwd = st.sidebar.text_input("Enter Admin Password:", type="password")

if admin_pwd == ADMIN_PASSWORD:
    st.sidebar.success("Unlocked: Admin Mode")
    target_ga_voice = st.sidebar.number_input("Target GA Voice:", value=100)
    target_ga_data = st.sidebar.number_input("Target GA Data:", value=50)
    target_renew_voice = st.sidebar.number_input("Target Renewal Voice:", value=40)
    target_renew_data = st.sidebar.number_input("Target Renewal Data:", value=30)
    target_zeed = st.sidebar.number_input("Target Zeed:", value=20)
else:
    st.sidebar.info("🔒 Targets Locked (View Mode)")
    target_ga_voice = 100
    target_ga_data = 50
    target_renew_voice = 40
    target_renew_data = 30
    target_zeed = 20
    
    st.sidebar.text(f"Target GA Voice: {target_ga_voice}")
    st.sidebar.text(f"Target GA Data: {target_ga_data}")
    st.sidebar.text(f"Target Renewal Voice: {target_renew_voice}")
    st.sidebar.text(f"Target Renewal Data: {target_renew_data}")
    st.sidebar.text(f"Target Zeed: {target_zeed}")

st.sidebar.markdown("---")

# Employee Inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1️⃣ Sales Achievement (Actual Numbers)")
    ach_ga_voice = st.number_input("Achieved GA Voice:", min_value=0, value=100)
    ach_ga_data = st.number_input("Achieved GA Data:", min_value=0, value=45)
    ach_renew_voice = st.number_input("Achieved Renewal Voice:", min_value=0, value=32)
    ach_renew_data = st.number_input("Achieved Renewal Data:", min_value=0, value=15)
    ach_zeed = st.number_input("Achieved Zeed:", min_value=0, value=20)

with col2:
    st.markdown("### 2️⃣ Operational KPIs Score (20%)")
    kpi1 = st.slider("KPI-1: STC Care (%)", 0, 100, 85) / 100
    kpi2 = st.slider("KPI-2: W&P (%)", 0, 100, 80) / 100
    kpi3 = st.slider("KPI-3: Accessories (%)", 0, 100, 90) / 100
    kpi4 = st.slider("KPI-4: MNP (%)", 0, 100, 70) / 100

# -------------------------------------------------------------
# 1. حساب أوزان الـ KPIs (20%) بناءً على حدود الأدنى
# -------------------------------------------------------------
kpi1_w = (kpi1 * 0.05) if kpi1 >= 0.60 else 0
kpi2_w = (kpi2 * 0.05) if kpi2 >= 0.75 else 0
kpi3_w = (kpi3 * 0.05) if kpi3 >= 0.75 else 0
kpi4_w = (kpi4 * 0.05) if kpi4 >= 0.75 else 0
total_kpi_weight = kpi1_w + kpi2_w + kpi3_w + kpi4_w

# 2. حساب نسبة الإنجاز الخام للمنتج (Raw Achievement %)
raw_ach = {
    'GA Voice': ach_ga_voice / target_ga_voice if target_ga_voice > 0 else 0,
    'GA Data': ach_ga_data / target_ga_data if target_ga_data > 0 else 0,
    'Renew Voice': ach_renew_voice / target_renew_voice if target_renew_voice > 0 else 0,
    'Renew Data': ach_renew_data / target_renew_data if target_renew_data > 0 else 0,
    'Zeed': ach_zeed / target_zeed if target_zeed > 0 else 0,
}

# 3. حساب النسبة الموزونة النهائية (80% أداء المنتج + 20% أداء KPIs)
weighted_ach = {k: (v * 0.8) + total_kpi_weight for k, v in raw_ach.items()}

min_weighted_ach = min(weighted_ach.values())
avg_weighted_ach = sum(weighted_ach.values()) / len(weighted_ach)

# -------------------------------------------------------------
# 4. جداول العمولات والبونص (Incentive & Bonus Matrices)
# -------------------------------------------------------------
# Incentive Matrix (Standard Scheme) - يبدأ من 80% إلى 140%
incentive_matrix = {
    'GA Voice':   {0.80: 20, 0.85: 22, 0.90: 25, 0.95: 28, 1.00: 30, 1.05: 33, 1.10: 35, 1.15: 38, 1.20: 40, 1.25: 42, 1.30: 45, 1.35: 48, 1.40: 50},
    'GA Data':    {0.80: 10, 0.85: 12, 0.90: 15, 0.95: 18, 1.00: 20, 1.05: 22, 1.10: 25, 1.15: 28, 1.20: 30, 1.25: 32, 1.30: 35, 1.35: 38, 1.40: 40},
    'Renew Voice':{0.80: 5,  0.85: 8,  0.90: 10, 0.95: 12, 1.00: 15, 1.05: 18, 1.10: 20, 1.15: 22, 1.20: 25, 1.25: 28, 1.30: 30, 1.35: 32, 1.40: 35},
    'Renew Data': {0.80: 10, 0.85: 12, 0.90: 15, 0.95: 18, 1.00: 20, 1.05: 22, 1.10: 25, 1.15: 28, 1.20: 30, 1.25: 32, 1.30: 35, 1.35: 38, 1.40: 40},
    'Zeed':       {0.80: 3,  0.85: 4,  0.90: 5,  0.95: 8,  1.00: 10, 1.05: 12, 1.10: 15, 1.15: 18, 1.20: 20, 1.25: 22, 1.30: 25, 1.35: 28, 1.40: 30},
}

# Bonus Matrix (Bonus Scheme) - يبدأ من 90% إلى 120%
bonus_matrix = {
    'GA Voice':   {0.90: 15, 1.00: 20, 1.10: 25, 1.20: 30},
    'GA Data':    {0.90: 10, 1.00: 15, 1.10: 20, 1.20: 25},
    'Renew Voice':{0.90: 5,  1.00: 10, 1.10: 15, 1.20: 20},
    'Renew Data': {0.90: 10, 1.00: 15, 1.10: 20, 1.20: 25},
    'Zeed':       {0.90: 3,  1.00: 5,  1.10: 10, 1.20: 15},
}

# -------------------------------------------------------------
# 5. تطبيق شروط التأهل الحاكمة (Eligibility Logic)
# -------------------------------------------------------------
standard_payout = 0.0
bonus_payout = 0.0
eligibility_status = ""

if min_weighted_ach >= 0.75:
    # 🟢 النظام الأول: Standard Scheme
    eligibility_status = "Standard Scheme Qualified (MIN Weighted Ach ≥ 75%)"
    for prod, ach in weighted_ach.items():
        if ach >= 0.80:
            rates = incentive_matrix.get(prod, {})
            earned = 0
            for thresh in sorted(rates.keys()):
                if ach >= thresh:
                    earned = rates[thresh]
            standard_payout += earned
        else:
            # النسبة أقل من 80% مع تحقيقه شرط الـ MIN: يحصل على 0 د.ك دون خطأ برمجى (تلافي N/A)
            standard_payout += 0

elif avg_weighted_ach >= 0.75:
    # 🥈 النظام الثاني: Bonus Scheme
    eligibility_status = "Bonus Scheme Qualified (AVERAGE Weighted Ach ≥ 75%)"
    for prod, ach in weighted_ach.items():
        if ach >= 0.90:
            rates = bonus_matrix.get(prod, {})
            earned = 0
            for thresh in sorted(rates.keys()):
                if ach >= thresh:
                    earned = rates[thresh]
            bonus_payout += earned
        else:
            # المنتجات أقل من 90% تأخذ 0 د.ك (تلافي N/A)
            bonus_payout += 0

else:
    # 🔴 غير مؤهل
    eligibility_status = "Ineligible (MIN < 75% & AVERAGE < 75%)"

total_final_payout = standard_payout + bonus_payout

# -------------------------------------------------------------
# 6. الشاشات وعرض النتائج (Outputs & Cards)
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 📊 Qualification & Payout Summary")

# بطاقة حالة التأهل
if "Standard" in eligibility_status:
    st.markdown(f'<div class="status-card status-standard">🟢 {eligibility_status}</div>', unsafe_allow_html=True)
elif "Bonus" in eligibility_status:
    st.markdown(f'<div class="status-card status-bonus">🥈 {eligibility_status}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-card status-ineligible">🔴 {eligibility_status}</div>', unsafe_allow_html=True)

# المتركس
res_col1, res_col2, res_col3, res_col4 = st.columns(4)
with res_col1:
    st.metric("Earned KPI Weight", f"{total_kpi_weight*100:.1f}%")
with res_col2:
    st.metric("Standard Scheme Payout", f"{standard_payout:.1f} KD")
with res_col3:
    st.metric("Bonus Scheme Payout", f"{bonus_payout:.1f} KD")
with res_col4:
    st.metric("Min / Avg Ach %", f"{min_weighted_ach*100:.1f}% / {avg_weighted_ach*100:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# المبلغ النهائي المستحق
st.markdown(f"""
    <div class="total-card">
        <p style="margin: 0; font-size: 15px; opacity: 0.9;">Total Final Payout</p>
        <h2>{total_final_payout:.1f} KD</h2>
    </div>
""", unsafe_allow_html=True)
