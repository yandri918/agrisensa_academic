import os
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Optional, List, Union
from ml_models.model_loader import ModelLoader
from config import settings
from data.yield_benchmarks import YieldBenchmarks

logger = logging.getLogger("mlops_api.ml_service")

# Static fertilizer composition database
FERTILIZER_DATA = {
    # Pupuk Anorganik
    "urea": {"name": "Urea", "content": {"N": 0.46, "P": 0, "K": 0}, "type": "anorganik"},
    "sp36": {"name": "SP-36", "content": {"N": 0, "P": 0.158, "K": 0}, "type": "anorganik"},
    "kcl": {"name": "KCL (MOP)", "content": {"N": 0, "P": 0, "K": 0.50}, "type": "anorganik"},
    "npk_mutiara": {"name": "NPK Mutiara (16-16-16)", "content": {"N": 0.16, "P": 0.07, "K": 0.13}, "type": "anorganik"},
    
    # Pupuk Organik
    "kompos": {"name": "Kompos", "content": {"N": 0.015, "P": 0.01, "K": 0.015}, "type": "organik"},
    "pupuk_kandang_sapi": {"name": "Pupuk Kandang Sapi", "content": {"N": 0.005, "P": 0.0025, "K": 0.005}, "type": "organik"},
    "pupuk_kandang_ayam": {"name": "Pupuk Kandang Ayam", "content": {"N": 0.015, "P": 0.013, "K": 0.008}, "type": "organik"},
    "pupuk_kandang_kambing": {"name": "Pupuk Kandang Kambing", "content": {"N": 0.007, "P": 0.003, "K": 0.009}, "type": "organik"},
    "bokashi": {"name": "Bokashi", "content": {"N": 0.02, "P": 0.015, "K": 0.018}, "type": "organik"},
    "vermikompos": {"name": "Vermikompos (Kascing)", "content": {"N": 0.02, "P": 0.018, "K": 0.015}, "type": "organik"}
}

def get_dataset_path(filename: str) -> str:
    """Get path to dataset file."""
    return os.path.join(settings.ML_MODELS_PATH, filename)

def prepare_fao_features(data: Dict[str, Any]) -> np.ndarray:
    """Map NPK soil values to 5 FAO model features."""
    rainfall = float(data.get('rainfall', 1500.0))
    temperature = float(data.get('temperature', 27.0))
    pesticides = 10.0  # Average tonnes
    item_encoded = 1.0  # Default encoded crop
    year = 2026.0
    return np.array([[rainfall, pesticides, temperature, item_encoded, year]])

