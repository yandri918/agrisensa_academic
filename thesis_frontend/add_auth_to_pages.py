"""
Script to add authentication check to all Streamlit pages
Run this once to add require_auth() to all pages
"""

import os
import re

PAGES_DIR = r"c:\Users\yandr\OneDrive\Desktop\agrisensa-api\agrisensa_streamlit\pages"

# Auth imports to add
AUTH_IMPORT = "from utils.auth import require_auth, show_user_info_sidebar"
AUTH_CHECK = """
# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================
"""

# Files to skip (already have auth or are admin pages)
SKIP_FILES = [
    "99_🔐_Admin_Dashboard.py",  # Has its own auth
]

def add_auth_to_file(filepath):
    """Add auth check to a single file."""
    filename = os.path.basename(filepath)
    
    if filename in SKIP_FILES:
        print(f"⏭️  Skipping: {filename}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has auth
    if 'require_auth' in content or 'from utils.auth' in content:
        print(f"✅ Already has auth: {filename}")
        return False
    
    # Find the position after imports and page config
    # Look for st.set_page_config or first st. call
    
    lines = content.split('\n')
    new_lines = []
    auth_added = False
    import_added = False
    in_imports = True
    page_config_found = False
    
    for i, line in enumerate(lines):
        # Add import after other imports
        if not import_added and line.strip() and not line.startswith('#') and not line.startswith('import') and not line.startswith('from') and in_imports:
            # End of imports section, add our import
            new_lines.append(AUTH_IMPORT)
            new_lines.append('')
            import_added = True
            in_imports = False
        
        new_lines.append(line)
        
        # After page_config, add auth check
        if not auth_added and 'st.set_page_config' in line:
            page_config_found = True
            # Find the closing parenthesis
            paren_count = line.count('(') - line.count(')')
            j = i
            while paren_count > 0 and j < len(lines) - 1:
                j += 1
                new_lines.append(lines[j])
                paren_count += lines[j].count('(') - lines[j].count(')')
            
            # Now add auth check
            new_lines.append(AUTH_CHECK)
            auth_added = True
            
            # Skip the lines we already processed
            for k in range(i + 1, j + 1):
                lines[k] = ''
    
    # If no page_config found, add at beginning after imports
    if not auth_added:
        # Find first non-import, non-blank, non-comment line
        insert_pos = 0
        for i, line in enumerate(new_lines):
            if line.strip() and not line.startswith('#') and not line.startswith('import') and not line.startswith('from') and line != AUTH_IMPORT:
                insert_pos = i
                break
        
        new_lines.insert(insert_pos, AUTH_CHECK)
        if not import_added:
            new_lines.insert(0, AUTH_IMPORT)
    
    new_content = '\n'.join(new_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Added auth: {filename}")
    return True

def main():
    print("=" * 50)
    print("Adding Authentication to All Pages")
    print("=" * 50)
    
    updated = 0
    skipped = 0
    
    for filename in sorted(os.listdir(PAGES_DIR)):
        if filename.endswith('.py'):
            filepath = os.path.join(PAGES_DIR, filename)
            if add_auth_to_file(filepath):
                updated += 1
            else:
                skipped += 1
    
    print("=" * 50)
    print(f"✅ Updated: {updated} files")
    print(f"⏭️  Skipped: {skipped} files")
    print("=" * 50)

if __name__ == "__main__":
    main()
