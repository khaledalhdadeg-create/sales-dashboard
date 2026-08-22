import streamlit as st
import json
import os
import calendar
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="stc Sales Incentive Calculator", layout="wide", page_icon="📱")

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

# تحميل الأرقام الحالية للجميع
current_targets = load_targets()

# Custom CSS
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

# -------------------------------------------------------------
# Admin Sidebar (مخفي داخل قائمة منسدلة مغلقة تلقائياً)
# -------------------------------------------------------------
with st.sidebar.expander("⚙️ Admin Target Settings", expanded=False):
    ADMIN_PASSWORD = "CHV4"
    admin_pwd = st.text_input("Enter Admin Password:", type="password")

    if admin_pwd == ADMIN_PASSWORD:
        st.success("Unlocked: Admin Mode")
        
        with st.form("admin_target_form"):
            new_ga_voice = st.number_input("Target GA Voice:", value=int(current_targets["target_ga_voice"]))
            new_ga_data = st.number_input("Target GA Data:", value=int(current_targets["target_ga_data"]))
            new_renew_voice = st.number_input("Target Renewal Voice:", value=int(current_targets["target_renew_voice"]))
            new_renew_data = st.number_input("Target Renewal Data:", value=int(current_targets["target_renew_data"]))
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

        target_ga_voice = current_targets["target_ga_voice"]
        target_ga_data = current_targets["target_ga_data"]
        target_renew_voice = current_targets["target_renew_voice"]
        target_renew_data = current_targets["target_renew_data"]
        target_zeed = current_targets["target_zeed"]
    else:
        if admin_pwd != "":
            st.error("🔒 Incorrect Password")
        else:
            st.info("🔒 Targets Locked (View Mode)")
            
        target_ga_voice = current_targets["target_ga_voice"]
        target_ga_data = current_targets["target_ga_data"]
        target_renew_voice = current_targets["target_renew_voice"]
        target_renew_data = current_targets["target_renew_data"]
        target_zeed = current_targets["target_zeed"]
        
        st.text(f"Target GA Voice: {target_ga_voice}")
        st.text(f"Target GA Data: {target_ga_data}")
        st.text(f"Target Renewal Voice: {target_renew_voice}")
        st.text(f"Target Renewal Data: {target_renew_data}")
        st.text(f"Target Zeed: {target_zeed}")

st.sidebar.markdown("---")

# Layout Inputs
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

# Logic
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
        <p style="margin: 0; font-size: 15px; opacity: 0.9;">Total Final Payout</p>
        <h2>{total_final_payout:.2f} KD</h2>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# ميزة حاسبة Target اليومية (Daily Run-Rate Tracker - Automatic Date)
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 📈 Daily Target Tracker")

# جلب اليوم والشهر الحاليين تلقائياً من النظام
now = datetime.now()
current_day = now.day
total_days = calendar.monthrange(now.year, now.month)[1]

days_remaining = max(1, total_days - current_day)

# عرض معلومات الشهر واليوم تلقائياً
st.info(f"📅 **Today:** Day {current_day} of {total_days} ({now.strftime('%B %Y')}) | **Days Remaining:** {days_remaining} days")

products_tracker = [
    ("GA Voice", ach_ga_voice, target_ga_voice),
    ("GA Data", ach_ga_data, target_ga_data),
    ("Renew Voice", ach_renew_voice, target_renew_voice),
    ("Renew Data", ach_renew_data, target_renew_data),
    ("Zeed", ach_zeed, target_zeed),
]

tracker_cols = st.columns(5)

for idx, (prod_name, ach, tgt) in enumerate(products_tracker):
    rem_needed = max(0, tgt - ach)
    daily_req = rem_needed / days_remaining
    
    with tracker_cols[idx]:
        st.markdown(f"**{prod_name}**")
        st.caption(f"Remaining: {rem_needed} units")
        st.metric("Needed / Day", f"{daily_req:.1f}")

# -------------------------------------------------------------
# ميزة تفصيل نقاط الـ KPIs (KPI Weight Breakdown)
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 📋 Operational KPIs Score Breakdown (20%)")

kpi_data = [
    {"KPI": "STC Care", "Achieved Score": f"{kpi1*100:.0f}%", "Min Threshold": "60%", "Earned Weight": f"{kpi1_w*100:.2f}%", "Status": "✅ Qualified" if kpi1 >= 0.60 else "❌ Below Threshold"},
    {"KPI": "W&P", "Achieved Score": f"{kpi2*100:.0f}%", "Min Threshold": "75%", "Earned Weight": f"{kpi2_w*100:.2f}%", "Status": "✅ Qualified" if kpi2 >= 0.75 else "❌ Below Threshold"},
    {"KPI": "Accessories", "Achieved Score": f"{kpi3*100:.0f}%", "Min Threshold": "75%", "Earned Weight": f"{kpi3_w*100:.2f}%", "Status": "✅ Qualified" if kpi3 >= 0.75 else "❌ Below Threshold"},
    {"KPI": "MNP", "Achieved Score": f"{kpi4*100:.0f}%", "Min Threshold": "75%", "Earned Weight": f"{kpi4_w*100:.2f}%", "Status": "✅ Qualified" if kpi4 >= 0.75 else "❌ Below Threshold"},
]

