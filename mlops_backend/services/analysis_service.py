"""Analysis service for leaf and soil analysis, independent of Flask."""
import cv2
import numpy as np
import logging
from typing import Optional
from ml_models.model_loader import ModelLoader

logger = logging.getLogger("mlops_api.analysis_service")

class AnalysisService:
    """Service for analyzing leaf images and NPK values."""
    
    @staticmethod
    def analyze_leaf_image(image_data: bytes) -> Optional[dict]:
        """
        Analyze leaf image for BWD score.
        
        Args:
            image_data: Binary image data
            
        Returns:
            dict: Analysis results with score, hue, and confidence
        """
        try:
            bwd_model = ModelLoader.get_model('bwd')
            
            # Decode image
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                logger.error("Failed to decode image data")
                return None
            
            # Convert to HSV color space
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Create mask for green color (leaves)
            lower_green = np.array([30, 40, 40])
            upper_green = np.array([90, 255, 255])
            mask = cv2.inRange(hsv_image, lower_green, upper_green)
            
            # Check if any green pixels found
            if cv2.countNonZero(mask) == 0:
                logger.warning("No green pixels detected in image")
                return None
            
            # Calculate average hue value
            avg_hue = cv2.mean(hsv_image, mask=mask)[0]
            
            # --- Enhanced Analysis: Spot Detection (Brown & White) ---
            lower_brown = np.array([10, 100, 20])
            upper_brown = np.array([20, 255, 200])
            brown_mask = cv2.inRange(hsv_image, lower_brown, upper_brown)
            brown_pixels = cv2.countNonZero(brown_mask)
            
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 20, 255])
            white_mask = cv2.inRange(hsv_image, lower_white, upper_white)
            white_pixels = cv2.countNonZero(white_mask)
            
            total_pixels = cv2.countNonZero(mask)
            brown_ratio = (brown_pixels / total_pixels) * 100 if total_pixels > 0 else 0
            white_ratio = (white_pixels / total_pixels) * 100 if total_pixels > 0 else 0
            
            disease_analysis = {
                "brown_spots": f"{brown_ratio:.1f}%",
                "white_spots": f"{white_ratio:.1f}%",
                "condition": "Sehat",
                "details": "Tidak ditemukan bercak signifikan."
            }
            
            if brown_ratio > 5:
                disease_analysis["condition"] = "Terindikasi Brown Spot (Bercak Coklat)"
                disease_analysis["details"] = "Terdeteksi bercak coklat yang mungkin menandakan infeksi jamur (Helminthosporium oryzae) atau kekurangan nutrisi."
            elif white_ratio > 5:
                disease_analysis["condition"] = "Terindikasi White Spot / Hama"
                disease_analysis["details"] = "Terdeteksi bercak putih yang bisa menandakan serangan hama (seperti Hama Putih Palsu) atau defisiensi mikronutrien."
            
            # --- BWD Score Logic (Heuristic / Model) ---
            if bwd_model is None:
                logger.warning("⚠️ BWD model not available, using color-based heuristic")
                
                if avg_hue < 35:
                    predicted_score = 2
                    confidence = 75.0
                    bwd_status = "Kritis (Kuning)"
                    recommendation = "Tanaman sangat kekurangan Nitrogen. Segera aplikasikan pupuk Urea (Nitrogen) dengan dosis tinggi sesuai anjuran setempat."
                elif avg_hue < 45:
                    predicted_score = 3
                    confidence = 70.0
                    bwd_status = "Kurang (Hijau Muda)"
                    recommendation = "Tanaman kekurangan Nitrogen. Perlu penambahan pupuk Urea segera untuk memacu pertumbuhan."
                elif avg_hue < 60:
                    predicted_score = 4
                    confidence = 80.0
                    bwd_status = "Cukup (Hijau)"
                    recommendation = "Kadar Nitrogen cukup. Pertahankan pemupukan berimbang, pantau terus warna daun."
                else:
                    predicted_score = 5
                    confidence = 85.0
                    bwd_status = "Berlebih (Hijau Gelap)"
                    recommendation = "Kadar Nitrogen sangat tinggi/berlebih. Kurangi atau hentikan sementara pupuk Urea untuk mencegah serangan penyakit."
            else:
                input_data = np.array([[avg_hue]])
                predicted_score = bwd_model.predict(input_data)[0]
                
                if hasattr(bwd_model, 'predict_proba'):
                    confidence = np.max(bwd_model.predict_proba(input_data)) * 100
                else:
                    confidence = 80.0
                
                score_int = int(round(predicted_score))
                if score_int <= 2:
                    bwd_status = "Kritis (Kuning)"
                    recommendation = "Tanaman sangat kekurangan Nitrogen. Segera aplikasikan pupuk Urea."
                elif score_int == 3:
                    bwd_status = "Kurang (Hijau Muda)"
                    recommendation = "Tanaman kekurangan Nitrogen. Tambahkan pupuk Urea."
                elif score_int == 4:
                    bwd_status = "Cukup (Hijau)"
                    recommendation = "Kadar Nitrogen cukup. Lanjutkan pemeliharaan."
                else:
                    bwd_status = "Berlebih (Hijau Gelap)"
                    recommendation = "Kadar Nitrogen berlebih. Kurangi pupuk Urea."
            
            return {
                'bwd_score': int(predicted_score),
                'bwd_status': bwd_status,
                'avg_hue': round(avg_hue, 2),
                'confidence': round(confidence, 2),
                'disease_analysis': disease_analysis,
                'recommendation': recommendation
            }
            
        except Exception as e:
            logger.error(f"Error in leaf analysis: {e}")
            raise RuntimeError(f"Leaf analysis failed: {str(e)}")

    @staticmethod
    def analyze_npk_values(n_value: float, p_value: float, k_value: float) -> dict:
        """Analyze NPK values and provide recommendations."""
        analysis = {}
        
        # --- 1. Nitrogen (N) Analysis ---
        if n_value < 100:
            n_label = "Sangat Rendah"
            n_class = "danger"
            n_rec = "<strong>Kritis!</strong> Pertumbuhan vegetatif akan terhambat (kerdil). <br>👉 <strong>Saran:</strong> Tambahkan Urea 150-200 kg/ha atau Pupuk Kandang 5-10 ton/ha segera."
        elif 100 <= n_value < 150:
            n_label = "Rendah"
            n_class = "warning"
            n_rec = "<strong>Kurang.</strong> Daun mungkin hijau muda/kuning. <br>👉 <strong>Saran:</strong> Tambahkan Urea 100 kg/ha atau ZA untuk memacu pertumbuhan."
        elif 150 <= n_value <= 250:
            n_label = "Optimal"
            n_class = "success"
            n_rec = "<strong>Ideal.</strong> Suplai Nitrogen cukup untuk pertumbuhan daun dan batang yang sehat. Pertahankan."
        else:
            n_label = "Tinggi"
            n_class = "info"
            n_rec = "<strong>Berlebih.</strong> Tanaman terlalu sukulen (berair), rentan rebah dan serangan penyakit/hama. <br>👉 <strong>Saran:</strong> Hentikan pemupukan N sementara."
        
        analysis['Nitrogen (N)'] = {
            'value': n_value,
            'label': n_label,
            'class': n_class,
            'rekomendasi': n_rec
        }
        
        # --- 2. Phosphorus (P) Analysis ---
        if p_value < 15:
            p_label = "Sangat Rendah"
            p_class = "danger"
            p_rec = "<strong>Defisiensi Berat.</strong> Perakaran buruk, pembungaan terhambat. <br>👉 <strong>Saran:</strong> Berikan SP-36 100-150 kg/ha. Pertimbangkan pupuk hayati pelarut fosfat."
        elif 15 <= p_value < 25:
            p_label = "Rendah"
            p_class = "warning"
            p_rec = "<strong>Kurang.</strong> Daun tua mungkin keunguan. <br>👉 <strong>Saran:</strong> Tambahkan SP-36 50-75 kg/ha saat pengolahan tanah."
        elif 25 <= p_value <= 45:
            p_label = "Optimal"
            p_class = "success"
            p_rec = "<strong>Ideal.</strong> Cukup untuk menunjang pembungaan dan pengisian buah/biji."
        else:
            p_label = "Tinggi"
            p_class = "info"
            p_rec = "<strong>Sangat Tinggi.</strong> Fosfor berlebih dapat mengikat unsur mikro (Zn, Fe). <br>👉 <strong>Saran:</strong> Tidak perlu pupuk P tambahan untuk 1-2 musim."
        
        analysis['Fosfor (P)'] = {
            'value': p_value,
            'label': p_label,
            'class': p_class,
            'rekomendasi': p_rec
        }
        
        # --- 3. Potassium (K) Analysis ---
        if k_value < 100:
            k_label = "Sangat Rendah"
            k_class = "danger"
            k_rec = "<strong>Kritis!</strong> Buah kecil, rasa hambar, rentan kekeringan. <br>👉 <strong>Saran:</strong> Berikan KCL 100-150 kg/ha."
        elif 100 <= k_value < 180:
            k_label = "Rendah"
            k_class = "warning"
            k_rec = "<strong>Kurang.</strong> Tepi daun mungkin hangus (necrosis). <br>👉 <strong>Saran:</strong> Tambahkan KCL 50-75 kg/ha."
        elif 180 <= k_value <= 300:
            k_label = "Optimal"
            k_class = "success"
            k_rec = "<strong>Ideal.</strong> Kualitas buah dan ketahanan penyakit akan optimal."
        else:
            k_label = "Tinggi"
            k_class = "info"
            k_rec = "<strong>Berlebih.</strong> Antagonisme dengan Magnesium (Mg) dan Kalsium (Ca). <br>👉 <strong>Saran:</strong> Waspada gejala kekurangan Mg (daun tua kuning di antara tulang daun)."
        
        analysis['Kalium (K)'] = {
            'value': k_value,
            'label': k_label,
            'class': k_class,
            'rekomendasi': k_rec
        }

        # --- 4. Ratio Analysis ---
        ratio_rec = ""
        if k_value > 0:
            nk_ratio = n_value / k_value
            if nk_ratio > 2.0:
                ratio_rec = "⚠️ <strong>Rasio N:K Tinggi (>2.0):</strong> Dominasi Nitrogen. Tanaman rimbun tapi mungkin malas berbuah. Tingkatkan asupan Kalium."
            elif nk_ratio < 0.5:
                ratio_rec = "⚠️ <strong>Rasio N:K Rendah (<0.5):</strong> Dominasi Kalium. Pertumbuhan vegetatif mungkin melambat. Pastikan N cukup saat fase awal."
            else:
                ratio_rec = "✅ <strong>Keseimbangan Hara:</strong> Rasio N dan K seimbang untuk pertumbuhan dan pembuahan."
        
        analysis['Analisis Rasio'] = {
            'value': f"N:K = {round(n_value/k_value, 2) if k_value else 'N/A'}",
            'label': "Info",
            'class': "primary",
            'rekomendasi': ratio_rec
        }
        
        return analysis
