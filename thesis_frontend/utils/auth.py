"""
Authentication utility for AgriSensa Streamlit
Database-backed via Vercel API with session fallback
"""

import streamlit as st
import requests
from datetime import datetime

# ========== API CONFIGURATION ==========
API_BASE_URL = "https://agriisensa-api2.vercel.app"

# ========== DEFAULT USERS (Fallback) ==========
DEFAULT_USERS = {
    'yandri': {
        'password': 'yandri2025',
        'role': 'superadmin',
        'name': 'Yandri - Owner',
        'email': 'yandri@agrisensa.com'
    },
    'admin': {
        'password': 'admin123',
        'role': 'admin',
        'name': 'Administrator',
        'email': 'admin@agrisensa.com'
    },
    'demo': {
        'password': 'demo123',
        'role': 'user',
        'name': 'Demo User',
        'email': 'demo@agrisensa.com'
    },
    'petani': {
        'password': 'petani123',
        'role': 'user',
        'name': 'Petani Indonesia',
        'email': 'petani@agrisensa.com'
    }
}


def api_request(endpoint: str, method: str = 'GET', data: dict = None) -> dict:
    """Make API request with error handling."""
    try:
        url = f"{API_BASE_URL}/api/auth/{endpoint}"
        if method == 'GET':
            response = requests.get(url, params=data, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {'success': False, 'message': f'API Error: {str(e)}', 'api_error': True}


def get_users():
    """Get users from session state."""
    if 'registered_users' not in st.session_state:
        st.session_state.registered_users = DEFAULT_USERS.copy()
    return st.session_state.registered_users


def get_activity_log():
    """Get user activity log from API."""
    if 'user_activity_log' not in st.session_state:
        st.session_state.user_activity_log = []
    
    # Try to get from API
    result = api_request('activities')
    if result.get('success') and result.get('activities'):
        return result['activities']
    
    return st.session_state.user_activity_log


def log_user_activity(username: str, action: str, details: str = ""):
    """Log user activity to API and session."""
    # Log to session
    log = st.session_state.get('user_activity_log', [])
    log.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'username': username,
        'action': action,
        'details': details
    })
    st.session_state.user_activity_log = log
    
    # Try to log to API
    api_request('log-activity', 'POST', {
        'username': username,
        'action': action,
        'details': details
    })


def init_auth_state():
    """Initialize authentication state."""
    # AUTO-LOGIN as Guest (User Request: Disable mandatory login)
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
    if 'user' not in st.session_state:
        st.session_state.user = {
            'username': 'guest',
            'name': 'Tamu (Guest)',
            'role': 'user', 
            'email': 'guest@agrisensa.com'
        }
    if 'user_activity_log' not in st.session_state:
        st.session_state.user_activity_log = []
    get_users()


def login(username: str, password: str) -> tuple:
    """Authenticate user with API, fallback to session."""
    init_auth_state()
    
    if not username or not password:
        return False, "Username dan password harus diisi"
    
    username = username.strip().lower()
    
    # Try API login first
    result = api_request('simple-login', 'POST', {
        'username': username,
        'password': password
    })
    
    if result.get('success'):
        user_data = result.get('user', {})
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': user_data.get('username', username),
            'name': user_data.get('name', username),
            'role': user_data.get('role', 'user'),
            'email': user_data.get('email', '')
        }
        return True, result.get('message', 'Login berhasil!')
    
    # If API fails (error or user not found), try local DEFAULT_USERS
    users = st.session_state.get('registered_users', DEFAULT_USERS)
    if username in users:
        if users[username]['password'] == password:
            st.session_state.authenticated = True
            st.session_state.user = {
                'username': username,
                'name': users[username]['name'],
                'role': users[username]['role'],
                'email': users[username]['email']
            }
            log_user_activity(username, 'LOGIN', 'Login via local')
            return True, f"Selamat datang, {users[username]['name']}!"
        else:
            return False, "Password salah"
    
    # If not in local users either, return the API message
    return False, result.get('message', 'Username tidak ditemukan')



def logout():
    """Logout current user."""
    if st.session_state.get('user'):
        log_user_activity(st.session_state.user['username'], 'LOGOUT', 'User logout')
    st.session_state.authenticated = False
    st.session_state.user = None


def register(username: str, password: str, name: str, email: str) -> tuple:
    """Register a new user via API with session fallback."""
    init_auth_state()
    
    if not username or not password or not name:
        return False, "Username, password, dan nama harus diisi"
    
    if len(username) < 3:
        return False, "Username minimal 3 karakter"
    
    if len(password) < 6:
        return False, "Password minimal 6 karakter"
    
    username = username.strip().lower()
    
    # Try API register first
    result = api_request('simple-register', 'POST', {
        'username': username,
        'password': password,
        'name': name,
        'email': email
    })
    
    if result.get('success'):
        user_data = result.get('user', {})
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': user_data.get('username', username),
            'name': user_data.get('name', name),
            'role': user_data.get('role', 'user'),
            'email': user_data.get('email', email)
        }
        return True, result.get('message', 'Registrasi berhasil!')
    
    # If API error, try session fallback
    if result.get('api_error'):
        users = st.session_state.get('registered_users', {})
        if username in users:
            return False, "Username sudah digunakan"
        
        users[username] = {
            'password': password,
            'role': 'user',
            'name': name,
            'email': email or f"{username}@agrisensa.com"
        }
        st.session_state.registered_users = users
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': username,
            'name': name,
            'role': 'user',
            'email': email or f"{username}@agrisensa.com"
        }
        log_user_activity(username, 'REGISTER', 'Register via fallback')
        return True, f"Selamat datang, {name}! Akun berhasil dibuat."
    
    return False, result.get('message', 'Registrasi gagal')


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    init_auth_state()
    return st.session_state.authenticated


def get_current_user() -> dict:
    """Get current logged in user info."""
    init_auth_state()
    return st.session_state.user


def require_auth():
    """Require authentication to access page."""
    init_auth_state()
    
    if not st.session_state.authenticated:
        show_login_required()
        st.stop()
    
    return st.session_state.user


def show_login_required():
    """Show login required message."""
    st.warning("🔐 **Login Diperlukan** - Silakan login untuk mengakses fitur ini")
    
    with st.form("quick_login"):
        st.markdown("### 🔑 Quick Login")
        username = st.text_input("Username", placeholder="admin / demo / petani")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login", use_container_width=True, type="primary"):
            success, message = login(username, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    st.caption("Demo: admin/admin123, demo/demo123, petani/petani123")


def show_user_info_sidebar():
    """Show current user info in sidebar."""
    if is_authenticated():
        user = get_current_user()
        role_icon = '👑' if user['role'] == 'superadmin' else ('🛡️' if user['role'] == 'admin' else '👤')
        st.sidebar.success(f"{role_icon} **{user['name']}** ({user['role']})")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