st.table(kpi_data)
st.caption(f"💡 Total KPI Contribution to Final Achievement Weight: **{total_kpi_weight*100:.1f}% / 20.0%**")

# -------------------------------------------------------------
# ميزة النصائح والتنبيهات الذكية (Smart Sales Insights - Arabic & English)
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 💡 Smart Sales Insights & Advice | النصائح والتنبيهات الذكية")

insights = []

# 1. فحص التأهل للعمولة
if min_weighted_ach < 0.75 and avg_weighted_ach >= 0.75:
    weak_prods = [prod for prod, ach in weighted_ach.items() if ach < 0.75]
    insights.append((
        "warning",
        f"⚠️ **Boost Standard Eligibility | تحسين استحقاق الشرائح الأساسية:**<br>"
        f"You qualify for **Bonus Scheme** because these products are below 75%: **{', '.join(weak_prods)}**.<br>"
        f"أنت مؤهل حالياً لعمولة الـ Bonus لأن هذه المنتجات أقل من 75%: **{', '.join(weak_prods)}**. ارفعها لـ 75% لتأهل للعمولة الأساسية الأعلى!"
    ))
elif min_weighted_ach < 0.75 and avg_weighted_ach < 0.75:
    insights.append((
        "error",
        "🔴 **Ineligible Warning | تنبيه عدم الاستحقاق:**<br>"
        "Your Minimum Weighted Achievement and Average are below 75%. Focus on raising all product achievements above 75% to get paid.<br>"
        "نسبة الإنجاز الأدنى والمعدل أقل من 75%. ركز على رفع جميع المنتجات لأعلى من 75% لتستحق العمولة."
    ))

# 2. فحص الـ KPIs المؤثرة
failed_kpis = []
if kpi1 < 0.60: failed_kpis.append("STC Care (Needs ≥ 60%)")
if kpi2 < 0.75: failed_kpis.append("W&P (Needs ≥ 75%)")
if kpi3 < 0.75: failed_kpis.append("Accessories (Needs ≥ 75%)")
if kpi4 < 0.75: failed_kpis.append("MNP (Needs ≥ 75%)")

if failed_kpis:
    insights.append((
        "info",
        f"🎯 **KPI Opportunity | فرصة تحسين الـ KPIs:**<br>"
        f"Improve the following KPIs to gain full weight: **{', '.join(failed_kpis)}**.<br>"
        f"قم بتحسين مؤشرات الأداء التالية لتحصل على الوزن الكامل للـ KPIs: **{', '.join(failed_kpis)}**."
    ))

# 3. فحص الفرص المتاحة للانتقال لشرائح أعلى في المبيعات
thresholds = [0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40]
targets_map = {
    'GA Voice': target_ga_voice,
    'GA Data': target_ga_data,
    'Renew Voice': target_renew_voice,
    'Renew Data': target_renew_data,
    'Zeed': target_zeed
}
achieved_map = {
    'GA Voice': ach_ga_voice,
    'GA Data': ach_ga_data,
    'Renew Voice': ach_renew_voice,
    'Renew Data': ach_renew_data,
    'Zeed': ach_zeed
}

for prod, weight in weighted_ach.items():
    tgt = targets_map.get(prod, 0)
    ach = achieved_map.get(prod, 0)
    if tgt > 0:
        for t in thresholds:
            if weight < t:
                needed_raw = (t - total_kpi_weight) / 0.8
                needed_units = int(needed_raw * tgt) - ach + 1
                if 0 < needed_units <= 5:
                    insights.append((
                        "success",
                        f"🔥 **Near Next Tier ({prod}) | قريب من الشريحة التالية:**<br>"
                        f"You are just **{needed_units} unit(s)** away from unlocking the **{int(t*100)}%** tier payout!<br>"
                        f"باقي لك **{needed_units} خط/خطوط** فقط للوصول لشريحة **{int(t*100)}%** في عمولة {prod}!"
                    ))
                break

# عرض التنبيهات
if insights:
    for category, message in insights:
        if category == "warning":
            st.warning(message, icon="⚠️")
        elif category == "error":
            st.error(message, icon="🔴")
        elif category == "info":
            st.info(message, icon="🎯")
        elif category == "success":
            st.success(message, icon="🔥")
else:
    st.success("🌟 **Great Job!** All your metrics and targets are running at maximum performance!<br>عمل ممتاز! جميع أرقامك ومؤشراتك تعمل بأعلى مستوى أداء!", icon="🌟")
