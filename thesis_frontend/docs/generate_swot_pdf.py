"""
AgriSensa SWOT Analysis PDF Generator
Generates a professional PDF report from the SWOT analysis
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
import os

class AgriSensaPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        
    def header(self):
        # Logo placeholder - green header bar
        self.set_fill_color(16, 185, 129)  # Emerald green
        self.rect(0, 0, 210, 15, 'F')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 5)
        self.cell(0, 5, 'AgriSensa Intelligence Platform', align='L')
        self.set_xy(-50, 5)
        self.cell(40, 5, 'SWOT Analysis 2025', align='R')
        self.ln(15)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | (c) 2025 AgriSensa Team', align='C')
        
    def chapter_title(self, title, emoji=""):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(6, 78, 59)  # Dark green
        self.cell(0, 10, f'{emoji} {title}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(16, 185, 129)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        
    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(5, 150, 105)  # Medium green
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        
    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(55, 65, 81)  # Gray
        self.multi_cell(0, 6, text)
        self.ln(2)
        
    def bullet_point(self, text, indent=10):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(55, 65, 81)
        current_x = self.get_x()
        self.set_x(current_x + indent)
        self.cell(5, 6, "-")  # Bullet character
        self.set_x(current_x + indent + 5)
        # Use remaining width for multi_cell
        remaining_width = 190 - indent - 5
        self.multi_cell(remaining_width, 6, text)
        
    def add_table(self, headers, data, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
            
        # Header
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(236, 253, 245)  # Light green
        self.set_text_color(6, 78, 59)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, fill=True, align='C')
        self.ln()
        
        # Data rows
        self.set_font('Helvetica', '', 9)
        self.set_text_color(55, 65, 81)
        fill = False
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), border=1, fill=fill, align='L')
            self.ln()
            fill = not fill
        self.ln(5)

    def highlight_box(self, text, color_type="info"):
        colors = {
            "info": (219, 234, 254),      # Blue
            "success": (209, 250, 229),   # Green
            "warning": (254, 243, 199),   # Yellow
            "danger": (254, 226, 226)     # Red
        }
        self.set_fill_color(*colors.get(color_type, colors["info"]))
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(55, 65, 81)
        
        # Calculate height needed
        self.set_x(15)
        self.multi_cell(180, 6, text, border=0, fill=True)
        self.ln(3)

def generate_swot_pdf():
    pdf = AgriSensaPDF()
    pdf.alias_nb_pages()
    
    # ========== COVER PAGE ==========
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 36)
    pdf.set_text_color(6, 78, 59)
    pdf.ln(40)
    pdf.cell(0, 20, 'ANALISIS SWOT', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 20, '& EXECUTIVE SUMMARY', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 10, 'AgriSensa Intelligence Platform', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', 'I', 14)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 10, 'AI-Powered Smart Farming Super App', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(30)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 8, f'Versi Dokumen: 1.0', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f'Tanggal: {datetime.now().strftime("%d %B %Y")}', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, 'Penyusun: Tim AgriSensa', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Green box at bottom
    pdf.set_y(-50)
    pdf.set_fill_color(16, 185, 129)
    pdf.rect(0, 260, 210, 37, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_y(-40)
    pdf.cell(0, 8, 'Build for Indonesian Agriculture Sovereignty', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # ========== EXECUTIVE SUMMARY ==========
    pdf.add_page()
    pdf.chapter_title("EXECUTIVE SUMMARY", "")
    
    pdf.section_title("Tentang AgriSensa")
    pdf.body_text(
        "AgriSensa adalah platform kecerdasan pertanian terpadu (Integrated Agricultural "
        "Intelligence Platform) yang mengintegrasikan 55+ modul dalam satu ekosistem. "
        "Platform ini menggabungkan teknologi mutakhir seperti Artificial Intelligence, "
        "Geospatial Technology, Data Science, dan IoT Integration."
    )
    
    pdf.ln(3)
    pdf.highlight_box(
        "Value Proposition: Superapp Pertanian Modern yang memberdayakan petani, peneliti, "
        "dan pelaku agribisnis Indonesia dengan teknologi presisi untuk revolusi ketahanan pangan.",
        "success"
    )
    
    pdf.section_title("Key Metrics")
    pdf.add_table(
        ["Metrik", "Nilai"],
        [
            ["Total Modul", "55+ modul terintegrasi"],
            ["Kategori Fitur", "8 kategori utama"],
            ["Tech Stack", "Python, Streamlit, OpenCV, Folium"],
            ["AI Integration", "Google Gemini, Computer Vision"],
            ["Target Users", "Petani, PPL, Peneliti, Agribisnis"],
        ],
        [60, 130]
    )
    
    # ========== STRENGTHS ==========
    pdf.add_page()
    pdf.chapter_title("STRENGTHS (Kekuatan)", "")
    
    pdf.section_title("1. Cakupan Modul Paling Komprehensif di Indonesia")
    pdf.bullet_point("55+ modul yang mencakup seluruh value chain pertanian")
    pdf.bullet_point("Dari hulu (input pertanian) hingga hilir (pasca panen)")
    pdf.bullet_point("Fitur yang terintegrasi dalam satu platform terpadu")
    pdf.ln(3)
    
    pdf.section_title("2. Integrasi AI & Computer Vision Tingkat Lanjut")
    pdf.add_table(
        ["Fitur AI", "Deskripsi"],
        [
            ["AgriSensa Vision", "Analisis foto drone untuk pemetaan tanaman"],
            ["Dokter Tanaman AI", "Deteksi hama & penyakit dengan Gemini AI"],
            ["Prediksi Panen", "ML untuk estimasi produktivitas"],
            ["Asisten Penelitian", "Analisis statistik otomatis (ANOVA)"],
        ],
        [50, 140]
    )
    
    pdf.section_title("3. Teknologi Geospasial Modern")
    pdf.bullet_point("Peta interaktif dengan Folium")
    pdf.bullet_point("Analisis kesesuaian lahan berdasarkan ketinggian & iklim")
    pdf.bullet_point("Integrasi cuaca real-time (Open-Meteo API)")
    pdf.bullet_point("NDVI mapping & GIS Intelligence")
    pdf.ln(3)
    
    pdf.section_title("4. UI/UX Premium & Modern")
    pdf.bullet_point("Desain Glassmorphism yang elegan dan profesional")
    pdf.bullet_point("Animasi modern & micro-interactions")
    pdf.bullet_point("Bilingual support (Bahasa Indonesia & English)")
    pdf.ln(3)
    
    pdf.section_title("5. Kombinasi Keahlian yang Langka")
    pdf.body_text(
        "Platform ini memerlukan kombinasi keahlian yang sangat jarang: "
        "Agronomist + Software Engineer + Data Scientist + UX Designer"
    )
    
    # ========== WEAKNESSES ==========
    pdf.add_page()
    pdf.chapter_title("WEAKNESSES (Kelemahan)", "")
    
    pdf.section_title("1. Basis Pengguna Masih Terbatas")
    pdf.bullet_point("Platform masih dalam tahap pengembangan")
    pdf.bullet_point("Belum ada base user aktif yang signifikan")
    pdf.bullet_point("Perlu strategi marketing yang kuat")
    pdf.ln(3)
    
    pdf.section_title("2. Ketergantungan pada API Eksternal")
    pdf.bullet_point("Cuaca: Open-Meteo API")
    pdf.bullet_point("AI: Google Gemini API")
    pdf.bullet_point("Elevasi: Open-Elevation API")
    pdf.bullet_point("Risiko jika layanan pihak ketiga bermasalah")
    pdf.ln(3)
    
    pdf.section_title("3. Infrastruktur Monetisasi Belum Matang")
    pdf.bullet_point("Model bisnis belum sepenuhnya terimplementasi")
    pdf.bullet_point("Belum ada sistem subscription/premium")
    pdf.bullet_point("Perlu strategi revenue yang jelas")
    pdf.ln(3)
    
    pdf.section_title("4. Data Lokal Terbatas")
    pdf.bullet_point("Database komoditas masih statis")
    pdf.bullet_point("Perlu integrasi data harga pasar real-time")
    pdf.bullet_point("Data spesifik lokasi Indonesia perlu diperkaya")
    
    # ========== OPPORTUNITIES ==========
    pdf.add_page()
    pdf.chapter_title("OPPORTUNITIES (Peluang)", "")
    
    pdf.section_title("1. Pasar AgriTech Indonesia yang Berkembang Pesat")
    pdf.highlight_box(
        "Proyeksi Pasar AgriTech Indonesia: "
        "2023: $1.2 Billion  |  2028: $3.5 Billion (CAGR ~24%)",
        "success"
    )
    
    pdf.section_title("2. Dukungan Pemerintah untuk Digitalisasi Pertanian")
    pdf.bullet_point("Program Pertanian 4.0 oleh Kementerian Pertanian")
    pdf.bullet_point("Inisiatif Smart Farming di berbagai daerah")
    pdf.bullet_point("Dana CSR dari BUMN untuk pemberdayaan petani")
    pdf.ln(3)
    
    pdf.section_title("3. Gap Besar antara Kebutuhan dan Solusi")
    pdf.add_table(
        ["Kebutuhan", "Solusi Existing", "AgriSensa"],
        [
            ["Rekomendasi pupuk", "Manual/Spreadsheet", "AI-Powered"],
            ["Deteksi hama", "Tidak ada", "Computer Vision"],
            ["Analisis bisnis tani", "Sederhana", "Komprehensif"],
            ["Edukasi petani", "Fragmented", "Terintegrasi"],
        ],
        [60, 60, 70]
    )
    
    pdf.section_title("4. Potensi Ekspansi Regional ASEAN")
    pdf.bullet_point("Kesamaan komoditas dengan negara ASEAN")
    pdf.bullet_point("Potensi adaptasi untuk Thailand, Vietnam, Filipina")
    pdf.bullet_point("Model SaaS yang scalable")
    pdf.ln(3)
    
    pdf.section_title("5. Kemitraan Strategis")
    pdf.bullet_point("Universitas: Untuk riset dan validasi")
    pdf.bullet_point("Kementerian Pertanian: Untuk adopsi massal")
    pdf.bullet_point("Perusahaan Agro-Input: Untuk sponsorship")
    pdf.bullet_point("Bank/Fintech Pertanian: Untuk pembiayaan petani")
    
    # ========== THREATS ==========
    pdf.add_page()
    pdf.chapter_title("THREATS (Ancaman)", "")
    
    pdf.section_title("1. Kompetitor dengan Funding Besar")
    pdf.add_table(
        ["Kompetitor", "Fokus", "Funding"],
        [
            ["TaniHub", "Marketplace", "$65M+"],
            ["Eden Farm", "B2B Supply", "$27M+"],
            ["eFishery", "Aquaculture IoT", "$200M+"],
        ],
        [60, 70, 60]
    )
    
    pdf.section_title("2. Adopsi Teknologi Petani yang Masih Rendah")
    pdf.bullet_point("Literasi digital petani Indonesia masih terbatas")
    pdf.bullet_point("Infrastruktur internet di pedesaan belum merata")
    pdf.bullet_point("Perlu pendekatan edukasi yang intensif")
    pdf.ln(3)
    
    pdf.section_title("3. Regulasi Data & Privasi")
    pdf.bullet_point("Potensi regulasi ketat untuk data pertanian")
    pdf.bullet_point("Isu kepemilikan data petani")
    pdf.bullet_point("Compliance dengan standar keamanan")
    pdf.ln(3)
    
    pdf.section_title("4. Perubahan Cepat Teknologi AI")
    pdf.bullet_point("Model AI terus berkembang")
    pdf.bullet_point("Perlu update konstan untuk tetap relevan")
    pdf.bullet_point("Biaya maintenance yang meningkat")
    
    # ========== STRATEGIC RECOMMENDATIONS ==========
    pdf.add_page()
    pdf.chapter_title("STRATEGIC RECOMMENDATIONS", "")
    
    pdf.section_title("Jangka Pendek (0-6 Bulan)")
    pdf.bullet_point("Validasi MVP dengan 100 petani aktif (Early Adopters)")
    pdf.bullet_point("Fokus pada 3-5 modul unggulan")
    pdf.bullet_point("Bangun komunitas (WhatsApp/Telegram)")
    pdf.bullet_point("Content marketing di media sosial")
    pdf.bullet_point("Video tutorial untuk setiap modul")
    pdf.ln(3)
    
    pdf.section_title("Jangka Menengah (6-18 Bulan)")
    pdf.bullet_point("Monetisasi: Freemium model (Basic gratis, Premium berbayar)")
    pdf.bullet_point("B2B licensing ke perusahaan agro-input")
    pdf.bullet_point("Integrasi IoT Hardware (sensor tanah, drone)")
    pdf.bullet_point("Ekspansi database dengan data real-time")
    pdf.ln(3)
    
    pdf.section_title("Jangka Panjang (18-36 Bulan)")
    pdf.bullet_point("Regional Expansion ke pasar ASEAN")
    pdf.bullet_point("Multi-language support")
    pdf.bullet_point("Advanced AI: Autonomous drone planning")
    pdf.bullet_point("Ekosistem terintegrasi: Marketplace, Fintech, Insurance")
    
    # ========== VALUATION ==========
    pdf.add_page()
    pdf.chapter_title("POTENSI VALUASI", "")
    
    pdf.section_title("Comparable Analysis")
    pdf.add_table(
        ["Startup AgriTech", "Valuasi Terakhir", "Stage"],
        [
            ["eFishery (ID)", "$1.2 Billion", "Series D"],
            ["DeHaat (India)", "$850 Million", "Series E"],
            ["Cropin (India)", "$400 Million", "Series D"],
            ["AgriWebb (Australia)", "$100 Million", "Series B"],
        ],
        [70, 60, 60]
    )
    
    pdf.section_title("Faktor Penilaian AgriSensa")
    pdf.add_table(
        ["Faktor", "Score", "Catatan"],
        [
            ["Technology Moat", "9/10", "Sangat sulit direplikasi"],
            ["Market Potential", "8/10", "Indonesia = pasar besar"],
            ["Team Expertise", "8/10", "Kombinasi unik Agro + Tech"],
            ["Product Completeness", "9/10", "55+ modul terintegrasi"],
            ["Revenue Model", "5/10", "Perlu validasi"],
            ["User Traction", "4/10", "Masih early stage"],
        ],
        [60, 30, 100]
    )
    
    pdf.ln(5)
    pdf.highlight_box(
        "Estimasi Valuasi: Pre-Seed: $500K - $1.5M | Seed (dengan traction): $2M - $5M",
        "info"
    )
    
    # ========== CONCLUSION ==========
    pdf.add_page()
    pdf.chapter_title("KESIMPULAN", "")
    
    pdf.body_text(
        "AgriSensa memiliki keunggulan kompetitif yang sangat kuat terutama dari sisi:"
    )
    pdf.ln(3)
    
    pdf.bullet_point("Kelengkapan fitur (55+ modul paling komprehensif)")
    pdf.bullet_point("Integrasi teknologi (AI, GIS, Data Science)")
    pdf.bullet_point("Kualitas UI/UX (Premium, modern, profesional)")
    pdf.bullet_point("Kedalaman konten (Pengetahuan agronomis yang kaya)")
    pdf.bullet_point("Keunikan tim (Kombinasi keahlian yang langka)")
    
    pdf.ln(10)
    pdf.section_title("Next Steps Prioritas")
    pdf.bullet_point("Validasi pasar dengan early adopters")
    pdf.bullet_point("Bangun traction (user acquisition)")
    pdf.bullet_point("Definisikan revenue model yang jelas")
    pdf.bullet_point("Jalin kemitraan strategis")
    pdf.bullet_point("Prepare untuk fundraising (jika diperlukan)")
    
    pdf.ln(20)
    pdf.set_fill_color(236, 253, 245)
    pdf.set_draw_color(16, 185, 129)
    pdf.rect(15, pdf.get_y(), 180, 30, 'DF')
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(6, 78, 59)
    pdf.set_xy(20, pdf.get_y() + 5)
    pdf.cell(170, 8, 'AgriSensa Intelligence Systems', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_x(20)
    pdf.cell(170, 6, 'Website: https://agrisensa-app.streamlit.app/', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(20)
    pdf.cell(170, 6, 'Build for Indonesian Agriculture Sovereignty', align='C')
    
    # Save PDF
    output_path = os.path.join(os.path.dirname(__file__), "AgriSensa_SWOT_Analysis_2025.pdf")
    pdf.output(output_path)
    print(f"PDF berhasil dibuat: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_swot_pdf()
