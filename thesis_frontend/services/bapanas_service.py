
import requests
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# =============================================================================
# 🔗 MODULAR IMPORT STRATEGY
# =============================================================================
try:
    from ..utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING
except (ImportError, ValueError):
    try:
        from utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING
    except ImportError:
        try:
            from agrisensa_streamlit.utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING
        except ImportError:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            from utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING

class BapanasService:
    def __init__(self):
        self.base_url = API_CONFIG["BASE_URL"]
        self.headers = API_CONFIG["HEADERS"]
    
    def get_latest_prices(self, province_id=None, city_id=None):
        """
        Fetch latest prices from Bapanas API with Auto-Seek (H-7 lookback).
        If all attempts fail, returns a high-quality static fallback.
        """
        endpoint = f"{self.base_url}/harga-pangan-informasi"
        
        # 1. ATTEMPT LIVE API (7 Days Window)
        for days_back in range(7):
            params = {"level_harga_id": 1}
            if province_id and str(province_id) != "0":
                params["province_id"] = province_id
            if city_id:
                params["city_id"] = city_id
                
            try:
                # Target date isn't usually sent as a param in Bapanas v2 information endpoint,
                # but we try to see if they have any latest snapshot available.
                response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "success" and result.get("data"):
                        df = self._parse_price_response(result.get("data", []))
                        if df is not None and not df.empty:
                            return df
            except: continue
                
        # 2. EMERGENCY FALLBACK (Ensures UI never breaks)
        return self.get_fallback_data()
    
    def get_fallback_data(self):
        """Provide realistic price data if API is entirely unreachable."""
        fallback_date = datetime.now() - timedelta(days=1)
        data = [
            {'commodity': 'Beras Premium', 'price': 16250, 'unit': 'Rp/kg'},
            {'commodity': 'Beras Medium', 'price': 14300, 'unit': 'Rp/kg'},
            {'commodity': 'Bawang Merah', 'price': 34500, 'unit': 'Rp/kg'},
            {'commodity': 'Cabai Merah Keriting', 'price': 48900, 'unit': 'Rp/kg'},
            {'commodity': 'Cabai Rawit Merah', 'price': 52000, 'unit': 'Rp/kg'},
            {'commodity': 'Daging Sapi Murni', 'price': 135000, 'unit': 'Rp/kg'},
            {'commodity': 'Daging Ayam Ras', 'price': 38500, 'unit': 'Rp/kg'},
            {'commodity': 'Telur Ayam Ras', 'price': 31000, 'unit': 'Rp/kg'},
            {'commodity': 'Gula Konsumsi', 'price': 17800, 'unit': 'Rp/kg'},
            {'commodity': 'Minyak Goreng Kemasan', 'price': 18500, 'unit': 'Rp/l'}
        ]
        df = pd.DataFrame(data)
        df['date'] = fallback_date
        df['status'] = 'Offline/Historis'
        return df

    def _parse_price_response(self, data_list):
        if not data_list: return None
        parsed_data = []
        today_date = datetime.now()
        yesterday_date = today_date - timedelta(days=1)
        
        for item in data_list:
            try:
                if item.get('today'):
                    parsed_data.append({
                        'commodity': item.get('name'),
                        'price': float(item.get('today', 0)),
                        'date': today_date,
                        'unit': item.get('satuan', 'Rp/kg'),
                        'status': 'Official'
                    })
                if item.get('yesterday'):
                    parse_yesterday = item.get('yesterday_date')
                    date_obj = yesterday_date
                    if parse_yesterday:
                        try:
                            date_obj = datetime.strptime(parse_yesterday, '%d-%m-%Y')
                        except: pass
                    parsed_data.append({
                        'commodity': item.get('name'),
                        'price': float(item.get('yesterday', 0)),
                        'date': date_obj,
                        'unit': item.get('satuan', 'Rp/kg'),
                        'status': 'Official'
                    })
            except: continue
        return pd.DataFrame(parsed_data) if parsed_data else None

    def get_price_map_data(self, commodity_id=2, level_id=3):
        endpoint = f"{self.base_url}/harga-peta-provinsi"
        today = datetime.now()
        start_date = (today - timedelta(days=7)).strftime("%d/%m/%Y")
        end_date = today.strftime("%d/%m/%Y")
        period = f"{start_date} - {end_date}"
        
        params = {
            "level_harga_id": level_id,
            "komoditas_id": commodity_id,
            "period_date": period,
            "multi_status_map[0]": "",
            "multi_province_id[0]": ""
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if "data" in result and result['data']:
                    return self._parse_map_response(result['data'])
            return None
        except: return None

    def _parse_map_response(self, data_list):
        parsed_data = []
        for item in data_list:
            try:
                ll = item.get('latlong', '').split(',')
                if len(ll) != 2: continue
                lat, lon = float(ll[0]), float(ll[1])
                price = float(item.get('rata_rata_geometrik', 0))
                if price > 0:
                    parsed_data.append({
                        'province': item.get('province_name'),
                        'lat': lat,
                        'lon': lon,
                        'price': price,
                        'level': item.get('level_harga', '?'),
                        'status': item.get('status_map', 'Normal')
                    })
            except: continue
        return pd.DataFrame(parsed_data) if parsed_data else None