class MLService:
    """
    Business logic for Machine Learning functionalities.
    Translates and runs predictions on loaded Scikit-Learn/LightGBM models.
    """

    @staticmethod
    def recommend_crop(data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend crop based on soil and environmental conditions."""
        crop_model = ModelLoader.get_model('crop_recommendation')
        if crop_model is None:
            logger.warning("⚠️ Crop recommendation model not available, using fallback")
            # Fallback logic based on NPK ratios
            n = float(data.get('n_value', 0))
            p = float(data.get('p_value', 0))
            k = float(data.get('k_value', 0))
            
            # Simple heuristic
            if n > 80 and p > 40: return {"crop": "Rice", "confidence": 75.0, "details": {"description": "Padi adalah tanaman pangan utama."}}
            elif k > 40: return {"crop": "Cotton", "confidence": 70.0, "details": {"description": "Kapas adalah tanaman serat."}}
            elif p > 50: return {"crop": "Wheat", "confidence": 70.0, "details": {"description": "Gandum."}}
            else: return {"crop": "Maize", "confidence": 65.0, "details": {"description": "Jagung."}}
        
        # Features mapping
        features = [
            float(data.get('n_value', 0)),
            float(data.get('p_value', 0)),
            float(data.get('k_value', 0)),
            float(data.get('temperature', 0)),
            float(data.get('humidity', 0)),
            float(data.get('ph', 0)),
            float(data.get('rainfall', 0))
        ]
        input_data = np.array([features])
        
        # Predict
        prediction = crop_model.predict(input_data)[0]
        crop_name = prediction.capitalize()
        
        confidence = 0.0
        if hasattr(crop_model, 'predict_proba'):
            probs = crop_model.predict_proba(input_data)[0]
            confidence = round(max(probs) * 100, 2)
        else:
            confidence = 85.0  # Default confidence
            
        crop_details = {
            "Rice": {
                "description": "Padi adalah tanaman pangan utama yang membutuhkan banyak air.",
                "optimal_conditions": "Suhu 20-35°C, Curah hujan tinggi, pH 5.5-7.0.",
                "care_tips": "Pastikan pengairan cukup (tergenang), berikan pupuk Urea dan SP-36 secara teratur."
            },
            "Maize": {
                "description": "Jagung adalah tanaman serbaguna untuk pangan dan pakan ternak.",
                "optimal_conditions": "Suhu 20-30°C, Tanah gembur kaya organik, pH 5.8-7.0.",
                "care_tips": "Lakukan pembumbunan akar, waspadai ulat grayak, dan pupuk NPK seimbang."
            },
            "Chickpea": {
                "description": "Kacang Arab, sumber protein nabati tinggi.",
                "optimal_conditions": "Iklim sejuk hingga hangat, tanah berpasir/lempung, pH 6.0-9.0.",
                "care_tips": "Hindari tanah yang tergenang air, butuh sinar matahari penuh."
            },
            "Kidneybeans": {
                "description": "Kacang Merah, kaya serat dan protein.",
                "optimal_conditions": "Suhu 15-25°C, Curah hujan sedang, pH 6.0-7.0.",
                "care_tips": "Perlu ajir/lanjaran untuk merambat, jaga kelembaban tanah."
            },
            "Pigeonpeas": {
                "description": "Kacang Gude, tanaman tahan kering.",
                "optimal_conditions": "Suhu 18-30°C, Tahan kekeringan, pH 5.0-7.0.",
                "care_tips": "Bisa ditanam sebagai tanaman sela atau pagar hidup."
            },
            "Mothbeans": {
                "description": "Kacang Moth, sangat tahan kekeringan.",
                "optimal_conditions": "Iklim kering/semi-kering, Suhu tinggi, pH 6.5-8.0.",
                "care_tips": "Sangat minim perawatan, hindari penyiraman berlebih."
            },
            "Mungbean": {
                "description": "Kacang Hijau, umur pendek dan mudah tumbuh.",
                "optimal_conditions": "Suhu 25-35°C, Iklim panas, pH 5.8-7.0.",
                "care_tips": "Panen serempak saat polong berwarna hitam/coklat tua."
            },
            "Blackgram": {
                "description": "Kacang Hitam (Urad Dal), populer di Asia Selatan.",
                "optimal_conditions": "Suhu 25-35°C, Tanah liat berpasir, pH 6.0-7.0.",
                "care_tips": "Peka terhadap genangan air, butuh drainase baik."
            },
            "Lentil": {
                "description": "Lentil, tanaman legum biji-bijian.",
                "optimal_conditions": "Iklim dingin, Tanah berpasir, pH 6.0-7.5.",
                "care_tips": "Tanam di akhir musim hujan atau awal musim kemarau."
            },
            "Pomegranate": {
                "description": "Delima, tanaman buah perdu.",
                "optimal_conditions": "Iklim semi-kering, Suhu panas, pH 5.5-7.0.",
                "care_tips": "Lakukan pemangkasan rutin untuk bentuk pohon dan produksi buah."
            },
            "Banana": {
                "description": "Pisang, buah tropis populer.",
                "optimal_conditions": "Suhu 27°C, Curah hujan tinggi merata, pH 6.0-7.0.",
                "care_tips": "Butuh banyak air dan pupuk Kalium, bersihkan anakan secara rutin."
            },
            "Mango": {
                "description": "Mangga, raja buah tropis.",
                "optimal_conditions": "Suhu 24-30°C, Musim kering tegas untuk pembungaan, pH 5.5-7.5.",
                "care_tips": "Pangkas cabang air, berikan paclobutrazol untuk memacu bunga di luar musim."
            },
            "Grapes": {
                "description": "Anggur, tanaman merambat.",
                "optimal_conditions": "Iklim kering saat pematangan, Suhu hangat, pH 6.5-7.5.",
                "care_tips": "Sangat butuh pemangkasan dan penjarangan buah."
            },
            "Watermelon": {
                "description": "Semangka, tanaman merambat semusim.",
                "optimal_conditions": "Suhu panas 25-30°C, Tanah berpasir, pH 6.0-7.0.",
                "care_tips": "Kurangi penyiraman menjelang panen untuk meningkatkan kemanisan."
            },
            "Muskmelon": {
                "description": "Melon, buah segar beraroma wangi.",
                "optimal_conditions": "Suhu 25-30°C, Kelembaban rendah, pH 6.0-7.0.",
                "care_tips": "Hindari air hujan langsung pada buah (gunakan mulsa/greenhouse)."
            },
            "Apple": {
                "description": "Apel, tanaman buah subtropis.",
                "optimal_conditions": "Suhu sejuk, Butuh chilling hours, pH 6.0-7.0.",
                "care_tips": "Hanya cocok di dataran tinggi (Batu, Malang) di Indonesia."
            },
            "Orange": {
                "description": "Jeruk, kaya vitamin C.",
                "optimal_conditions": "Suhu 13-35°C, Sinar matahari penuh, pH 6.0-7.0.",
                "care_tips": "Waspadai penyakit CVPD, lakukan pemupukan berimbang."
            },
            "Papaya": {
                "description": "Pepaya, buah sepanjang tahun.",
                "optimal_conditions": "Suhu 21-33°C, Tanah gembur drainase baik, pH 6.0-7.0.",
                "care_tips": "Sangat rentan busuk akar jika tergenang air."
            },
            "Coconut": {
                "description": "Kelapa, pohon kehidupan.",
                "optimal_conditions": "Suhu 27°C, Curah hujan tinggi, pH 5.5-7.0.",
                "care_tips": "Berikan garam (NaCl) dan pupuk KCL untuk produksi optimal."
            },
            "Cotton": {
                "description": "Kapas, tanaman serat.",
                "optimal_conditions": "Suhu panas, Musim kering panjang saat panen, pH 6.0-8.0.",
                "care_tips": "Pengendalian hama (bollworm) sangat krusial."
            },
            "Jute": {
                "description": "Yute, serat emas.",
                "optimal_conditions": "Suhu 24-37°C, Kelembaban tinggi, pH 6.0-7.0.",
                "care_tips": "Butuh air rendaman untuk proses pembusukan batang (retting)."
            },
            "Coffee": {
                "description": "Kopi, tanaman perkebunan bernilai tinggi.",
                "optimal_conditions": "Suhu 18-24°C (Arabika), Naungan cukup, pH 5.0-6.0.",
                "care_tips": "Pangkas lepas panen, jaga naungan, dan pemupukan organik."
            }
        }
        
        details = crop_details.get(crop_name, {
            "description": f"Tanaman {crop_name} direkomendasikan berdasarkan kondisi tanah Anda.",
            "optimal_conditions": "Sesuaikan dengan standar budidaya tanaman ini.",
            "care_tips": "Lakukan pemupukan dan pengairan sesuai SOP."
        })
        
        return {
            "crop": crop_name,
            "confidence": confidence,
            "details": details
        }

    @staticmethod
    def predict_yield(data: Dict[str, Any]) -> float:
        """Predict crop yield based on environmental factors."""
        yield_model = ModelLoader.get_model('yield_prediction')
        if yield_model is None:
            logger.warning("⚠️ Yield prediction model not available, using fallback")
            n = float(data.get('nitrogen', 0))
            p = float(data.get('phosphorus', 0))
            k = float(data.get('potassium', 0))
            estimated_yield = (n * 0.03 + p * 0.05 + k * 0.02) / 10
            return max(1.0, min(10.0, round(estimated_yield, 2)))
        
        input_data = prepare_fao_features(data)
        prediction = yield_model.predict(input_data)[0]
        return round(float(prediction) / 1000, 2) # kg/ha to ton/ha

    @staticmethod
    def predict_yield_advanced(data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict yield with explainable AI (SHAP values)."""
        advanced_model = ModelLoader.get_model('advanced_yield')
        explainer = ModelLoader.get_model('shap_explainer')
        
        feature_names = ['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp', 'Item_encoded', 'Year']
        features = [
            float(data.get('rainfall', 1500)),
            10.0,
            float(data.get('temperature', 27.0)),
            1.0,
            2026.0
        ]
        
        if advanced_model is None or explainer is None:
            logger.warning("⚠️ Advanced yield model not available, using fallback with insights")
            n, p, k, temp, rain, ph = float(data.get('nitrogen', 0)), float(data.get('phosphorus', 0)), float(data.get('potassium', 0)), float(data.get('temperature', 0)), float(data.get('rainfall', 0)), float(data.get('ph', 0))
            estimated_yield = (n * 0.025 + p * 0.045 + k * 0.015)
            
            if temp < 20 or temp > 35: estimated_yield *= 0.8
            if rain < 100 or rain > 300: estimated_yield *= 0.9
            if ph < 5.5 or ph > 7.5: estimated_yield *= 0.85
            
            estimated_yield = max(1.0, min(12.0, round(estimated_yield / 10, 2)))
            
            importances = [0.35, 0.25, 0.15, 0.10, 0.10, 0.05]
            legacy_feature_names = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Rainfall', 'pH']
            feature_importance_dict = sorted(zip(legacy_feature_names, importances), key=lambda x: x[1], reverse=True)
            
            shap_dict = {
                'Nitrogen': 0.5 if n > 80 else -0.2,
                'Phosphorus': 0.4 if p > 40 else -0.1,
                'Potassium': 0.2 if k > 40 else -0.1,
                'Temperature': 0.3 if 25 <= temp <= 30 else -0.3,
                'Rainfall': 0.2 if 150 <= rain <= 250 else -0.2,
                'pH': 0.1 if 6.0 <= ph <= 7.0 else -0.2
            }
            
            return {
                'predicted_yield_ton_ha': estimated_yield,
                'feature_importances': feature_importance_dict,
                'shap_values': shap_dict,
                'base_value': 4.5
            }

        input_data = pd.DataFrame([features], columns=feature_names)
        
        prediction = advanced_model.predict(input_data)[0]
        importances = advanced_model.feature_importances_
        feature_importance_dict = sorted(zip(feature_names, [float(i) for i in importances]), key=lambda x: x[1], reverse=True)
        shap_values = explainer.shap_values(input_data)
        shap_dict = {name: round(float(val), 2) for name, val in zip(feature_names, shap_values[0])}
        
        return {
            'predicted_yield_ton_ha': round(float(prediction) / 1000, 2),
            'feature_importances': feature_importance_dict,
            'shap_values': shap_dict,
            'base_value': round(float(explainer.expected_value) / 1000, 2)
        }

    @staticmethod
    def calculate_fertilizer_bags(nutrient_needed: str, nutrient_amount_kg: float, fertilizer_type: str) -> Optional[Dict[str, Any]]:
        """Calculate fertilizer bags needed for nutrient requirement."""
        fert_data = FERTILIZER_DATA.get(fertilizer_type)
        if not fert_data:
            return None
            
        nutrient_percentage = fert_data["content"].get(nutrient_needed, 0)
        if nutrient_percentage == 0:
            return None
            
        required_fertilizer_kg = nutrient_amount_kg / nutrient_percentage
        return {
            'required_kg': round(required_fertilizer_kg, 2),
            'fertilizer_name': fert_data["name"],
            'nutrient_needed': nutrient_needed,
            'nutrient_amount_kg': nutrient_amount_kg
        }

    @staticmethod
    def generate_yield_plan(commodity: Optional[str] = None, target_yield_ton_ha: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """Generate plan to achieve target yield."""
        if target_yield_ton_ha is None:
            raise ValueError("target_yield_ton_ha is required")
        
        if commodity and commodity != "umum":
            commodity_data = YieldBenchmarks.get_commodity_data().get(commodity.lower())
            if commodity_data:
                return MLService._generate_commodity_specific_plan(commodity.lower(), target_yield_ton_ha, commodity_data)
        
        # Fallback to EDA dataset
        dataset_path = get_dataset_path('EDA_500.csv')
        if not os.path.exists(dataset_path):
            logger.warning(f"Dataset {dataset_path} not found. Returning simplified fallback plan.")
            return {
                "commodity_name": "Umum (Fallback)",
                "target_yield": target_yield_ton_ha,
                "feasibility": "unknown",
                "npk_requirements": {
                    "Nitrogen (kg/ha)": round(target_yield_ton_ha * 20, 2),
                    "Phosphorus (kg/ha)": round(target_yield_ton_ha * 15, 2),
                    "Potassium (kg/ha)": round(target_yield_ton_ha * 15, 2)
                },
                "environmental_conditions": {
                    "Temperature (°C)": 25.0,
                    "Rainfall (mm)": 1500.0,
                    "pH Tanah": 6.5
                },
                "actual_yield_from_data": "N/A"
            }
        
        df = pd.read_csv(dataset_path)
        df['Yield'] = pd.to_numeric(df['Yield'], errors='coerce')
        df.dropna(subset=['Yield'], inplace=True)
        
        target_yield_kg = float(target_yield_ton_ha) * 1000
        best_match_row = df.iloc[(df['Yield'] - target_yield_kg).abs().argsort()[:1]]
        
        if best_match_row.empty:
            return None

        result = best_match_row.iloc[0]
        plan = {
            "commodity_name": "Umum",
            "target_yield": target_yield_ton_ha,
            "feasibility": "unknown",
            "npk_requirements": {
                "Nitrogen (kg/ha)": round(float(result['Nitrogen']), 2),
                "Phosphorus (kg/ha)": round(float(result['Phosphorus']), 2),
                "Potassium (kg/ha)": round(float(result['Potassium']), 2)
            },
            "environmental_conditions": {
                "Temperature (°C)": round(float(result['Temperature']), 2),
                "Rainfall (mm)": round(float(result['Rainfall']), 2),
                "pH Tanah": round(float(result['pH']), 2)
            },
            "actual_yield_from_data": f"{round(float(result['Yield'])/1000, 2)} ton/ha"
        }
        return plan

    @staticmethod
    def _generate_commodity_specific_plan(commodity, target_yield, commodity_data):
        """Generate detailed commodity-specific yield plan."""
        yield_category = YieldBenchmarks.get_yield_category(commodity, target_yield)
        benchmarks = commodity_data["benchmarks"]
        
        if yield_category == "very_low":
            feasibility = "Sangat Rendah - Target di bawah standar"
            feasibility_color = "red"
        elif yield_category == "low":
            feasibility = "Rendah - Dapat dicapai dengan input minimal"
            feasibility_color = "orange"
        elif yield_category == "average":
            feasibility = "Realistis - Target standar petani"
            feasibility_color = "green"
        elif yield_category == "high":
            feasibility = "Tinggi - Memerlukan manajemen intensif"
            feasibility_color = "blue"
        else:
            feasibility = "Sangat Tinggi - Target ambisius, perlu teknologi canggih"
            feasibility_color = "purple"
        
        npk = YieldBenchmarks.get_npk_for_yield(commodity, target_yield)
        varieties = YieldBenchmarks.get_variety_recommendations(commodity, target_yield)
        fertilizers = MLService._convert_npk_to_fertilizers(npk['N'], npk['P'], npk['K'])
        costs = MLService._calculate_input_costs(fertilizers, commodity, target_yield)
        timeline = MLService._generate_cultivation_timeline(commodity, commodity_data['growth_duration'])
        
        return {
            "commodity_name": commodity_data["name"],
            "commodity_icon": commodity_data["icon"],
            "target_yield": target_yield,
            "yield_unit": commodity_data["unit"],
            "feasibility": {
                "status": feasibility,
                "color": feasibility_color,
                "category": yield_category,
                "benchmark_range": {
                    "low": f"{benchmarks['low']['min']}-{benchmarks['low']['max']} {commodity_data['unit']}",
                    "average": f"{benchmarks['average']['min']}-{benchmarks['average']['max']} {commodity_data['unit']}",
                    "high": f"{benchmarks['high']['min']}-{benchmarks['high']['max']} {commodity_data['unit']}",
                    "record": f"{benchmarks['record']['min']}-{benchmarks['record']['max']} {commodity_data['unit']}"
                }
            },
            "npk_requirements": {
                "Nitrogen (N)": f"{npk['N']} kg/ha",
                "Phosphorus (P)": f"{npk['P']} kg/ha",
                "Potassium (K)": f"{npk['K']} kg/ha"
            },
            "fertilizer_products": fertilizers,
            "environmental_conditions": {
                "Suhu Optimal": f"{commodity_data['optimal_conditions']['temperature']['min']}-{commodity_data['optimal_conditions']['temperature']['max']} °C",
                "Curah Hujan": f"{commodity_data['optimal_conditions']['rainfall']['min']}-{commodity_data['optimal_conditions']['rainfall']['max']} {commodity_data['optimal_conditions']['rainfall']['unit']}",
                "pH Tanah": f"{commodity_data['optimal_conditions']['ph']['min']}-{commodity_data['optimal_conditions']['ph']['max']}",
                "Ketinggian": f"{commodity_data['optimal_conditions']['altitude']['min']}-{commodity_data['optimal_conditions']['altitude']['max']} {commodity_data['optimal_conditions']['altitude']['unit']}"
            },
            "recommended_varieties": varieties,
            "critical_factors": commodity_data["critical_factors"],
            "cost_estimate": costs,
            "cultivation_timeline": timeline,
            "growth_duration": f"{commodity_data['growth_duration']} hari"
        }

    @staticmethod
    def _convert_npk_to_fertilizers(n_kg, p_kg, k_kg):
        fertilizers = {}
        if n_kg > 0:
            fertilizers["Urea (46% N)"] = f"{round(n_kg / 0.46, 2)} kg/ha"
        if p_kg > 0:
            fertilizers["SP-36 (36% P2O5)"] = f"{round(p_kg / 0.158, 2)} kg/ha"
        if k_kg > 0:
            fertilizers["KCl (60% K2O)"] = f"{round(k_kg / 0.50, 2)} kg/ha"
        fertilizers["Pupuk Kandang/Kompos"] = "2-5 ton/ha (aplikasi dasar)"
        return fertilizers

    @staticmethod
    def _calculate_input_costs(fertilizers, commodity, target_yield):
        prices = {"Urea": 2500, "SP-36": 3000, "KCl": 4500, "Pupuk Kandang": 500}
        total_fertilizer_cost = 0
        breakdown = {}
        
        for fert_name, amount_str in fertilizers.items():
            if "Pupuk Kandang" in fert_name or "Kompos" in fert_name:
                cost = 3.5 * 1000 * prices["Pupuk Kandang"]
                breakdown[fert_name] = f"Rp {cost:,.0f}"
                total_fertilizer_cost += cost
            else:
                try:
                    kg = float(amount_str.split()[0])
                    fert_type = fert_name.split()[0]
                    if fert_type in prices:
                        cost = kg * prices[fert_type]
                        breakdown[fert_name] = f"Rp {cost:,.0f}"
                        total_fertilizer_cost += cost
                except:
                    pass
        
        seed_costs = {"padi": 100000, "jagung": 500000, "kedelai": 200000, "cabai": 2000000, "tomat": 1500000}
        seed_cost = seed_costs.get(commodity, 300000)
        labor_cost = 3000000
        pesticide_cost = 1500000
        total_cost = total_fertilizer_cost + seed_cost + labor_cost + pesticide_cost
        
        price_per_ton = {"padi": 5000000, "jagung": 4000000, "kedelai": 8000000, "cabai": 15000000, "tomat": 8000000}
        commodity_price = price_per_ton.get(commodity, 5000000)
        estimated_revenue = target_yield * commodity_price
        
        return {
            "fertilizer_breakdown": breakdown,
            "total_fertilizer": f"Rp {total_fertilizer_cost:,.0f}",
            "seed_cost": f"Rp {seed_cost:,.0f}",
            "labor_cost": f"Rp {labor_cost:,.0f}",
            "pesticide_cost": f"Rp {pesticide_cost:,.0f}",
            "total_input_cost": f"Rp {total_cost:,.0f}",
            "estimated_revenue": f"Rp {estimated_revenue:,.0f}",
            "estimated_profit": f"Rp {estimated_revenue - total_cost:,.0f}",
            "note": "Estimasi kasar, sesuaikan dengan harga lokal"
        }

    @staticmethod
    def _generate_cultivation_timeline(commodity, growth_duration):
        return [
            {
                "phase": "Persiapan Lahan",
                "weeks": "2 minggu sebelum tanam",
                "activities": ["Pembajakan dan penggemburan tanah", "Aplikasi pupuk kandang/kompos", "Pengapuran jika pH rendah"]
            },
            {
                "phase": "Penanaman",
                "weeks": "Minggu 0",
                "activities": ["Penanaman benih/bibit berkualitas", "Aplikasi pupuk dasar (P dan K)", "Penyiraman awal"]
            },
            {
                "phase": "Vegetatif Awal",
                "weeks": "Minggu 1-3",
                "activities": ["Penyulaman tanaman mati", "Penyiangan gulma", "Aplikasi pupuk N pertama", "Monitoring hama/penyakit"]
            },
            {
                "phase": "Vegetatif Lanjut",
                "weeks": f"Minggu 4-{growth_duration//14}",
                "activities": ["Aplikasi pupuk N susulan", "Pengendalian hama/penyakit", "Pengairan teratur"]
            },
            {
                "phase": "Generatif",
                "weeks": f"Minggu {growth_duration//14 + 1}-{growth_duration//7}",
                "activities": ["Aplikasi pupuk K tinggi", "Pengurangan N", "Monitoring pembungaan/pembuahan"]
            },
            {
                "phase": "Pematangan & Panen",
                "weeks": f"Minggu {growth_duration//7 + 1}-{growth_duration//7 + 2}",
                "activities": ["Pengurangan pengairan", "Monitoring kematangan", "Persiapan alat panen", "Panen tepat waktu"]
            }
        ]

    @staticmethod
    def predict_success(data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict farming success probability."""
        success_model = ModelLoader.get_model('success')
        if success_model is None:
            logger.warning("⚠️ Success prediction model not available, using fallback")
            ph = float(data.get('ph', 7.0))
            rainfall = float(data.get('rainfall', 0))
            temp = float(data.get('temperature', 25))
            
            score = 0
            if 6.0 <= ph <= 7.5: score += 30
            if 500 <= rainfall <= 1500: score += 30
            if 20 <= temp <= 30: score += 40
            
            status = "Berhasil" if score >= 60 else "Berisiko Tinggi"
            return {'status': status, 'probability_of_success': score}
        
        input_data = prepare_fao_features(data)
        prediction = success_model.predict(input_data)[0]
        probability = success_model.predict_proba(input_data)[0]
        
        status = "Berhasil" if prediction == 1 else "Berisiko Tinggi"
        prob_percent = round(probability[1] * 100, 2)
        
        return {
            'status': status,
            'probability_of_success': prob_percent
        }
