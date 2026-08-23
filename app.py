import streamlit as st
import json
import os
import calendar
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="stc Sales Incentive Calculator - The Avenues", 
    layout="wide", 
    page_icon="📱",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# إدارة ملف التارجت العام (Persistence File)
# -------------------------------------------------------------
TARGETS_FILE = "targets.json"

DEFAULT_TARGETS = {
    "target_ga_voice": 100,
    "target_ga_data": 50,
    "target_renew_voice": 40,
    "target_renew_data": 30,
    "target_zeed": 20
}

def load_targets():
    if os.path.exists(TARGETS_FILE):
        try:
            with open(TARGETS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_TARGETS
    return DEFAULT_TARGETS

def save_targets(data):
    with open(TARGETS_FILE, "w") as f:
        json.dump(data, f)

current_targets = load_targets()

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #F8F9FA; }
    
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    .stc-header {
        background: linear-gradient(135deg, #4F008C 0%, #33005A 100%);
        color: white; padding: 24px 30px; border-radius: 16px;
        box-shadow: 0 10px 25px rgba(79, 0, 140, 0.2); margin-bottom: 20px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .stc-header h1 { color: #FFFFFF !important; font-weight: 800; margin: 0; font-size: 24px; }
    .stc-header p { color: #E2D1F0; margin: 5px 0 0 0; font-size: 13px; }
    .stc-badge { background-color: #FF007A; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 12px; }
    
    div[data-testid="stMetric"] {
        background-color: #FFFFFF; border: 1px solid #EBE2F2; border-radius: 14px; padding: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); border-top: 4px solid #4F008C;
    }
    div[data-testid="stMetricValue"] { color: #4F008C !important; font-weight: 800; font-size: 20px !important; }
    h2, h3 { color: #4F008C !important; font-weight: 700; }
    
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
    
    .insight-box { padding: 15px 20px; border-radius: 10px; margin-bottom: 15px; }
    .insight-warning { background-color: #FFF3CD; border-left: 5px solid #FFC107; color: #856404; }
    .insight-error { background-color: #F8D7DA; border-left: 5px solid #DC3545; color: #721C24; }
    .insight-info { background-color: #D1ECF1; border-left: 5px solid #17A2B8; color: #0C5460; }
    .insight-success { background-color: #D4EDDA; border-left: 5px solid #28A745; color: #155724; }
    
    .priority-card {
        background: #FFFFFF; border: 1px solid #E2D1F0; border-radius: 12px;
        padding: 16px; margin-bottom: 12px; border-right: 6px solid #FF007A;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .priority-rank {
        background: #4F008C; color: white; padding: 3px 10px; border-radius: 12px;
        font-weight: bold; font-size: 12px; display: inline-block; margin-bottom: 6px;
    }

    .text-en { font-weight: 600; direction: ltr; text-align: left; margin-bottom: 6px; }
    .text-ar { font-weight: 600; direction: rtl; text-align: right; margin-top: 6px; border-top: 1px dashed rgba(0,0,0,0.1); padding-top: 6px; }
    
    .admin-container {
        background-color: #FFFFFF; border: 1px solid #E2D1F0; border-radius: 12px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(79,0,140,0.05);
    }

    /* Pacing Gauge Cards Style */
    .pacing-card {
        background: #FFFFFF; border: 1px solid #E2D1F0; border-radius: 12px;
        padding: 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        margin-bottom: 10px;
    }
    .pacing-on-track { border-top: 5px solid #28A745; }
    .pacing-lagging { border-top: 5px solid #DC3545; }
    .pacing-ahead { border-top: 5px solid #17A2B8; }

    /* Custom Progress Bar Style */
    .progress-wrapper {
        background-color: #E9ECEF;
        border-radius: 10px;
        height: 18px;
        width: 100%;
        overflow: hidden;
        margin-top: 8px;
        margin-bottom: 15px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
    }
    .progress-bar-inner {
        height: 100%;
        border-radius: 10px;
        transition: width 0.4s ease-in-out;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 8px;
        color: white;
        font-size: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# دالة رسم شريط التقدم المرئي
def render_progress_bar(ratio):
    pct = ratio * 100
    display_pct = min(pct, 100)
    
    if pct < 75:
        color = "linear-gradient(90deg, #EA4335, #D93025)"
    elif pct < 100:
        color = "linear-gradient(90deg, #FBBC04, #F9AB00)"
    elif pct < 120:
        color = "linear-gradient(90deg, #34A853, #188038)"
    else:
        color = "linear-gradient(90deg, #FF007A, #4F008C)"
        
    st.markdown(f"""
        <div class="progress-wrapper">
            <div class="progress-bar-inner" style="width: {display_pct}%; background: {color};">
                {f"{pct:.0f}%" if display_pct > 15 else ""}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Main Header
st.markdown("""
    <div class="stc-header">
        <div>
            <h1>stc | Sales Incentive Calculator</h1>
            <p>Interactive commission & bonus dashboard — فرع الأڤنيوز (The Avenues)</p>
        </div>
        <div class="stc-badge">Sales Incentive</div>
    </div>
""", unsafe_allow_html=True)

# Admin Settings Panel
top_col1, top_col2 = st.columns([0.85, 0.15])
with top_col2:
    show_admin = st.toggle("⚙️ Admin", value=False)

if show_admin:
    st.markdown('<div class="admin-container">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Target Settings (Admin Panel)")
    ADMIN_PASSWORD = "CHV4"
    admin_pwd = st.text_input("Enter Admin Password:", type="password")

    if admin_pwd == ADMIN_PASSWORD:
        st.success("Unlocked: Admin Mode")
        with st.form("admin_target_form"):
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                new_ga_voice = st.number_input("Target GA Voice:", value=int(current_targets["target_ga_voice"]))
                new_ga_data = st.number_input("Target GA Data:", value=int(current_targets["target_ga_data"]))
            with col_a2:
                new_renew_voice = st.number_input("Target Renewal Voice:", value=int(current_targets["target_renew_voice"]))
                new_renew_data = st.number_input("Target Renewal Data:", value=int(current_targets["target_renew_data"]))
            with col_a3:
                new_zeed = st.number_input("Target Zeed:", value=int(current_targets["target_zeed"]))
            
            save_btn = st.form_submit_button("💾 Save Targets For All Users")
            
            if save_btn:
                updated_data = {
                    "target_ga_voice": new_ga_voice,
                    "target_ga_data": new_ga_data,
                    "target_renew_voice": new_renew_voice,
                    "target_renew_data": new_renew_data,
                    "target_zeed": new_zeed
                }
                save_targets(updated_data)
                st.success("✅ Targets updated globally!")
                st.rerun()

        target_ga_voice, target_ga_data, target_renew_voice, target_renew_data, target_zeed = new_ga_voice, new_ga_data, new_renew_voice, new_renew_data, new_zeed
    else:
        if admin_pwd != "":
            st.error("🔒 Incorrect Password")
        else:
            st.info("🔒 Enter password to edit targets.")
        target_ga_voice = current_targets["target_ga_voice"]
        target_ga_data = current_targets["target_ga_data"]
        target_renew_voice = current_targets["target_renew_voice"]
        target_renew_data = current_targets["target_renew_data"]
        target_zeed = current_targets["target_zeed"]
    st.markdown('</div>', unsafe_allow_html=True)
else:
    target_ga_voice = current_targets["target_ga_voice"]
    target_ga_data = current_targets["target_ga_data"]
    target_renew_voice = current_targets["target_renew_voice"]
    target_renew_data = current_targets["target_renew_data"]
    target_zeed = current_targets["target_zeed"]

# Layout Inputs
main_col1, main_col2 = st.columns([1.2, 1])

with main_col1:
    st.markdown("### 1️⃣ Sales Achievement & Target Progress")
    
    # GA Voice
    c1, c2 = st.columns([2, 1])
    with c1: ach_ga_voice = st.number_input("Achieved GA Voice:", min_value=0, value=100)
    raw_ga_voice = (ach_ga_voice / target_ga_voice) if target_ga_voice > 0 else 0
    with c2: st.metric("Raw Ach %", f"{raw_ga_voice*100:.1f}%")
    render_progress_bar(raw_ga_voice)

    # GA Data
    c1, c2 = st.columns([2, 1])
    with c1: ach_ga_data = st.number_input("Achieved GA Data:", min_value=0, value=45)
    raw_ga_data = (ach_ga_data / target_ga_data) if target_ga_data > 0 else 0
    with c2: st.metric("Raw Ach %", f"{raw_ga_data*100:.1f}%")
    render_progress_bar(raw_ga_data)

    # Renew Voice
    c1, c2 = st.columns([2, 1])
    with c1: ach_renew_voice = st.number_input("Achieved Renewal Voice:", min_value=0, value=32)
    raw_renew_voice = (ach_renew_voice / target_renew_voice) if target_renew_voice > 0 else 0
    with c2: st.metric("Raw Ach %", f"{raw_renew_voice*100:.1f}%")
    render_progress_bar(raw_renew_voice)

    # Renew Data
    c1, c2 = st.columns([2, 1])
    with c1: ach_renew_data = st.number_input("Achieved Renewal Data:", min_value=0, value=15)
    raw_renew_data = (ach_renew_data / target_renew_data) if target_renew_data > 0 else 0
    with c2: st.metric("Raw Ach %", f"{raw_renew_data*100:.1f}%")
    render_progress_bar(raw_renew_data)

    # Zeed
    c1, c2 = st.columns([2, 1])
    with c1: ach_zeed = st.number_input("Achieved Zeed:", min_value=0, value=20)
    raw_zeed = (ach_zeed / target_zeed) if target_zeed > 0 else 0
    with c2: st.metric("Raw Ach %", f"{raw_zeed*100:.1f}%")
    render_progress_bar(raw_zeed)

with main_col2:
    st.markdown("### 2️⃣ Operational KPIs Score (20%)")
    kpi1 = st.slider("KPI-1: STC Care (%)", 0, 100, 85) / 100
    kpi2 = st.slider("KPI-2: W&P (%)", 0, 100, 80) / 100
    kpi3 = st.slider("KPI-3: Accessories (%)", 0, 100, 90) / 100
    kpi4 = st.slider("KPI-4: MNP (%)", 0, 100, 70) / 100

# Calculations
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
                if ach >= thresh: earned = rates[thresh]
            standard_payout += earned
elif avg_weighted_ach >= 0.75:
    eligibility_status = "Bonus Scheme Qualified (AVERAGE Weighted Ach ≥ 75%)"
    for prod, ach in weighted_ach.items():
        if ach >= 0.90:
            rates = bonus_matrix.get(prod, {})
            earned = 0.0
            for thresh in sorted(rates.keys()):
                if ach >= thresh: earned = rates[thresh]
            bonus_payout += earned
else:
    eligibility_status = "Ineligible (MIN < 75% & AVERAGE < 75%)"

total_final_payout = standard_payout + bonus_payout

# Summary
st.markdown("---")
st.markdown("### 📊 Qualification & Payout Summary")

if "Standard" in eligibility_status:
    st.markdown(f'<div class="status-card status-standard">🟢 {eligibility_status}</div>', unsafe_allow_html=True)
elif "Bonus" in eligibility_status:
    st.markdown(f'<div class="status-card status-bonus">🥈 {eligibility_status}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-card status-ineligible">🔴 {eligibility_status}</div>', unsafe_allow_html=True)

res_col1, res_col2, res_col3, res_col4 = st.columns(4)
with res_col1: st.metric("Earned KPI Weight", f"{total_kpi_weight*100:.1f}%")
with res_col2: st.metric("Standard Scheme Payout", f"{standard_payout:.2f} KD")
with res_col3: st.metric("Bonus Scheme Payout", f"{bonus_payout:.2f} KD")
with res_col4: st.metric("Min / Avg Weighted Ach %", f"{min_weighted_ach*100:.1f}% / {avg_weighted_ach*100:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
    <div class="total-card">
        <p style="margin: 0; font-size: 15px; opacity: 0.9;">Total Final Payout</p>
        <h2 style="display:inline;">{total_final_payout:.2f} KD</h2>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Smart Priority Recommendation Engine (ترتيب الأولويات الذكي)
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 🎯 Smart Priority Recommendation | ترتيب الأولويات الذكي لأعلى عائد")

targets_map = {'GA Voice': target_ga_voice, 'GA Data': target_ga_data, 'Renew Voice': target_renew_voice, 'Renew Data': target_renew_data, 'Zeed': target_zeed}
achieved_map = {'GA Voice': ach_ga_voice, 'GA Data': ach_ga_data, 'Renew Voice': ach_renew_voice, 'Renew Data': ach_renew_data, 'Zeed': ach_zeed}
thresholds = [0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40]

priority_opportunities = []

for prod, weight in weighted_ach.items():
    tgt = targets_map.get(prod, 0)
    ach = achieved_map.get(prod, 0)
    rates = incentive_matrix.get(prod, {})
    
    current_earned = 0.0
    for thresh in sorted(rates.keys()):
        if weight >= thresh:
            current_earned = rates[thresh]

    if tgt > 0:
        for t in thresholds:
            if weight < t:
                needed_raw = (t - total_kpi_weight) / 0.8
                needed_units = int(needed_raw * tgt) - ach + 1
                next_tier_payout = rates.get(t, 0.0)
                extra_kd = next_tier_payout - current_earned

                if needed_units > 0 and extra_kd > 0:
                    roi_per_value = extra_kd / needed_units
                    priority_opportunities.append({
                        "prod": prod,
                        "needed_units": needed_units,
                        "target_tier": int(t * 100),
                        "extra_kd": extra_kd,
                        "roi_per_value": roi_per_value
                    })
                break

priority_opportunities.sort(key=lambda x: x["roi_per_value"], reverse=True)

if priority_opportunities:
    p_cols = st.columns(min(3, len(priority_opportunities)))
    for idx, opp in enumerate(priority_opportunities[:3]):
        rank_label = f"الأولوية #{idx+1} 🏆" if idx == 0 else f"الأولوية #{idx+1}"
        with p_cols[idx]:
            st.markdown(f"""
                <div class="priority-card">
                    <span class="priority-rank">{rank_label}</span>
                    <h4 style="margin: 5px 0; color: #4F008C;">{opp['prod']}</h4>
                    <p style="margin: 0; font-size: 13px; color: #555;">
                        • تحتاج لبيع: <b>{opp['needed_units']} ڤاليو</b><br>
                        • الشريحة القادمة: <b>{opp['target_tier']}%</b><br>
                        • الزيادة بالعمولة: <b style="color: #28A745;">+{opp['extra_kd']:.2f} KD</b><br>
                        • قيمة الـ Value الواحدة: <b>{opp['roi_per_value']:.2f} KD/value</b>
                    </p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("🌟 **أنت حالياً في أعلى شريحة ممكنة لجميع المنتجات!**")

# -------------------------------------------------------------
# مؤشر سرعة الإنجاز مقابل الوقت (Pacing & Velocity Gauge) الجديد
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### ⏱️ Pacing & Velocity Gauge | مؤشر سرعة الإنجاز مقابل الوقت")

now = datetime.now()
current_day = now.day
total_days = calendar.monthrange(now.year, now.month)[1]
days_remaining = max(1, total_days - current_day)
time_elapsed_pct = current_day / total_days

st.info(f"📅 **الوضع الزمني للشهر:** اليوم **{current_day}** من أصل **{total_days}** يوم ({now.strftime('%B %Y')}) — نسبة الوقت المنقضي من الشهر: **{time_elapsed_pct*100:.1f}%**")

pacing_cols = st.columns(5)
products_tracker = [
    ("GA Voice", ach_ga_voice, target_ga_voice),
    ("GA Data", ach_ga_data, target_ga_data),
    ("Renew Voice", ach_renew_voice, target_renew_voice),
    ("Renew Data", ach_renew_data, target_renew_data),
    ("Zeed", ach_zeed, target_zeed),
]

for idx, (prod_name, ach, tgt) in enumerate(products_tracker):
    ach_pct = (ach / tgt) if tgt > 0 else 0
    # الفرق بين نسبة الإنجاز الفعلية ونسبة الوقت المنقضي
    pacing_diff = ach_pct - time_elapsed_pct
    
    if pacing_diff >= 0.05:
        status_class = "pacing-ahead"
        status_text = "🚀 متقدم عن الوقت"
        status_color = "#17A2B8"
    elif pacing_diff >= -0.05:
        status_class = "pacing-on-track"
        status_text = "✅ مسار مثالي"
        status_color = "#28A745"
    else:
        status_class = "pacing-lagging"
        status_text = "⚠️ متأخر عن الخطة"
        status_color = "#DC3545"
        
    rem_needed = max(0, tgt - ach)
    daily_req = rem_needed / days_remaining

    with pacing_cols[idx]:
        st.markdown(f"""
            <div class="pacing-card {status_class}">
                <h4 style="margin: 0; color: #4F008C; font-size: 15px;">{prod_name}</h4>
                <p style="margin: 4px 0; font-size: 12px; color: #666;">الإنجاز: <b>{ach_pct*100:.1f}%</b></p>
                <p style="margin: 2px 0; font-size: 12px; color: {status_color}; font-weight: bold;">{status_text}</p>
                <hr style="margin: 6px 0; border: none; border-top: 1px solid #eee;">
                <p style="margin: 0; font-size: 11px; color: #555;">المطلوب يومياً:<br><b style="font-size: 14px; color: #333;">{daily_req:.1f} وحدة/يوم</b></p>
            </div>
        """, unsafe_allow_html=True)

# KPI Breakdown
st.markdown("---")
st.markdown("### 📋 Operational KPIs Score Breakdown (20%)")
kpi_data = [
    {"KPI": "STC Care", "Achieved Score": f"{kpi1*100:.0f}%", "Min Threshold": "60%", "Earned Weight": f"{kpi1_w*100:.2f}%", "Status": "✅ Qualified" if kpi1 >= 0.60 else "❌ Below Threshold"},
    {"KPI": "W&P", "Achieved Score": f"{kpi2*100:.0f}%", "Min Threshold": "75%", "Earned Weight": f"{kpi2_w*100:.2f}%", "Status": "✅ Qualified" if kpi2 >= 0.75 else "❌ Below Threshold"},
    {"KPI": "Accessories", "Achieved Score": f"{kpi3*100:.0f}%", "Min Threshold": "75%", "Earned Weight": f"{kpi3_w*100:.2f}%", "Status": "✅ Qualified" if kpi3 >= 0.75 else "❌ Below Threshold"},
    {"KPI": "MNP", "Achieved Score": f"{kpi4*100:.0f}%", "Min Threshold": "75%", "Earned Weight": f"{kpi4_w*100:.2f}%", "Status": "✅ Qualified" if kpi4 >= 0.75 else "❌ Below Threshold"},
]
st.table(kpi_data)

# Smart Sales Insights & Advice (Including Threshold Jump Warning)
st.markdown("---")
st.markdown("### 💡 Smart Sales Insights & Advice | النصائح والتنبيهات الذكية بالأرقام")

insights = []

# تنبيه الفجوة الحرجة (Threshold Jump Warning)
critical_jumps = []
for opp in priority_opportunities:
    if opp["needed_units"] == 1:
        critical_jumps.append(f"<b>{opp['prod']}</b> للانتقال إلى شريحة <b>{opp['target_tier']}%</b> (زيادة متوقعة: <span style='color:#28A745; font-weight:bold;'>+{opp['extra_kd']:.2f} KD</span>)")

if critical_jumps:
    jumps_text = "<br>• ".join(critical_jumps)
    insights.append({
        "style": "insight-warning",
        "en": f"🚨 <b>THRESHOLD JUMP ALERT!</b> You are only <b>1 unit away</b> from a major tier upgrade on:<br>• {jumps_text}. Close this sale immediately to maximize your commission!",
        "ar": f"🚨 <b>تنبيه قفزة الشرائح (فجوة وحدة واحدة):</b> أنت على بعد <b>بيع وحدة واحدة فقط (1 Value)</b> للانتقال لشريحة أعلى في:<br>• {jumps_text}. أنجز هذه البيعة فوراً لتعظيم عمولتك!"
    })

# تنبيهات السرعة الزمنية (Pacing Warning)
lagging_prods = []
for prod_name, ach, tgt in products_tracker:
    ach_pct = (ach / tgt) if tgt > 0 else 0
    if ach_pct < (time_elapsed_pct - 0.05):
        lagging_prods.append(f"<b>{prod_name}</b> (معدل الإنجاز {ach_pct*100:.1f}% مقابل مرور {(time_elapsed_pct)*100:.1f}% من الشهر)")

if lagging_prods:
    lagging_text = "<br>• ".join(lagging_prods)
    insights.append({
        "style": "insight-error",
        "en": f"⚠️ <b>Velocity Warning:</b> The following products are lagging behind the monthly time pace. Consider increasing daily efforts:<br>• " + "<br>• ".join([p.split('(')[0] for p in lagging_prods]),
        "ar": f"⚠️ <b>تنبيه سرعة الإنجاز (Pacing):</b> المنتجات التالية تسير بمعدل أبطأ من الوقت المنقضي من الشهر، وتتطلب تكثيف الجهود:<br>• {lagging_text}"
    })

if min_weighted_ach < 0.75:
    weak_details = []
    for prod, weight in weighted_ach.items():
        if weight < 0.75:
            tgt = targets_map[prod]
            ach = achieved_map[prod]
            needed_raw = (0.75 - total_kpi_weight) / 0.8
            needed_units = max(1, int(needed_raw * tgt) - ach + 1)
            weak_details.append(f"<b>{prod}</b>: تحتاج إلى <b>{needed_units} ڤاليو</b>")

    weak_text_ar = "<br>• ".join(weak_details)
    weak_text_en = ", ".join([f"{p}" for p in weak_details])

    if avg_weighted_ach >= 0.75:
        insights.append({
            "style": "insight-warning",
            "en": f"⚠️ <b>Unlock Standard Scheme:</b> You are currently on Bonus. Complete the following values to reach 75% across all products:<br>• {weak_text_en}",
            "ar": f"⚠️ <b>لتفعيل العمولة الأساسية (Standard):</b> أنت مؤهل حالياً لـ Bonus فقط. تحتاج للوصول لـ 75% في جميع المنتجات إلى تحقيق:<br>• {weak_text_ar}"
        })
    else:
        insights.append({
            "style": "insight-error",
            "en": f"🔴 <b>Ineligible Status:</b> You need to achieve the following values to reach the minimum payout threshold (75%):<br>• {weak_text_en}",
            "ar": f"🔴 <b>تنبيه عدم الاستحقاق (0 KD):</b> أنت أقل من 75%. تحتاج لتحقيق الـ Values التالية للوصول للحد الأدنى للعمولة:<br>• {weak_text_ar}"
        })

failed_kpi_details = []
if kpi1 < 0.60: failed_kpi_details.append(f"<b>STC Care</b> (تحتاج زيادة {int((0.60 - kpi1)*100)}%)")
if kpi2 < 0.75: failed_kpi_details.append(f"<b>W&P</b> (تحتاج زيادة {int((0.75 - kpi2)*100)}%)")
if kpi3 < 0.75: failed_kpi_details.append(f"<b>Accessories</b> (تحتاج زيادة {int((0.75 - kpi3)*100)}%)")
if kpi4 < 0.75: failed_kpi_details.append(f"<b>MNP</b> (تحتاج زيادة {int((0.75 - kpi4)*100)}%)")

if failed_kpi_details:
    insights.append({
        "style": "insight-info",
        "en": f"🎯 <b>KPI Cash Boost:</b> Raise these KPIs to unlock up to 20% weight:<br>• " + "<br>• ".join(failed_kpi_details),
        "ar": f"🎯 <b>فرصة زيادة الموزون للـ KPIs:</b> قم بزيادة المؤشرات التالية للحصول على وزن أكبر ورفع عمولتك مباشرة:<br>• " + "<br>• ".join(failed_kpi_details)
    })

if insights:
    for item in insights:
        st.markdown(f"""
            <div class="insight-box {item['style']}">
                <div class="text-en">{item['en']}</div>
                <div class="text-ar">{item['ar']}</div>
            </div>
        """, unsafe_allow_html=True)

# Printable HTML / PDF Generator
st.markdown("---")
st.markdown("### 📄 Export Performance Report | تصدير تقرير الأداء")

html_report = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>stc Sales Incentive Report - The Avenues</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 30px; background: #fff; color: #333; }}
        .header {{ background: #4F008C; color: #fff; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .card {{ background: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin-bottom: 15px; }}
        .total {{ background: #FF007A; color: #fff; font-size: 24px; font-weight: bold; padding: 15px; border-radius: 8px; text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #4F008C; color: white; }}
        @media print {{ .print-btn {{ display: none; }} }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()" style="background:#FF007A; color:white; padding:12px 24px; border:none; border-radius:6px; font-weight:bold; cursor:pointer; margin-bottom:20px;">
        🖨️ Save as PDF / Print Report
    </button>
    <div class="header">
        <h1>stc Sales Incentive Performance Report (The Avenues)</h1>
        <p>Generated Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    
    <div class="card">
        <h3>Qualification Status: {eligibility_status}</h3>
        <p>Earned KPI Weight: {total_kpi_weight*100:.1f}% | Min Weighted Ach: {min_weighted_ach*100:.1f}% | Avg Weighted Ach: {avg_weighted_ach*100:.1f}%</p>
    </div>

    <div class="total">Total Final Payout: {total_final_payout:.2f} KD</div>

    <h3>Sales Achievement Breakdown</h3>
    <table>
        <tr><th>Product</th><th>Achieved</th><th>Target</th><th>Raw Ach %</th><th>Weighted Ach %</th></tr>
        <tr><td>GA Voice</td><td>{ach_ga_voice}</td><td>{target_ga_voice}</td><td>{raw_ga_voice*100:.1f}%</td><td>{weighted_ach['GA Voice']*100:.1f}%</td></tr>
        <tr><td>GA Data</td><td>{ach_ga_data}</td><td>{target_ga_data}</td><td>{raw_ga_data*100:.1f}%</td><td>{weighted_ach['GA Data']*100:.1f}%</td></tr>
        <tr><td>Renew Voice</td><td>{ach_renew_voice}</td><td>{target_renew_voice}</td><td>{raw_renew_voice*100:.1f}%</td><td>{weighted_ach['Renew Voice']*100:.1f}%</td></tr>
        <tr><td>Renew Data</td><td>{ach_renew_data}</td><td>{target_renew_data}</td><td>{raw_renew_data*100:.1f}%</td><td>{weighted_ach['Renew Data']*100:.1f}%</td></tr>
        <tr><td>Zeed</td><td>{ach_zeed}</td><td>{target_zeed}</td><td>{raw_zeed*100:.1f}%</td><td>{weighted_ach['Zeed']*100:.1f}%</td></tr>
    </table>

    <script>
        window.onload = function() {{ window.print(); }};
    </script>
</body>
</html>"""

exp_col1, exp_col2 = st.columns([0.7, 0.3])
with exp_col1:
    st.write("اضغط على الزر لتنزيل ملف التقرير. بمجرد فتح الملف على جهازك سيتكفل المتصفح بفتح نافذة التصدير لـ **PDF** فوراً.")
with exp_col2:
    st.download_button(
        label="📥 Download PDF Report",
        data=html_report,
        file_name=f"stc_Incentive_Report_Avenues_{datetime.now().strftime('%Y_%m_%d')}.html",
        mime="text/html",
        use_container_width=True
    )
