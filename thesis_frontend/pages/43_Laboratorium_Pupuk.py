import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Laboratorium Pupuk Organik | AgriSensa Eco",
    page_icon="🧴",
    layout="wide"
)

# Load the HTML and CSS
try:
    with open("agrisensa-eco-lab/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    with open("agrisensa-eco-lab/style.css", "r", encoding="utf-8") as f:
        css_content = f.read()
    
    # Inject CSS into HTML
    full_html = f"<style>{css_content}</style>{html_content}"
    
    # Adjust for Streamlit: Remove <html>, <head>, <body> tags as they are being injected into an iframe
    # Also adjust relative paths if any.
    
    components.html(full_html, height=2500, scrolling=True)

except Exception as e:
    st.error(f"Gagal memuat konten Laboratorium: {e}")
    st.info("Pastikan file 'index.html' dan 'style.css' tersedia di folder 'agrisensa-eco-lab'.")
