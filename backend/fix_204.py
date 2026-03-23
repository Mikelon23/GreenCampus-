import os
import re

api_dir = r"c:\Users\Miguel\Desktop\Miguelon\GH\green-campus-plus\backend\api"
for file in os.listdir(api_dir):
    if not file.endswith(".py"): continue
    path = os.path.join(api_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "status_code=204" in content:
        if "from fastapi import " in content and "Response" not in content:
            # Add Response to the existing from fastapi import ...
            content = re.sub(
                r"(from fastapi import\s+(?:\([^)]+\)|[^\n]+))",
                lambda m: m.group(1).replace(")", ", Response)") if "(" in m.group(1) else m.group(1) + ", Response",
                content,
                count=1
            )
        
        # Only replace if not already there
        if "response_class=Response" not in content:
            content = content.replace("status_code=204)", "status_code=204, response_class=Response)")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed {file}")
