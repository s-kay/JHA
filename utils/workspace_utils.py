# utils/workspace_utils.py

import os
from datetime import datetime

def save_to_workspace(content, filename_prefix="tailored_resume", ext="txt"):
    os.makedirs("workspace", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.{ext}"
    file_path = os.path.join("workspace", filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return file_path
