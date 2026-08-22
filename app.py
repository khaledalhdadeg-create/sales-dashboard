import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import io

# Page Configuration
st.set_page_config(page_title="stc Sales Incentive Calculator", layout="wide", page_icon="📱")

# -------------------------------------------------------------
# 1. إدارة حفظ واسترجاع تارجت الفروع بشكل آمن (Safe Persistence)
# -------------------------------------------------------------
TARGETS_FILE = "targets.json"

DEFAULT_BRANCH_TARGETS = {
    "The Avenues": {
        "target_ga_voice": 120,
        "target_ga_data": 60,
        "target_renew_voice": 50,
        "target_renew_data": 35,
        "target_zeed": 25
    },
    "Assima Mall": {
        "target_ga_voice": 100,
        "target_ga_data": 50,
        "target_renew_voice": 40,
        "target_renew_data": 30,
        "target_zeed": 20
    },
    "Marina Mall": {
        "target_ga_voice": 90,
        "target_ga_data": 45,
        "target_renew_voice": 35,
        "target_renew_data": 25,
        "target_zeed": 18
    }
}

def load_all_targets():
    if os.path.exists(TARGETS_FILE):
        try:
            with open(TARGETS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and len(data) > 0:
                    return data
        except Exception:
            return DEFAULT_BRANCH_TARGETS
    return DEFAULT_BRANCH_TARGETS

def save_all_targets(data):
    try:
        with open(TARGETS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Error saving targets: {e}")

all_targets = load_all_targets()

# Custom CSS for stc Branding
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #F8F9FA; }
    .stc-header {
        background: linear-gradient(135deg, #4F008C 0%, #33005A 100%);
        color: white; padding: 24px 30px; border-radius: 16px;
        box-shadow: 0 10px 25px rgba(79, 0, 140, 0.2); margin-bottom: 25px;
        display: flex; justify-content: space-between; align-items: center;
        flex-wrap: wrap; gap: 10px;
    }
    .stc-header h1 { color: #FFFFFF !important; font-weight: 800; margin: 0; font-size: 24px; }
    .stc-header p { color: #E2D1F0; margin: 5px 0 0 0; font-size: 13px; }
    .stc-badge { background-color: #FF007A; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 12px; }
    section[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 2px solid #EFEFEF; }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF; border: 1px solid #EBE2F2; border-radius: 14px; padding: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); border-top: 4px solid #4F008C;
    }
    div[data-testid="stMetricValue"] { color: #4F008C !important; font-weight: 800; font-size: 20px !important; }
    h2, h3, h4 { color: #4F008C !important; font-weight: 700; }
    .status-card { padding: 15px 20px; border-radius: 12px; font-weight: bold; text-align: center; font-size: 16px; margin-bottom: 20px; }
    .status-standard { background-color: #E6F4EA; color: #137333; border: 1px solid #CEEAD6; }
    .status-bonus { background-color: #FEF7E0; color: #B06000; border: 1px solid #FEEFC3; }
    .status-ineligible { background-color: #FCE8E6; color: #C5221F; border: 1px solid #FAD2CF; }
    .total-card {
        background: linear-gradient(135deg, #FF007A 0%, #C4005E 100%);
        color: white; padding: 22px; border-radius: 16px; text-align: center;
        box-shadow: 0 8px 20px rgba(255, 0, 122, 0.25);
    }
    .total-card h2 { color: white !important; margin: 0; font-size: 34px; }
    .sim-card { background-color: #F0E6F7; border: 1px solid #D8BFD8; padding: 15px; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
    <div class="stc-header">
        <div>
            <h1>stc | Sales Incentive & Branch Performance Calculator</h1>
            <p>Interactive commission, daily run-rate & bonus calculator</p>
        </div>
        <div class="stc-badge">The Avenues Branch Ready</div>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. القائمة الجانبية (Sidebar): اختيار الفرع
# -------------------------------------------------------------
st.sidebar.markdown("<h2 style='color: #4F008C;'>🏢 Select Branch</h2>", unsafe_allow_html=True)
branch_list = list(all_targets.keys()) if all_targets else ["The Avenues"]
selected_branch = st.sidebar.selectbox("Branch Location:", branch_list, index=0)

current_branch_targets = all_targets.get(selected_branch, DEFAULT_BRANCH_TARGETS.get("The Avenues", {}))

# قراءة القيم بأمان
target_ga_voice = current_branch_targets.get("target_ga_voice", 120)
target_ga_data = current_branch_targets.get("target_ga_data", 60)
target_renew_voice = current_branch_targets.get("target_renew_voice", 50)
target_renew_data = current_branch_targets.get("target_renew_data", 35)
target_zeed = current_branch_targets.get("target_zeed", 25)

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color: #4F008C;'>⚙️ Admin Target Settings</h2>", unsafe_allow_html=True)

ADMIN_PASSWORD = "CHV4"
admin_pwd = st.sidebar.text_input("Enter Admin Password:", type="password")

if admin_pwd == ADMIN_PASSWORD:
    st.sidebar.success(f"Unlocked: Editing Targets for {selected_branch}")
    
    with st.sidebar.form("admin_branch_target_form"):
        new_ga_voice = st.number_input("Target GA Voice:", value=int(target_ga_voice))
        new_ga_data = st.number_input("Target GA Data:", value=int(target_ga_data))
        new_renew_voice = st.number_input("Target Renewal Voice:", value=int(target_renew_voice))
        new_renew_data = st.number_input("Target Renewal Data:", value=int(target_renew_data))
        new_zeed = st.number_input("Target Zeed:", value=int(target_zeed))
        
        save_btn = st.form_submit_button(f"💾 Save {selected_branch} Targets")
        
        if save_btn:
            all_targets[selected_branch] = {
                "target_ga_voice": new_ga_voice,
                "target_ga_data": new_ga_data,
                "target_renew_voice": new_renew_voice,
                "target_renew_data": new_renew_data,
                "target_zeed": new_zeed
            }
            save_all_targets(all_targets)
            st.sidebar.success(f"✅ Targets updated globally for {selected_branch}!")
            st.rerun()
else:
    st.sidebar.info("🔒 Targets Locked (View Mode)")
    st.sidebar.text(f"Branch: {selected_branch}")
    st.sidebar.text(f"Target GA Voice: {target_ga_voice}")
    st.sidebar.text(f"Target GA Data: {target_ga_data}")
    st.sidebar.text(f"Target Renewal Voice: {target_renew_voice}")
    st.sidebar.text(f"Target Renewal Data: {target_renew_data}")
    st.sidebar.text(f"Target Zeed: {target_zeed}")

st.sidebar.markdown("---")

# -------------------------------------------------------------
# 3. واجهة الإدخال الرئيسية
# -------------------------------------------------------------
main_col1, main_col2 = st.columns([1.2, 1])

with main_col1:
    st.markdown("### 1️⃣ Sales Achievement (Actual Numbers vs Target %)")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        ach_ga_voice = st.number_input("Achieved GA Voice:", min_value=0, value=100)
    raw_ga_voice = (ach_ga_voice / target_ga_voice) if target_ga_voice > 0 else 0
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Raw Ach %", f"{raw_ga_voice*100:.1f}%")

    c1, c2 = st.columns([2, 1])
    with c1:
        ach_ga_data = st.number_input("Achieved GA Data:", min_value=0, value=45)
    raw_ga_data = (ach_ga_data / target_ga_data) if target_ga_data > 0 else 0
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Raw Ach %", f"{raw_ga_data*100:.1f}%")

    c1, c2 = st.columns([2, 1])
    with c1:
        ach_renew_voice = st.number_input("Achieved Renewal Voice:", min_value=0, value=32)
    raw_renew_voice = (ach_renew_voice / target_renew_voice) if target_renew_voice > 0 else 0
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Raw Ach %", f"{raw_renew_voice*100:.1f}%")

    c1, c2 = st.columns([2, 1])
    with c1:
        ach_renew_data = st.number_input("Achieved Renewal Data:", min_value=0, value=15)
    raw_renew_data = (ach_renew_data / target_renew_data) if target_renew_data > 0 else 0
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Raw Ach %", f"{raw_renew_data*100:.1f}%")

    c1, c2 = st.columns([2, 1])
    with c1:
        ach_zeed = st.number_input("Achieved Zeed:", min_value=0, value=20)
    raw_zeed = (ach_zeed / target_zeed) if target_zeed > 0 else 0
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Raw Ach %", f"{raw_zeed*100:.1f}%")

with main_col2:
    st.markdown("### 2️⃣ Operational KPIs Score (20%)")
    kpi1 = st.slider("KPI-1: STC Care (%)", 0, 100, 85) / 100
    kpi2 = st.slider("KPI-2: W&P (%)", 0, 100, 80) / 100
    kpi3 = st.slider("KPI-3: Accessories (%)", 0, 100, 90) / 100
    kpi4 = st.slider("KPI-4: MNP (%)", 0, 100, 70) / 100

# -------------------------------------------------------------
# 4. الحسابات الرئيسية والتفصيلية
# -------------------------------------------------------------
kpi1_w = (kpi1 * 0.05) if kpi1 >= 0.60 else 0
kpi2_w = (kpi2 * 0.05) if kpi2 >= 0.75 else 0
kpi3_w = (kpi3 * 0.05) if kpi3 >= 0.75 else 0
kpi4_w = (kpi4 * 0.05) if kpi4 >= 0.75 else 0
total_kpi_weight = kpi1_w + kpi2_w + kpi3_w + kpi4_w

raw_ach = {
    'GA Voice': raw_ga_voice,
    'GA Data': raw_ga_data,
    'Renew Voice': raw_renew_voice,
    'Renew Data': raw_renew_data,
    'Zeed': raw_zeed,
}

weighted_ach = {k: (v * 0.8) + total_kpi_weight for k, v in raw_ach.items()}
min_weighted_ach = min(weighted_ach.values())
avg_weighted_ach = sum(weighted_ach.values()) / len(weighted_ach)

# Matrices
incentive_matrix = {
    'GA Voice':   {0.80: 88.00, 0.85: 93.50, 0.90: 99.00, 0.95: 104.50, 1.00: 110.00, 1.05: 115.50, 1.10: 121.00, 1.15: 126.50, 1.20: 132.00, 1.25: 137.50, 1.30: 143.00, 1.35: 148.50, 1.40: 154.00},
    'GA Data':    {0.80: 0.00,  0.85: 0.00,  0.90: 49.50, 0.95: 52.25,  1.00: 55.00,  1.05: 57.75,  1.10: 60.50,  1.15: 63.25,  1.20: 66.00,  1.25: 68.75,  1.30: 71.50,  1.35: 74.25,  1.40: 77.00},
    'Renew Voice':{0.80: 0.00,  0.85: 0.00,  0.90: 24.75, 0.95: 26.13,  1.00: 27.50,  1.05: 28.88,  1.10: 30.25,  1.15: 31.63,  1.20: 33.00,  1.25: 34.38,  1.30: 35.75,  1.35: 37.13,  1.40: 38.50},
    'Renew Data': {0.80: 0.00,  0.85: 0.00,  0.90: 24.75, 0.95: 26.13,  1.00: 27.50,  1.05: 28.88,  1.10: 30.25,  1.15: 31.63,  1.20: 33.00,  1.25: 34.38,  1.30: 35.75,  1.35: 37.13,  1.40: 38.50},
    'Zeed':       {0.80: 0.00,  0.85: 0.00,  0.90: 49.50, 0.95: 52.25,  1.00: 55.00,  1.05: 57.75,  1.10: 60.50,  1.15: 63.25,  1.20: 66.00,  1.25: 68.75,  1.30: 71.50,  1.35: 74.25,  1.40: 77.00},
}

bonus_matrix = {
    'GA Voice':   {0.90: 25.00, 1.00: 30.00, 1.10: 35.00, 1.20: 40.00},
    'GA Data':    {0.90: 15.00, 1.00: 20.00, 1.10: 25.00, 1.20: 30.00},
    'Renew Voice':{0.90: 10.00, 1.00: 15.00, 1.10: 20.00, 1.20: 25.00},
    'Renew Data': {0.90: 15.00, 1.00: 20.00, 1.10: 25.00, 1.20: 30.00},
    'Zeed':       {0.90: 5.00,  1.00: 10.00, 1.10: 15.00, 1.20: 20.00},
}

# Logic Payout
standard_payout = 0.0
bonus_payout = 0.0
eligibility_status = ""

if min_weighted_ach >= 0.75:
    eligibility_status = "Standard Scheme Qualified (MIN Weighted Ach ≥ 75%)"
    for prod, ach in weighted_ach.items():
        if ach >= 0.80:
            rates = incentive_matrix.get(prod, {})
            earned = 0.0
            for thresh in sorted(rates.keys()):
                if ach >= thresh:
                    earned = rates[thresh]
            standard_payout += earned

elif avg_weighted_ach >= 0.75:
    eligibility_status = "Bonus Scheme Qualified (AVERAGE Weighted Ach ≥ 75%)"
    for prod, ach in weighted_ach.items():
        if ach >= 0.90:
            rates = bonus_matrix.get(prod, {})
            earned = 0.0
            for thresh in sorted(rates.keys()):
                if ach >= thresh:
                    earned = rates[thresh]
            bonus_payout += earned
else:
    eligibility_status = "Ineligible (MIN < 75% & AVERAGE < 75%)"

total_final_payout = standard_payout + bonus_payout

# Display Outputs
st.markdown("---")
st.markdown("### 📊 Qualification & Payout Summary")

if "Standard" in eligibility_status:
    st.markdown(f'<div class="status-card status-standard">🟢 {eligibility_status}</div>', unsafe_allow_html=True)
elif "Bonus" in eligibility_status:
    st.markdown(f'<div class="status-card status-bonus">🥈 {eligibility_status}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-card status-ineligible">🔴 {eligibility_status}</div>', unsafe_allow_html=True)

res_col1, res_col2, res_col3, res_col4 = st.columns(4)
with res_col1:
    st.metric("Earned KPI Weight", f"{total_kpi_weight*100:.1f}%")
with res_col2:
    st.metric("Standard Scheme Payout", f"{standard_payout:.2f} KD")
with res_col3:
    st.metric("Bonus Scheme Payout", f"{bonus_payout:.2f} KD")
with res_col4:
    st.metric("Min / Avg Weighted Ach %", f"{min_weighted_ach*100:.1f}% / {avg_weighted_ach*100:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="total-card">
        <p style="margin: 0; font-size: 15px; opacity: 0.9;">Total Final Payout ({selected_branch})</p>
        <h2>{total_final_payout:.2f} KD</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------------
# 5. الميزات الإضافية (Extra Features Tabs)
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Daily Target & Run-Rate", 
    "🔮 What-If Simulator", 
    "🔍 KPI Weight Breakdown", 
    "📥 Export Payout Report"
])

# Tab 1: Daily Target
with tab1:
    st.markdown("#### 📅 Daily Sales Target Tracker")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        current_day = st.number_input("Current Day of Month:", min_value=1, max_value=31, value=15)
        total_days = st.number_input("Total Days in Month:", min_value=28, max_value=31, value=30)
    
    days_remaining = max(1, total_days - current_day)
    
    products_target_data = [
        ("GA Voice", ach_ga_voice, target_ga_voice),
        ("GA Data", ach_ga_data, target_ga_data),
        ("Renew Voice", ach_renew_voice, target_renew_voice),
        ("Renew Data", ach_renew_data, target_renew_data),
        ("Zeed", ach_zeed, target_zeed)
    ]
    
    rr_list = []
    for prod_name, ach, tgt in products_target_data:
        rem_needed = max(0, tgt - ach)
        daily_req = rem_needed / days_remaining
        curr_run_rate = (ach / current_day) * total_days
        proj_pct = (curr_run_rate / tgt * 100) if tgt > 0 else 0
        
        status_icon = "🟢 On Track" if proj_pct >= 100 else ("🟡 Borderline" if proj_pct >= 75 else "🔴 At Risk")
        
        rr_list.append({
            "Product": prod_name,
            "Achieved So Far": ach,
            "Target": tgt,
            "Remaining Needed": rem_needed,
            "Req. Daily Rate (Units/Day)": round(daily_req, 2),
            "Projected Month-End %": f"{proj_pct:.1f}%",
            "Status": status_icon
        })
    
    st.dataframe(pd.DataFrame(rr_list), use_container_width=True)

# Tab 2: What-If Simulator
with tab2:
    st.markdown("#### 🔮 What-If Incentive Simulator")
    st.info("Simulate extra sales to see how much your total commission KD increases!")
    
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        add_voice = st.slider("Extra GA Voice Units:", 0, 20, 3)
        add_data = st.slider("Extra GA Data Units:", 0, 20, 2)
    with sim_col2:
        add_ren_voice = st.slider("Extra Renew Voice Units:", 0, 20, 2)
        add_zeed = st.slider("Extra Zeed Units:", 0, 10, 1)
    
    sim_raw_ga_voice = ((ach_ga_voice + add_voice) / target_ga_voice) if target_ga_voice > 0 else 0
    sim_raw_ga_data = ((ach_ga_data + add_data) / target_ga_data) if target_ga_data > 0 else 0
    sim_raw_ren_voice = ((ach_renew_voice + add_ren_voice) / target_renew_voice) if target_renew_voice > 0 else 0
    sim_raw_zeed = ((ach_zeed + add_zeed) / target_zeed) if target_zeed > 0 else 0
    
    sim_raw_ach = {
        'GA Voice': sim_raw_ga_voice,
        'GA Data': sim_raw_ga_data,
        'Renew Voice': sim_raw_ren_voice,
        'Renew Data': raw_renew_data,
        'Zeed': sim_raw_zeed,
    }
    sim_weighted_ach = {k: (v * 0.8) + total_kpi_weight for k, v in sim_raw_ach.items()}
    sim_min_weighted = min(sim_weighted_ach.values())
    
    sim_payout = 0.0
    if sim_min_weighted >= 0.75:
        for prod, ach in sim_weighted_ach.items():
            if ach >= 0.80:
                rates = incentive_matrix.get(prod, {})
                earned = 0.0
                for thresh in sorted(rates.keys()):
                    if ach >= thresh:
                        earned = rates[thresh]
                sim_payout += earned
                
    gain_kd = sim_payout - total_final_payout
    
    st.markdown(f"""
        <div class="sim-card">
            <h4>Potential Additional Earnings: +{gain_kd:.2f} KD</h4>
            <p style="margin: 0;">New Estimated Total Payout: <b>{sim_payout:.2f} KD</b></p>
        </div>
    """, unsafe_allow_html=True)

# Tab 3: KPI Breakdown
with tab3:
    st.markdown("#### 🔍 KPI Weight Earned Breakdown (Max 20%)")
    kpi_breakdown_data = [
        {"KPI Name": "STC Care", "Actual Score": f"{kpi1*100:.0f}%", "Min Threshold": "60%", "Max Weight": "5.0%", "Weight Earned": f"{kpi1_w*100:.2f}%"},
        {"KPI Name": "W&P", "Actual Score": f"{kpi2*100:.0f}%", "Min Threshold": "75%", "Max Weight": "5.0%", "Weight Earned": f"{kpi2_w*100:.2f}%"},
        {"KPI Name": "Accessories", "Actual Score": f"{kpi3*100:.0f}%", "Min Threshold": "75%", "Max Weight": "5.0%", "Weight Earned": f"{kpi3_w*100:.2f}%"},
        {"KPI Name": "MNP", "Actual Score": f"{kpi4*100:.0f}%", "Min Threshold": "75%", "Max Weight": "5.0%", "Weight Earned": f"{kpi4_w*100:.2f}%"},
    ]
    st.dataframe(pd.DataFrame(kpi_breakdown_data), use_container_width=True)

# Tab 4: Export Report
with tab4:
    st.markdown("#### 📥 Export Official Statement")
    emp_name = st.text_input("Employee Name:", value="Sales Representative")
    
    report_df = pd.DataFrame([
        {"Product": "GA Voice", "Target": target_ga_voice, "Achieved": ach_ga_voice, "Raw Ach %": f"{raw_ga_voice*100:.1f}%", "Weighted Ach %": f"{weighted_ach['GA Voice']*100:.1f}%"},
        {"Product": "GA Data", "Target": target_ga_data, "Achieved": ach_ga_data, "Raw Ach %": f"{raw_ga_data*100:.1f}%", "Weighted Ach %": f"{weighted_ach['GA Data']*100:.1f}%"},
        {"Product": "Renew Voice", "Target": target_renew_voice, "Achieved": ach_renew_voice, "Raw Ach %": f"{raw_renew_voice*100:.1f}%", "Weighted Ach %": f"{weighted_ach['Renew Voice']*100:.1f}%"},
        {"Product": "Renew Data", "Target": target_renew_data, "Achieved": ach_renew_data, "Raw Ach %": f"{raw_renew_data*100:.1f}%", "Weighted Ach %": f"{weighted_ach['Renew Data']*100:.1f}%"},
        {"Product": "Zeed", "Target": target_zeed, "Achieved": ach_zeed, "Raw Ach %": f"{raw_zeed*100:.1f}%", "Weighted Ach %": f"{weighted_ach['Zeed']*100:.1f}%"},
    ])
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        report_df.to_excel(writer, index=False, sheet_name='Payout_Statement')
    
    st.download_button(
        label="📥 Download Excel Payout Report",
        data=buffer.getvalue(),
        file_name=f"stc_Incentive_{selected_branch}_{emp_name}_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd
