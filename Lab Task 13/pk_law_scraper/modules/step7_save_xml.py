"""
Step 7 — Save XML Files
Outputs: pakistan_laws.xml, agencies.xml
"""

import os
from datetime import datetime


def _safe(text):
    """Escape XML special characters"""
    return str(text)\
        .replace("&", "&amp;")\
        .replace("<", "&lt;")\
        .replace(">", "&gt;")\
        .replace('"', "&quot;")


def save_xml(laws, agencies, output_dir):
    print("\n[STEP 7] Saving XML files...")
    out = f"{output_dir}/xml"
    os.makedirs(out, exist_ok=True)

    ts = datetime.now().isoformat()

    # pakistan_laws.xml
    path = f"{out}/pakistan_laws.xml"
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<PakistanLaws generated="{ts}" total="{len(laws)}">'
    ]
    for law in laws:
        lines.append(f'  <law id="{_safe(law["id"])}">')
        for k, v in law.items():
            lines.append(f"    <{k}>{_safe(v)}</{k}>")
        lines.append("  </law>")
    lines.append("</PakistanLaws>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ pakistan_laws.xml  ({len(laws)} laws)")

    # agencies.xml
    path = f"{out}/agencies.xml"
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<Agencies>"]
    for a in agencies:
        lines.append(f'  <agency id="{_safe(a["id"])}">')
        for k, v in a.items():
            if k == "regional_offices":
                lines.append("    <regional_offices>")
                for city, phone in v.items():
                    lines.append(f"      <office city='{_safe(city)}'>{_safe(phone)}</office>")
                lines.append("    </regional_offices>")
            else:
                lines.append(f"    <{k}>{_safe(v)}</{k}>")
        lines.append("  </agency>")
    lines.append("</Agencies>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ agencies.xml  ({len(agencies)} agencies)")
