import streamlit as st

st.set_page_config(page_title="حاسبة العمولات والحوافز", layout="wide")

# تنسيق الشاشة لدعم اللغة العربية (RTL)
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-baseweb="select"] { direction: rtl; }
    .stNumberInput { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 حاسبة عمولات المبيعات التفاعلية")

# 1. لوحة تحكم المدير
st.sidebar.header("⚙️ لوحة تحكم المدير (تعديل التارجت)")
target_ga_voice = st.sidebar.number_input("تارجت GA Voice (صوت جديد):", value=100)
target_ga_data = st.sidebar.number_input("تارجت GA Data (بيانات جديدة):", value=50)
target_renew_voice = st.sidebar.number_input("تارجت Renewal Voice (تجديد صوت):", value=40)
target_renew_data = st.sidebar.number_input("تارجت Renewal Data (تجديد بيانات):", value=30)
target_zeed = st.sidebar.number_input("تارجت Zeed (خدمات زيد):", value=20)

st.subheader("📥 إدخال الأداء والمبيعات المحققة للموظف")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1️⃣ المبيعات المحققة")
    ach_ga_voice = st.number_input("المحقق GA Voice:", min_value=0, value=100)
    ach_ga_data = st.number_input("المحقق GA Data:", min_value=0, value=45)
    ach_renew_voice = st.number_input("المحقق Renewal Voice:", min_value=0, value=32)
    ach_renew_data = st.number_input("المحقق Renewal Data:", min_value=0, value=15)
    ach_zeed = st.number_input("المحقق Zeed:", min_value=0, value=20)

with col2:
    st.markdown("### 2️⃣ مؤشرات الأداء التشغيلية (KPIs - 20%)")
    kpi1 = st.slider("KPI-1: STC Care (عناية العملاء %)", 0, 100, 85) / 100
    kpi2 = st.slider("KPI-2: W&P (الالتزام والانضباط %)", 0, 100, 80) / 100
    kpi3 = st.slider("KPI-3: Accessories (الإكسسوارات %)", 0, 100, 90) / 100
    kpi4 = st.slider("KPI-4: MNP (تحويل الأرقام %)", 0, 100, 70) / 100

# حساب أوزان الـ KPIs حسب شروط الشيت
kpi1_w = (kpi1 * 0.05) if kpi1 >= 0.60 else 0
kpi2_w = (kpi2 * 0.05) if kpi2 >= 0.75 else 0
kpi3_w = (kpi3 * 0.05) if kpi3 >= 0.75 else 0
kpi4_w = (kpi4 * 0.05) if kpi4 >= 0.75 else 0
total_kpi_weight = kpi1_w + kpi2_w + kpi3_w + kpi4_w

# نسبة الإنجاز الخام
raw_ach = {
    'GA Voice': ach_ga_voice / target_ga_voice if target_ga_voice > 0 else 0,
    'GA Data': ach_ga_data / target_ga_data if target_ga_data > 0 else 0,
    'Renew Voice': ach_renew_voice / target_renew_voice if target_renew_voice > 0 else 0,
    'Renew Data': ach_renew_data / target_renew_data if target_renew_data > 0 else 0,
    'Zeed': ach_zeed / target_zeed if target_zeed > 0 else 0,
}

# النسبة الموزونة الإجمالية (80% للمنتج + 20% للـ KPIs)
weighted_ach = {k: (v * 0.8) + total_kpi_weight for k, v in raw_ach.items()}

# جدول البونص الإضافي (Bonus Scheme Matrix)
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
st.subheader("💰 ملخص العمولات والمستحقات")

res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric("وزن الـ KPIs المستحق", f"{total_kpi_weight*100:.1f}%")
res_col2.metric("مكافأة البونص الإضافية", f"{total_bonus} د.ك")
res_col3.metric("إجمالي المبلغ المستحق النهائي", f"{total_bonus} د.ك")
