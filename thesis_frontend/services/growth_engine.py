import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.crop_service import CropService

# ==========================================
# 🌱 GROWTH STANDARDS (Via CropService)
# ==========================================
# Now using centralized data


def get_ideal_value(crop, hst, metric):
    """Interpolate ideal value closest to HST"""
    # Fetch from Service
    std = CropService.get_growth_standards(crop)
    if not std:
        # Fallback to similar crops if specific not found
        if "Cabai" in crop: std = CropService.get_growth_standards("Cabai Merah")
        elif "Melon" in crop: std = CropService.get_growth_standards("Melon (Premium)")
        else: return 0
        
    standards = std.get("targets", {})
    days = sorted(standards.keys())
    
    if not days: return 0
    
    # Logic Simple: Find closest days (Prev & Next)
    prev_day = days[0]
    next_day = days[-1]
    
    for d in days:
        if d <= hst: prev_day = d
        if d >= hst: 
            next_day = d
            break
            
    val_prev = standards[prev_day].get(metric, 0)
    val_next = standards[next_day].get(metric, 0)
    
    if prev_day == next_day:
        return val_prev
        
    # Linear Interpolation
    slope = (val_next - val_prev) / (next_day - prev_day)
    interpolated = val_prev + slope * (hst - prev_day)
    return interpolated

def evaluate_growth(crop, hst, height, stem, leaf_color_idx):
    feedback = []
    status = "Normal"
    score = 100
    
    # 1. Height Check
    ideal_h = get_ideal_value(crop, hst, "height")
    if ideal_h > 0:
        dev_h = (height - ideal_h) / ideal_h
        if dev_h < -0.25:
            feedback.append("⚠️ **Kerdil (Stunted):** Tinggi tanaman di bawah standar (-{:.0f}%). Cek kecukupan air dan Nitrogen.".format(abs(dev_h)*100))
            status = "Perlu Perhatian"
            score -= 20
        elif dev_h > 0.30:
            feedback.append("⚠️ **Etiolasi (Kutilang):** Tanaman terlalu tinggi dan kurus. Kemungkinan kurang sinar matahari.")
            status = "Warning"
            score -= 15
        else:
            feedback.append("✅ Tinggi tanaman optimal sesuai umur.")

    # 2. Stem Check (Kekokohan)
    ideal_s = get_ideal_value(crop, hst, "stem")
    if ideal_s > 0 and stem > 0:
        dev_s = (stem - ideal_s) / ideal_s
        if dev_s < -0.20:
             feedback.append("⚠️ **Batang Kecil:** Batang kurang kokoh. Pertimbangkan penambahan Kalium (K) dan Kalsium (Ca).")
             score -= 10
        elif dev_s > 0.20:
             feedback.append("✅ **Batang Kokoh:** Perkembangan vegetatif sangat baik.")
             score += 5

    # 3. Leaf Color (Nitrogen Indicator)
    # Scale 1 (Pale Yellow) to 4 (Dark Green)
    if leaf_color_idx == 1:
        feedback.append("🍂 **Klorosis (Kuning):** Defisiensi Nitrogen parah atau pH tanah bermasalah. Segera aplikasi pupuk daun N tinggi.")
        status = "Kritis"
        score -= 30
    elif leaf_color_idx == 2:
        feedback.append("🍃 **Hijau Muda:** Indikasi kurang Nitrogen. Naikkan dosis pupuk N (Urea/AB Mix).")
        score -= 10
    elif leaf_color_idx == 4:
        feedback.append("🌿 **Hijau Gelap:** Kadar N sangat cukup (mungkin berlebih). Hati-hati serangan hama penghisap.")
    
    return status, score, feedback
