"""
AgriSensa Design System
=======================
Centralized styling tokens, CSS templates, and reusable UI components.
Import this module to maintain consistent styling across all pages.
"""

# =============================================================================
# COLOR TOKENS
# =============================================================================
COLORS = {
    # Primary Palette
    "primary": "#10b981",       # Emerald Green (Sustainability)
    "primary_dark": "#059669",
    "primary_light": "#34d399",
    
    # Secondary Palette
    "secondary": "#3b82f6",     # Blue (Technology)
    "secondary_dark": "#2563eb",
    "secondary_light": "#60a5fa",
    
    # Accent Colors
    "accent": "#f59e0b",        # Amber (Highlight)
    "accent_dark": "#d97706",
    "accent_light": "#fbbf24",
    
    # Semantic Colors
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#3b82f6",
    
    # Neutral Palette
    "white": "#ffffff",
    "gray_50": "#f9fafb",
    "gray_100": "#f3f4f6",
    "gray_200": "#e5e7eb",
    "gray_300": "#d1d5db",
    "gray_400": "#9ca3af",
    "gray_500": "#6b7280",
    "gray_600": "#4b5563",
    "gray_700": "#374151",
    "gray_800": "#1f2937",
    "gray_900": "#111827",
    "black": "#000000",
}

# =============================================================================
# TYPOGRAPHY
# =============================================================================
FONTS = {
    "primary": "'Inter', 'Segoe UI', sans-serif",
    "mono": "'JetBrains Mono', 'Consolas', monospace",
}

# =============================================================================
# SPACING & SIZING
# =============================================================================
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "2xl": "48px",
}

BORDER_RADIUS = {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "9999px",
}

# =============================================================================
# CSS TEMPLATES
# =============================================================================
def get_base_css():
    """Returns the base CSS for consistent styling across all pages."""
    return f"""
    <style>
        /* AgriSensa Design System v1.0 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global Overrides */
        .stApp {{
            font-family: {FONTS['primary']};
        }}
        
        /* Card Styles */
        .agri-card {{
            background: {COLORS['white']};
            padding: {SPACING['lg']};
            border-radius: {BORDER_RADIUS['lg']};
            border-left: 5px solid {COLORS['primary']};
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: {SPACING['md']};
        }}
        
        .agri-card-accent {{
            background: linear-gradient(135deg, {COLORS['gray_50']} 0%, {COLORS['white']} 100%);
            border-left-color: {COLORS['accent']};
        }}
        
        .agri-card-info {{
            background: #eff6ff;
            border-left-color: {COLORS['info']};
        }}
        
        .agri-card-success {{
            background: #ecfdf5;
            border-left-color: {COLORS['success']};
        }}
        
        .agri-card-warning {{
            background: #fffbeb;
            border-left-color: {COLORS['warning']};
        }}
        
        .agri-card-danger {{
            background: #fef2f2;
            border-left-color: {COLORS['danger']};
        }}
        
        /* Header Styles */
        .agri-header {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
            color: {COLORS['white']};
            padding: {SPACING['lg']};
            border-radius: {BORDER_RADIUS['lg']};
            margin-bottom: {SPACING['lg']};
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        }}
        
        .agri-header h1 {{
            margin: 0;
            font-weight: 700;
        }}
        
        .agri-header p {{
            margin: {SPACING['sm']} 0 0 0;
            opacity: 0.9;
        }}
        
        /* Metric Card */
        .agri-metric {{
            background: {COLORS['white']};
            padding: {SPACING['md']};
            border-radius: {BORDER_RADIUS['md']};
            text-align: center;
            border: 1px solid {COLORS['gray_200']};
        }}
        
        .agri-metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {COLORS['primary']};
        }}
        
        .agri-metric-label {{
            font-size: 0.85rem;
            color: {COLORS['gray_500']};
            margin-top: {SPACING['xs']};
        }}
        
        /* Badge */
        .agri-badge {{
            display: inline-block;
            padding: {SPACING['xs']} {SPACING['sm']};
            border-radius: {BORDER_RADIUS['full']};
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .agri-badge-success {{
            background: {COLORS['success']};
            color: {COLORS['white']};
        }}
        
        .agri-badge-warning {{
            background: {COLORS['warning']};
            color: {COLORS['white']};
        }}
        
        .agri-badge-danger {{
            background: {COLORS['danger']};
            color: {COLORS['white']};
        }}
        
        /* Print Optimization */
        @media print {{
            [data-testid="stSidebar"], 
            header, 
            footer, 
            .stButton, 
            .stDownloadButton, 
            [data-testid="stHeader"], 
            [data-testid="stToolbar"],
            [data-testid="stNotification"] {{
                display: none !important;
            }}
            
            .stApp, .main, .block-container, .stAppViewContainer {{
                overflow: visible !important;
                height: auto !important;
                min-height: auto !important;
                padding-top: 0 !important;
                margin: 0 !important;
            }}
            
            .agri-card, .agri-header, .agri-metric {{
                break-inside: avoid;
                box-shadow: none !important;
                border: 1px solid {COLORS['gray_200']} !important;
            }}
        }}
    </style>
    """

# =============================================================================
# COMPONENT GENERATORS
# =============================================================================
def card(content: str, variant: str = "default") -> str:
    """
    Generate an AgriSensa styled card.
    
    Args:
        content: HTML content inside the card
        variant: 'default', 'accent', 'info', 'success', 'warning', 'danger'
    
    Returns:
        HTML string for the card
    """
    variant_class = f"agri-card-{variant}" if variant != "default" else ""
    return f'<div class="agri-card {variant_class}">{content}</div>'


def header(title: str, subtitle: str = "") -> str:
    """Generate an AgriSensa styled page header."""
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    return f'<div class="agri-header"><h1>{title}</h1>{sub}</div>'


def metric_card(value: str, label: str) -> str:
    """Generate an AgriSensa styled metric display."""
    return f'''
    <div class="agri-metric">
        <div class="agri-metric-value">{value}</div>
        <div class="agri-metric-label">{label}</div>
    </div>
    '''


def badge(text: str, variant: str = "success") -> str:
    """Generate an AgriSensa styled badge."""
    return f'<span class="agri-badge agri-badge-{variant}">{text}</span>'


# =============================================================================
# QUICK ACCESS
# =============================================================================
def inject_styles():
    """
    Convenience function to inject all AgriSensa styles.
    Call this at the beginning of each page: 
    
        import streamlit as st
        from utils.styles import inject_styles
        inject_styles()
    """
    import streamlit as st
    st.markdown(get_base_css(), unsafe_allow_html=True)
