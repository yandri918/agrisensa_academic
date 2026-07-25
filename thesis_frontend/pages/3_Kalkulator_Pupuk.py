# Kalkulator Pupuk Holistik - Enhanced Version
# Hitung kebutuhan pupuk presisi dengan jadwal pemupukan bertahap untuk hasil optimal

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Kalkulator Pupuk Holistik", page_icon="🧮", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== DATA ==========
# Kebutuhan NPK per hektar untuk berbagai tanaman (kg/ha)
CROP_NPK_REQUIREMENTS = {
    "Padi": {"N": 120, "P": 60, "K": 60, "description": "Padi sawah irigasi"},
    "Jagung": {"N": 200, "P": 90, "K": 60, "description": "Jagung hibrida"},
    "Kedelai": {"N": 50, "P": 100, "K": 75, "description": "Kedelai varietas unggul"},
    "Cabai Merah": {"N": 180, "P": 120, "K": 150, "description": "Cabai merah besar"},
    "Cabai Rawit": {"N": 150, "P": 100, "K": 120, "description": "Cabai rawit"},
    "Tomat": {"N": 150, "P": 100, "K": 120, "description": "Tomat varietas unggul"},
    "Kentang": {"N": 180, "P": 120, "K": 180, "description": "Kentang konsumsi"},
    "Bawang Merah": {"N": 120, "P": 90, "K": 90, "description": "Bawang merah"},
    "Bawang Putih": {"N": 100, "P": 80, "K": 80, "description": "Bawang putih"},
}

# Kandungan NPK pupuk (%)
FERTILIZER_CONTENT = {
    # Anorganik
    "Urea": {"N": 46, "P": 0, "K": 0, "price_per_kg": 2500, "type": "anorganik"},
    "SP-36": {"N": 0, "P": 36, "K": 0, "price_per_kg": 3000, "type": "anorganik"},
    "KCl": {"N": 0, "P": 0, "K": 60, "price_per_kg": 3500, "type": "anorganik"},
    "NPK 15-15-15": {"N": 15, "P": 15, "K": 15, "price_per_kg": 4000, "type": "anorganik"},
    "NPK 16-16-16": {"N": 16, "P": 16, "K": 16, "price_per_kg": 4200, "type": "anorganik"},
    "ZA": {"N": 21, "P": 0, "K": 0, "price_per_kg": 2000, "type": "anorganik"},
    # Organik
    "Kompos": {"N": 1.5, "P": 1.0, "K": 1.5, "price_per_kg": 500, "type": "organik"},
    "Pupuk Kandang": {"N": 2.0, "P": 1.5, "K": 2.0, "price_per_kg": 300, "type": "organik"},
    "Guano": {"N": 10, "P": 12, "K": 2, "price_per_kg": 5000, "type": "organik"},
    "Kascing": {"N": 2.5, "P": 2.0, "K": 1.5, "price_per_kg": 2000, "type": "organik"},
}

# Growth phases for different crops
GROWTH_PHASES = {
    "Padi": [
        {"phase": "Vegetatif Awal", "days": "0-21", "N": 40, "P": 100, "K": 30},
        {"phase": "Vegetatif Akhir", "days": "22-50", "N": 30, "P": 0, "K": 30},
        {"phase": "Generatif", "days": "51-90", "N": 30, "P": 0, "K": 40},
    ],
    "Jagung": [
        {"phase": "Vegetatif", "days": "0-30", "N": 50, "P": 100, "K": 40},
        {"phase": "Pembungaan", "days": "31-60", "N": 30, "P": 0, "K": 30},
        {"phase": "Pengisian Biji", "days": "61-90", "N": 20, "P": 0, "K": 30},
    ],
    "Cabai Merah": [
        {"phase": "Vegetatif", "days": "0-30", "N": 30, "P": 50, "K": 20},
        {"phase": "Pembungaan", "days": "31-60", "N": 25, "P": 30, "K": 30},
        {"phase": "Pembuahan 1", "days": "61-90", "N": 20, "P": 10, "K": 25},
        {"phase": "Pembuahan 2", "days": "91-120", "N": 25, "P": 10, "K": 25},
    ],
}

