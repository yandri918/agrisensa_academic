"""Yield benchmarks and cultivation data for major commodities, independent of Flask."""

class YieldBenchmarks:
    """Database of yield benchmarks and cultivation requirements for major crops."""
    
    @staticmethod
    def get_commodity_data():
        """Get comprehensive yield and cultivation data for all commodities."""
        return {
            "padi": {
                "name": "Padi",
                "icon": "🌾",
                "unit": "ton/ha",
                "benchmarks": {
                    "low": {"min": 3.0, "max": 4.0, "label": "Rendah"},
                    "average": {"min": 4.5, "max": 6.0, "label": "Rata-rata"},
                    "high": {"min": 7.0, "max": 8.5, "label": "Tinggi"},
                    "record": {"min": 9.0, "max": 12.0, "label": "Rekor"}
                },
                "optimal_conditions": {
                    "temperature": {"min": 22, "max": 32, "unit": "°C"},
                    "rainfall": {"min": 1500, "max": 2000, "unit": "mm/tahun"},
                    "ph": {"min": 5.5, "max": 7.0},
                    "altitude": {"min": 0, "max": 1500, "unit": "mdpl"}
                },
                "npk_ratios": {
                    "low": {"N": 90, "P": 60, "K": 60},
                    "average": {"N": 120, "P": 75, "K": 75},
                    "high": {"N": 150, "P": 90, "K": 90},
                    "record": {"N": 180, "P": 110, "K": 110}
                },
                "varieties": {
                    "low": ["IR64", "Ciherang"],
                    "average": ["Inpari 32", "Mekongga"],
                    "high": ["Inpari 42", "Inpari 43"],
                    "record": ["Inpari 48", "Hybrid (Hipa 18)"]
                },
                "growth_duration": 110,  # days
                "critical_factors": [
                    "Pengairan teratur sangat penting",
                    "Pengendalian hama penggerek batang",
                    "Pemupukan berimbang sesuai fase",
                    "Varietas unggul bersertifikat"
                ]
            },
            "jagung": {
                "name": "Jagung",
                "icon": "🌽",
                "unit": "ton/ha",
                "benchmarks": {
                    "low": {"min": 3.0, "max": 4.5, "label": "Rendah"},
                    "average": {"min": 5.0, "max": 7.0, "label": "Rata-rata"},
                    "high": {"min": 8.0, "max": 10.0, "label": "Tinggi"},
                    "record": {"min": 11.0, "max": 14.0, "label": "Rekor"}
                },
                "optimal_conditions": {
                    "temperature": {"min": 21, "max": 34, "unit": "°C"},
                    "rainfall": {"min": 400, "max": 800, "unit": "mm/musim"},
                    "ph": {"min": 5.5, "max": 7.5},
                    "altitude": {"min": 0, "max": 1800, "unit": "mdpl"}
                },
                "npk_ratios": {
                    "low": {"N": 100, "P": 75, "K": 50},
                    "average": {"N": 150, "P": 100, "K": 75},
                    "high": {"N": 200, "P": 125, "K": 100},
                    "record": {"N": 250, "P": 150, "K": 125}
                },
                "varieties": {
                    "low": ["Lokal", "Bisma"],
                    "average": ["Bisi 18", "Pioneer 21"],
                    "high": ["NK 212", "Bisi 222"],
                    "record": ["Hybrid Premium", "DK 979"]
                },
                "growth_duration": 100,  # days
                "critical_factors": [
                    "Drainase baik untuk mencegah genangan",
                    "Pemupukan N tinggi saat vegetatif",
                    "Pengendalian ulat grayak",
                    "Benih hybrid bersertifikat"
                ]
            },
            "kedelai": {
                "name": "Kedelai",
                "icon": "🫘",
                "unit": "ton/ha",
                "benchmarks": {
                    "low": {"min": 1.0, "max": 1.3, "label": "Rendah"},
                    "average": {"min": 1.5, "max": 2.0, "label": "Rata-rata"},
                    "high": {"min": 2.3, "max": 2.8, "label": "Tinggi"},
                    "record": {"min": 3.0, "max": 3.8, "label": "Rekor"}
                },
                "optimal_conditions": {
                    "temperature": {"min": 23, "max": 30, "unit": "°C"},
                    "rainfall": {"min": 300, "max": 400, "unit": "mm/musim"},
                    "ph": {"min": 6.0, "max": 7.0},
                    "altitude": {"min": 0, "max": 900, "unit": "mdpl"}
                },
                "npk_ratios": {
                    "low": {"N": 25, "P": 75, "K": 50},
                    "average": {"N": 30, "P": 100, "K": 75},
                    "high": {"N": 40, "P": 125, "K": 90},
                    "record": {"N": 50, "P": 150, "K": 110}
                },
                "varieties": {
                    "low": ["Lokal", "Wilis"],
                    "average": ["Grobogan", "Anjasmoro"],
                    "high": ["Dena 1", "Dega 1"],
                    "record": ["Demas 1", "Hybrid"]
                },
                "growth_duration": 80,  # days
                "critical_factors": [
                    "Inokulasi rhizobium untuk fiksasi N",
                    "Drainase sempurna",
                    "Pengendalian lalat kacang",
                    "Pemupukan P dan K lebih tinggi dari N"
                ]
            },
            "cabai": {
                "name": "Cabai",
                "icon": "🌶️",
                "unit": "ton/ha",
                "benchmarks": {
                    "low": {"min": 10, "max": 15, "label": "Rendah"},
                    "average": {"min": 18, "max": 22, "label": "Rata-rata"},
                    "high": {"min": 25, "max": 30, "label": "Tinggi"},
                    "record": {"min": 32, "max": 40, "label": "Rekor"}
                },
                "optimal_conditions": {
                    "temperature": {"min": 24, "max": 28, "unit": "°C"},
                    "rainfall": {"min": 600, "max": 1200, "unit": "mm/tahun"},
                    "ph": {"min": 6.0, "max": 7.0},
                    "altitude": {"min": 200, "max": 1200, "unit": "mdpl"}
                },
                "npk_ratios": {
                    "low": {"N": 120, "P": 150, "K": 150},
                    "average": {"N": 180, "P": 200, "K": 200},
                    "high": {"N": 250, "P": 250, "K": 250},
                    "record": {"N": 300, "P": 300, "K": 300}
                },
                "varieties": {
                    "low": ["Lokal", "Keriting"],
                    "average": ["Lado", "PM 999"],
                    "high": ["Laris", "Gada"],
                    "record": ["Tanjung 2", "Hot Beauty"]
                },
                "growth_duration": 90,  # days to first harvest, continues for months
                "critical_factors": [
                    "Mulsa plastik untuk kontrol gulma dan kelembaban",
                    "Pemupukan intensif setiap minggu",
                    "Pengendalian thrips dan antraknosa",
                    "Sistem drip irrigation ideal"
                ]
            },
            "tomat": {
                "name": "Tomat",
                "icon": "🍅",
                "unit": "ton/ha",
                "benchmarks": {
                    "low": {"min": 15, "max": 20, "label": "Rendah"},
                    "average": {"min": 25, "max": 35, "label": "Rata-rata"},
                    "high": {"min": 40, "max": 50, "label": "Tinggi"},
                    "record": {"min": 55, "max": 70, "label": "Rekor"}
                },
                "optimal_conditions": {
                    "temperature": {"min": 20, "max": 27, "unit": "°C"},
                    "rainfall": {"min": 750, "max": 1250, "unit": "mm/tahun"},
                    "ph": {"min": 6.0, "max": 6.8},
                    "altitude": {"min": 300, "max": 1500, "unit": "mdpl"}
                },
                "npk_ratios": {
                    "low": {"N": 100, "P": 150, "K": 150},
                    "average": {"N": 150, "P": 200, "K": 200},
                    "high": {"N": 200, "P": 250, "K": 250},
                    "record": {"N": 250, "P": 300, "K": 300}
                },
                "varieties": {
                    "low": ["Lokal", "Permata"],
                    "average": ["Servo", "Tymoti"],
                    "high": ["Fortuna", "Intan"],
                    "record": ["Hybrid F1", "Betavila"]
                },
                "growth_duration": 70,  # days to first harvest
                "critical_factors": [
                    "Bedengan tinggi dengan mulsa",
                    "Pemangkasan dan pewiwilan rutin",
                    "Pengendalian layu fusarium",
                    "Kalsium cukup untuk mencegah blossom end rot"
                ]
            }
        }
    
    @staticmethod
    def get_yield_category(commodity, target_yield):
        """Determine yield category for given target."""
        data = YieldBenchmarks.get_commodity_data().get(commodity)
        if not data:
            return "unknown"
        
        benchmarks = data["benchmarks"]
        
        if target_yield < benchmarks["low"]["min"]:
            return "very_low"
        elif benchmarks["low"]["min"] <= target_yield <= benchmarks["low"]["max"]:
            return "low"
        elif benchmarks["average"]["min"] <= target_yield <= benchmarks["average"]["max"]:
            return "average"
        elif benchmarks["high"]["min"] <= target_yield <= benchmarks["high"]["max"]:
            return "high"
        elif target_yield >= benchmarks["record"]["min"]:
            return "record"
        else:
            # Between categories
            if target_yield < benchmarks["average"]["min"]:
                return "low"
            elif target_yield < benchmarks["high"]["min"]:
                return "average"
            else:
                return "high"
    
    @staticmethod
    def get_npk_for_yield(commodity, target_yield):
        """Get recommended NPK based on target yield category."""
        data = YieldBenchmarks.get_commodity_data().get(commodity)
        if not data:
            return None
        
        category = YieldBenchmarks.get_yield_category(commodity, target_yield)
        
        # Map category to NPK ratio key
        if category in ["very_low", "low"]:
            npk_key = "low"
        elif category == "average":
            npk_key = "average"
        elif category == "high":
            npk_key = "high"
        else:  # record
            npk_key = "record"
        
        return data["npk_ratios"].get(npk_key, data["npk_ratios"]["average"])
    
    @staticmethod
    def get_variety_recommendations(commodity, target_yield):
        """Get recommended varieties for target yield."""
        data = YieldBenchmarks.get_commodity_data().get(commodity)
        if not data:
            return []
        
        category = YieldBenchmarks.get_yield_category(commodity, target_yield)
        
        # Map category to variety key
        if category in ["very_low", "low"]:
            variety_key = "low"
        elif category == "average":
            variety_key = "average"
        elif category == "high":
            variety_key = "high"
        else:  # record
            variety_key = "record"
        
        return data["varieties"].get(variety_key, data["varieties"]["average"])
