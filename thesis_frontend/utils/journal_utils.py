import pandas as pd
import os
from datetime import datetime

DATA_DIR = "data"
JOURNAL_FILE = os.path.join(DATA_DIR, "activity_journal.csv")

def log_to_journal(category, title, notes, priority="Sedang", status="Selesai", cost=0, location="", cost_cat=""):
    """Log an activity to the shared AgriSensa journal"""
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            
        df = pd.read_csv(JOURNAL_FILE) if os.path.exists(JOURNAL_FILE) else pd.DataFrame()
        
        new_entry = {
            'tanggal': datetime.now().strftime("%Y-%m-%d"),
            'kategori': category,
            'judul': title,
            'catatan': notes,
            'biaya': cost,
            'kategori_biaya': cost_cat,
            'lokasi': location,
            'prioritas': priority,
            'status': status,
            'foto_path': "",
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(JOURNAL_FILE, index=False)
        return True
    except Exception as e:
        print(f"Error logging to journal: {e}")
        return False