# ========== FUNCTIONS ==========
def calculate_fertilizer_needs(area_ha, crop, soil_npk=None):
    """Calculate fertilizer needs"""
    requirements = CROP_NPK_REQUIREMENTS[crop]
    
    # Adjust for soil NPK if provided (in ppm, convert to kg/ha)
    # Assumption: 1 ppm ≈ 2 kg/ha for top 20cm soil
    if soil_npk:
        # Reduce requirement based on existing soil NPK
        n_from_soil = (soil_npk['N'] * 2) / 1000  # ppm to kg/ha
        p_from_soil = (soil_npk['P'] * 2) / 1000
        k_from_soil = (soil_npk['K'] * 2) / 1000
        
        n_needed = max(0, requirements['N'] - n_from_soil)
        p_needed = max(0, requirements['P'] - p_from_soil)
        k_needed = max(0, requirements['K'] - k_from_soil)
    else:
        n_needed = requirements['N']
        p_needed = requirements['P']
        k_needed = requirements['K']
    
    # Total for area
    total_n = n_needed * area_ha
    total_p = p_needed * area_ha
    total_k = k_needed * area_ha
    
    return {
        'N': total_n,
        'P': total_p,
        'K': total_k,
        'per_ha': {'N': n_needed, 'P': p_needed, 'K': k_needed}
    }

def calculate_fertilizer_amount(npk_needs, fertilizer_type):
    """Calculate amount of fertilizer needed"""
    content = FERTILIZER_CONTENT[fertilizer_type]
    
    results = {}
    for nutrient in ['N', 'P', 'K']:
        if content[nutrient] > 0:
            # Amount needed = (nutrient needed / content %) * 100
            amount = (npk_needs[nutrient] / content[nutrient]) * 100
            results[nutrient] = amount
        else:
            results[nutrient] = 0
    
    return results

