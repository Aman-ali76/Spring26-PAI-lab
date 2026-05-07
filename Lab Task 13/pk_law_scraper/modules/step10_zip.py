"""
Step 10 — Create ZIP Archive
Zips the entire output/ folder into pakistan_law_dataset.zip
"""

import os
import zipfile

ZIP_NAME = "pakistan_law_dataset.zip"


def create_zip(output_dir):
    print("\n[STEP 10] Creating ZIP archive...")

    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)

    file_count = 0
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname  = os.path.relpath(filepath, start=".")
                zf.write(filepath, arcname)
                file_count += 1

    size_mb = os.path.getsize(ZIP_NAME) / (1024 * 1024)
    print(f"  ✅ {ZIP_NAME}  ({file_count} files, {size_mb:.1f} MB)")
    return ZIP_NAME
