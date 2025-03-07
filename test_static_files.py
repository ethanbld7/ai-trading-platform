# test_static_files.py
from utils.file_generator import create_static_files

print("Creating static files...")
create_static_files()

import os
# Check if files were created
js_files = ["dashboard.js", "portfolio.js", "predictions.js"]
for file in js_files:
    path = os.path.join("static", "js", file)
    if os.path.exists(path):
        print(f"✓ Created: {path}")
    else:
        print(f"✗ Missing: {path}")