import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Configuration
provinces = ['Banten', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'DI Yogyakarta', 'Jawa Timur']
commodities = {
    'Cabai': {'base_price': 40000, 'volatility': 5000, 'trend': 2.0},
    'Padi': {'base_price': 6000, 'volatility': 500, 'trend': 0.5},
    'Jagung': {'base_price': 5000, 'volatility': 400, 'trend': 0.5},
    'Bawang Merah': {'base_price': 30000, 'volatility': 3000, 'trend': 1.5},
    'Tomat': {'base_price': 15000, 'volatility': 2000, 'trend': 1.0},
}

# Generate dates for 3 years
dates = pd.date_range(start='2021-01-01', end='2023-12-31', freq='D')
n_days = len(dates)

data = []

for prov in provinces:
    # Add some regional price difference (DKI Jakarta usually more expensive)
    regional_multiplier = 1.1 if prov == 'DKI Jakarta' else (1.05 if prov in ['Banten', 'Jawa Barat'] else 1.0)
    
    for comm, params in commodities.items():
        base = params['base_price'] * regional_multiplier
        vol = params['volatility']
        
        # Create a time series with trend, seasonality, and noise
        time_steps = np.arange(n_days)
        
        # Upward trend over time
        trend = time_steps * params['trend']
        
        # Yearly seasonality (e.g. prices peak/drop at certain months)
        seasonality = np.sin(2 * np.pi * time_steps / 365.25) * vol * 1.5
        
        # Random walk noise (autoregressive)
        noise = np.random.normal(0, vol * 0.1, n_days)
        noise = np.cumsum(noise) # Random walk
        # Mean revert the noise a bit to keep it bounded
        noise = noise - (noise * 0.05) 
        
        # Final price simulation
        prices = base + trend + seasonality + noise
        
        # Ensure prices don't drop below a minimum threshold
        prices = np.maximum(prices, base * 0.5)
        
        df_temp = pd.DataFrame({
            'tanggal': dates,
            'provinsi': prov,
            'komoditas': comm,
            'harga': prices.round(0) # Round to nearest Rupiah
        })
        
        data.append(df_temp)

# Combine all data
df_final = pd.concat(data, ignore_index=True)

# Ensure data directory exists
os.makedirs('data/raw', exist_ok=True)
output_path = 'data/raw/synthetic_crop_prices_java.csv'

# Save to CSV
df_final.to_csv(output_path, index=False)
print(f"Dataset berhasil dibuat: {output_path}")
print(f"Total baris: {len(df_final)}")
print(df_final.head())