# ========== MAIN APP ==========
st.title("🧮 Kalkulator Pupuk Holistik")
st.markdown("**Hitung kebutuhan pupuk NPK berdasarkan luas lahan dan jenis tanaman**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Langkah-langkah:**
    1. Pilih jenis tanaman yang akan ditanam
    2. Masukkan luas lahan (dalam hektar atau m²)
    3. (Opsional) Input data NPK tanah jika sudah ada hasil uji lab
    4. Pilih jenis pupuk yang akan digunakan
    5. Lihat hasil perhitungan kebutuhan pupuk
    
    **Tips:**
    - Jika ada data NPK tanah, input untuk hasil lebih akurat
    - Gunakan kombinasi pupuk tunggal (Urea, SP-36, KCl) untuk efisiensi biaya
    - Atau gunakan NPK majemuk untuk kemudahan aplikasi
    """)

# Input Section
st.subheader("📝 Input Data")

col1, col2 = st.columns(2)

with col1:
    crop = st.selectbox(
        "Jenis Tanaman *",
        options=list(CROP_NPK_REQUIREMENTS.keys()),
        help="Pilih jenis tanaman yang akan ditanam"
    )
    
    st.info(f"ℹ️ {CROP_NPK_REQUIREMENTS[crop]['description']}")
    
    # Area input
    area_unit = st.radio("Satuan Luas", ["Hektar (ha)", "Meter Persegi (m²)"], horizontal=True)
    
    if area_unit == "Hektar (ha)":
        area_input = st.number_input("Luas Lahan (ha)", min_value=0.01, value=1.0, step=0.1, format="%.2f")
        area_ha = area_input
    else:
        area_input = st.number_input("Luas Lahan (m²)", min_value=100.0, value=10000.0, step=100.0)
        area_ha = area_input / 10000  # Convert to hectare

with col2:
    st.markdown("**Data NPK Tanah (Opsional)**")
    st.caption("Jika ada hasil uji lab tanah, input di sini untuk perhitungan lebih akurat")
    
    use_soil_data = st.checkbox("Saya punya data NPK tanah")
    
    if use_soil_data:
        soil_n = st.number_input("Nitrogen Tanah (ppm)", min_value=0.0, value=2000.0, step=100.0)
        soil_p = st.number_input("Fosfor Tanah (ppm)", min_value=0.0, value=15.0, step=1.0)
        soil_k = st.number_input("Kalium Tanah (ppm)", min_value=0.0, value=2000.0, step=100.0)
        
        soil_npk = {'N': soil_n, 'P': soil_p, 'K': soil_k}
    else:
        soil_npk = None
        st.info("💡 Tanpa data tanah, perhitungan menggunakan kebutuhan standar")

# Calculate
if st.button("🔍 Hitung Kebutuhan Pupuk", type="primary", use_container_width=True):
    
    # Calculate NPK needs
    npk_needs = calculate_fertilizer_needs(area_ha, crop, soil_npk)
    
    # --- AUTO-LOG TO JOURNAL ---
    try:
        from utils.journal_utils import log_to_journal
        log_to_journal(
            category="🧮 Kalkulator Pupuk",
            title=f"Analisis Kebutuhan Pupuk: {crop}",
            notes=f"Luas Lahan: {area_ha} ha. Target Nutrisi: N={npk_needs['N']:.1f}, P={npk_needs['P']:.1f}, K={npk_needs['K']:.1f} kg. Lahan: {area_ha} ha.",
            priority="Sedang"
        )
    except Exception as e:
        pass
        
    st.markdown("---")
    st.subheader("📊 Hasil Perhitungan")
    
    # Display NPK needs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nitrogen (N)", f"{npk_needs['N']:.2f} kg", 
                 delta=f"{npk_needs['per_ha']['N']:.1f} kg/ha")
    with col2:
        st.metric("Fosfor (P)", f"{npk_needs['P']:.2f} kg",
                 delta=f"{npk_needs['per_ha']['P']:.1f} kg/ha")
    with col3:
        st.metric("Kalium (K)", f"{npk_needs['K']:.2f} kg",
                 delta=f"{npk_needs['per_ha']['K']:.1f} kg/ha")
    
    # Fertilizer recommendations
    st.markdown("---")
    st.subheader("💊 Rekomendasi Pupuk")
    
    tab1, tab2, tab3 = st.tabs(["Pupuk Tunggal (Ekonomis)", "Pupuk Majemuk (Praktis)", "Mix Organik + Anorganik (Sehat)"])
    
    with tab1:
        st.markdown("**Menggunakan kombinasi Urea, SP-36, dan KCl**")
        
        # Calculate for single fertilizers
        urea_needed = calculate_fertilizer_amount(npk_needs, "Urea")['N']
        sp36_needed = calculate_fertilizer_amount(npk_needs, "SP-36")['P']
        kcl_needed = calculate_fertilizer_amount(npk_needs, "KCl")['K']
        
        # Calculate costs
        urea_cost = urea_needed * FERTILIZER_CONTENT["Urea"]["price_per_kg"]
        sp36_cost = sp36_needed * FERTILIZER_CONTENT["SP-36"]["price_per_kg"]
        kcl_cost = kcl_needed * FERTILIZER_CONTENT["KCl"]["price_per_kg"]
        total_cost = urea_cost + sp36_cost + kcl_cost
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            **Urea (46% N)**
            - Jumlah: **{urea_needed:.2f} kg**
            - Karung (50kg): **{urea_needed/50:.1f} karung**
            - Biaya: **Rp {urea_cost:,.0f}**
            """)
        with col2:
            st.markdown(f"""
            **SP-36 (36% P)**
            - Jumlah: **{sp36_needed:.2f} kg**
            - Karung (50kg): **{sp36_needed/50:.1f} karung**
            - Biaya: **Rp {sp36_cost:,.0f}**
            """)
        with col3:
            st.markdown(f"""
            **KCl (60% K)**
            - Jumlah: **{kcl_needed:.2f} kg**
            - Karung (50kg): **{kcl_needed/50:.1f} karung**
            - Biaya: **Rp {kcl_cost:,.0f}**
            """)
        
        st.success(f"💰 **Total Biaya Pupuk: Rp {total_cost:,.0f}**")
    
    with tab2:
        st.markdown("**Menggunakan NPK Majemuk**")
        
        # Calculate for NPK 15-15-15
        npk_1515_for_n = calculate_fertilizer_amount(npk_needs, "NPK 15-15-15")['N']
        npk_1515_for_p = calculate_fertilizer_amount(npk_needs, "NPK 15-15-15")['P']
        npk_1515_for_k = calculate_fertilizer_amount(npk_needs, "NPK 15-15-15")['K']
        
        # Use the maximum (limiting factor)
        npk_1515_needed = max(npk_1515_for_n, npk_1515_for_p, npk_1515_for_k)
        npk_1515_cost = npk_1515_needed * FERTILIZER_CONTENT["NPK 15-15-15"]["price_per_kg"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **NPK 15-15-15**
            - Jumlah: **{npk_1515_needed:.2f} kg**
            - Karung (50kg): **{npk_1515_needed/50:.1f} karung**
            - Biaya: **Rp {npk_1515_cost:,.0f}**
            """)
        
        # Calculate for NPK 16-16-16
        npk_1616_for_n = calculate_fertilizer_amount(npk_needs, "NPK 16-16-16")['N']
        npk_1616_for_p = calculate_fertilizer_amount(npk_needs, "NPK 16-16-16")['P']
        npk_1616_for_k = calculate_fertilizer_amount(npk_needs, "NPK 16-16-16")['K']
        
        npk_1616_needed = max(npk_1616_for_n, npk_1616_for_p, npk_1616_for_k)
        npk_1616_cost = npk_1616_needed * FERTILIZER_CONTENT["NPK 16-16-16"]["price_per_kg"]
        
        with col2:
            st.markdown(f"""
            **NPK 16-16-16**
            - Jumlah: **{npk_1616_needed:.2f} kg**
            - Karung (50kg): **{npk_1616_needed/50:.1f} karung**
            - Biaya: **Rp {npk_1616_cost:,.0f}**
            """)
        
        st.info("💡 NPK majemuk lebih praktis tapi biasanya lebih mahal. Pilih sesuai budget dan kemudahan aplikasi.")
    
    with tab3:
        st.markdown("**Kombinasi Pupuk Organik + Anorganik untuk Kesehatan Tanah Jangka Panjang**")
        
        # 30% from organic, 70% from inorganic
        organic_ratio = 0.3
        inorganic_ratio = 0.7
        
        # Organic contribution (using Kompos)
        kompos_for_n = (npk_needs['N'] * organic_ratio / FERTILIZER_CONTENT['Kompos']['N']) * 100
        kompos_for_p = (npk_needs['P'] * organic_ratio / FERTILIZER_CONTENT['Kompos']['P']) * 100
        kompos_for_k = (npk_needs['K'] * organic_ratio / FERTILIZER_CONTENT['Kompos']['K']) * 100
        kompos_needed = max(kompos_for_n, kompos_for_p, kompos_for_k)
        
        # Inorganic contribution (reduced by organic)
        reduced_n = npk_needs['N'] * inorganic_ratio
        reduced_p = npk_needs['P'] * inorganic_ratio
        reduced_k = npk_needs['K'] * inorganic_ratio
        
        urea_mix = (reduced_n / FERTILIZER_CONTENT['Urea']['N']) * 100
        sp36_mix = (reduced_p / FERTILIZER_CONTENT['SP-36']['P']) * 100
        kcl_mix = (reduced_k / FERTILIZER_CONTENT['KCl']['K']) * 100
        
        # Calculate costs
        kompos_cost = kompos_needed * FERTILIZER_CONTENT['Kompos']['price_per_kg']
        urea_mix_cost = urea_mix * FERTILIZER_CONTENT['Urea']['price_per_kg']
        sp36_mix_cost = sp36_mix * FERTILIZER_CONTENT['SP-36']['price_per_kg']
        kcl_mix_cost = kcl_mix * FERTILIZER_CONTENT['KCl']['price_per_kg']
        total_mix_cost = kompos_cost + urea_mix_cost + sp36_mix_cost + kcl_mix_cost
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Pupuk Organik (30%):**")
            st.markdown(f"""
            **Kompos**
            - Jumlah: **{kompos_needed:.2f} kg**
            - Karung (50kg): **{kompos_needed/50:.1f} karung**
            - Biaya: **Rp {kompos_cost:,.0f}**
            
            *Manfaat: Memperbaiki struktur tanah, meningkatkan mikroorganisme*
            """)
        
        with col2:
            st.markdown("**Pupuk Anorganik (70%):**")
            st.markdown(f"""
            - **Urea:** {urea_mix:.1f} kg (Rp {urea_mix_cost:,.0f})
            - **SP-36:** {sp36_mix:.1f} kg (Rp {sp36_mix_cost:,.0f})
            - **KCl:** {kcl_mix:.1f} kg (Rp {kcl_mix_cost:,.0f})
            
            *Manfaat: Nutrisi cepat tersedia untuk tanaman*
            """)
        
        st.success(f"💰 **Total Biaya: Rp {total_mix_cost:,.0f}**")
        st.info("""
        ✅ **Keunggulan Mix Organik + Anorganik:**
        - Kesehatan tanah jangka panjang
        - Nutrisi slow-release + fast-release
        - Meningkatkan kesuburan biologis tanah
        - Lebih ramah lingkungan
        """)
    
    # Visualization
    st.markdown("---")
    st.subheader("📈 Visualisasi Kebutuhan NPK")
    
    fig = go.Figure(data=[
        go.Bar(name='Nitrogen (N)', x=['Kebutuhan NPK'], y=[npk_needs['N']], marker_color='#3b82f6'),
        go.Bar(name='Fosfor (P)', x=['Kebutuhan NPK'], y=[npk_needs['P']], marker_color='#10b981'),
        go.Bar(name='Kalium (K)', x=['Kebutuhan NPK'], y=[npk_needs['K']], marker_color='#f59e0b')
    ])
    
    fig.update_layout(
        title=f"Kebutuhan NPK untuk {crop} ({area_ha:.2f} ha)",
        yaxis_title="Jumlah (kg)",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced Application schedule
    st.markdown("---")
    st.subheader("📅 Jadwal Pemupukan Detail")
    
    # Check if crop has growth phases
    if crop in GROWTH_PHASES:
        st.markdown(f"**Jadwal Pemupukan Berdasarkan Fase Pertumbuhan {crop}:**")
        
        phases = GROWTH_PHASES[crop]
        schedule_data = []
        
        for phase in phases:
            n_amount = (npk_needs['N'] * phase['N'] / 100)
            p_amount = (npk_needs['P'] * phase['P'] / 100)
            k_amount = (npk_needs['K'] * phase['K'] / 100)
            
            urea_phase = (n_amount / FERTILIZER_CONTENT['Urea']['N']) * 100
            sp36_phase = (p_amount / FERTILIZER_CONTENT['SP-36']['P']) * 100 if phase['P'] > 0 else 0
            kcl_phase = (k_amount / FERTILIZER_CONTENT['KCl']['K']) * 100
            
            schedule_data.append({
                'Fase': phase['phase'],
                'Hari': phase['days'],
                'Urea (kg)': f"{urea_phase:.1f}",
                'SP-36 (kg)': f"{sp36_phase:.1f}" if sp36_phase > 0 else "-",
                'KCl (kg)': f"{kcl_phase:.1f}",
                'N (%)': f"{phase['N']}%",
                'P (%)': f"{phase['P']}%",
                'K (%)': f"{phase['K']}%"
            })
        
        df_schedule = pd.DataFrame(schedule_data)
        st.dataframe(df_schedule, use_container_width=True, hide_index=True)
        
        # Download schedule
        csv = df_schedule.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Jadwal Pemupukan (CSV)",
            data=csv,
            file_name=f"jadwal_pemupukan_{crop}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        # Default schedule for crops without specific phases
        st.markdown(f"""
        **Rekomendasi waktu pemupukan untuk {crop}:**
        
        | Waktu | Jenis Pupuk | Dosis | Keterangan |
        |-------|-------------|-------|------------|
        | **Dasar (0 HST)** | Urea 50% + SP-36 100% + KCl 50% | {urea_needed*0.5:.1f} + {sp36_needed:.1f} + {kcl_needed*0.5:.1f} kg | Saat tanam/olah tanah |
        | **Susulan 1 (21 HST)** | Urea 25% + KCl 25% | {urea_needed*0.25:.1f} + {kcl_needed*0.25:.1f} kg | Fase vegetatif |
        | **Susulan 2 (42 HST)** | Urea 25% + KCl 25% | {urea_needed*0.25:.1f} + {kcl_needed*0.25:.1f} kg | Fase generatif |
        
        *HST = Hari Setelah Tanam
        """)
    
    st.warning("⚠️ **Catatan:** Jadwal ini adalah rekomendasi umum. Sesuaikan dengan kondisi tanaman dan cuaca di lapangan.")

# Footer
st.markdown("---")
st.caption("💡 Kalkulator ini menggunakan rekomendasi standar. Untuk hasil optimal, lakukan uji tanah di laboratorium.")
