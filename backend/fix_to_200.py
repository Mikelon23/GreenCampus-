import os
import re

api_dir = r"c:\Users\Miguel\Desktop\Miguelon\GH\green-campus-plus\backend\api"
for file in os.listdir(api_dir):
    if not file.endswith(".py"): continue
    path = os.path.join(api_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove the response_class parameter if it was added incorrectly
    content = content.replace(", response_class=Response", "")
    
    # Change status_code=204 to status_code=200 on all endpoints to completely bypass this strict FastAPI 0.113+ validation
    # Since None is returned, 200 with no body is universally accepted and functionally identical for these clients
    if "status_code=204" in content:
        content = content.replace("status_code=204", "status_code=200")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Changed 204 to 200 in {file}")
