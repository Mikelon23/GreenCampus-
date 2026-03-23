import os

api_dir = r"c:\Users\Miguel\Desktop\Miguelon\GH\green-campus-plus\backend\api"
for file in os.listdir(api_dir):
    if not file.endswith(".py"): continue
    path = os.path.join(api_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "response_class=Response" in content and "Response" not in content[:content.find("response_class=Response")]:
        # Simple string injection at the very top instead of tricky regex
        content = "from fastapi import Response\n" + content
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed imports {file}")
