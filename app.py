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

# فرز الفرص حسب أعلى عائد لكل value
priority_opportunities.sort(key=lambda x: x["roi_per_value"], reverse=True)

if priority_opportunities:
    p_cols = st.columns(min(3, len(priority_opportunities)))
    for idx, opp in enumerate(priority_opportunities[:3]):
        rank_badge = f"الأولوية الأولى 🏆" if idx == 0 else f"الأولوية #{idx+1}"
        border_color = "#FF007A" if idx == 0 else "#4F008C"
        bg_color = "#FFF5F9" if idx == 0 else "#FFFFFF"
        
        with p_cols[idx]:
            st.markdown(f"""
                <div style="
                    background: {bg_color}; 
                    border: 1px solid #E2D1F0; 
                    border-top: 5px solid {border_color}; 
                    border-radius: 14px; 
                    padding: 18px; 
                    margin-bottom: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
                    direction: rtl;
                    text-align: right;">
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="background: {border_color}; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px;">
                            {rank_badge}
                        </span>
                    </div>
                    
                    <h3 style="margin: 8px 0 14px 0; color: #4F008C; font-size: 20px; font-weight: 800;">
                        {opp['prod']}
                    </h3>
                    
                    <div style="font-size: 14px; color: #333; line-height: 1.8;">
                        <div style="margin-bottom: 6px;">
                            📌 <b>المطلوب:</b> <span style="color: #4F008C; font-weight: bold;">{opp['needed_units']}</span> بيعة (Values)
                        </div>
                        <div style="margin-bottom: 6px;">
                            🎯 <b>الشريحة القادمة:</b> <b>{opp['target_tier']}%</b>
                        </div>
                        <div style="margin-bottom: 6px;">
                            💰 <b>الزيادة بالعمولة:</b> <span style="color: #28A745; font-weight: bold;">+{opp['extra_kd']:.2f} د.ك</span>
                        </div>
                        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed #E2D1F0; background: #F8F9FA; padding: 8px; border-radius: 8px; text-align: center;">
                            ⚡ <b>ربح البيعة الواحدة:</b> <span style="color: #FF007A; font-weight: 800;">{opp['roi_per_value']:.2f} د.ك</span> / Value
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("🌟 **ما شاء الله! أنت حالياً في أعلى شريحة عمولة ممكنة لجميع المنتجات.**")
