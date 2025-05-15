import re
from gemini.vegetation_image import search_image_url_wikimedia

def extract_scientific_name(name: str) -> str:
    match = re.search(r"\(([^)]+)\)", name)
    return match.group(1).strip() if match else name.strip()

def extract_name_and_text(line: str):
    try:
        name_part = line.split("**")[1].strip()
        text = line.split("**")[2].lstrip(": ").strip()
        name_part = name_part.replace("*", "")  # remove markdown asterisks

        return name_part, None, text
    except Exception as e:
        print(f"[파싱 오류] '{line}': {e}")
        return None, None, None

def build_veg_obj(veg):
    if veg is None or veg[0] is None:
        return None
    name, _, text = veg
    search_name = extract_scientific_name(name)
    image_url = search_image_url_wikimedia(search_name)
    print(f"🔍 '{name}' → '{search_name}' → image: {image_url}")
    return {
        "name": name,
        "text": text,
        "image": image_url
    }

def parse_vegetation_response(response_text: str):
    lines = response_text.splitlines()
    explanation_lines = []
    veg_lines = []

    for line in lines:
        if line.startswith("* **"):
            veg_lines.append(line)
        else:
            explanation_lines.append(line.strip())

    explanation = "\n".join([line for line in explanation_lines if line])

    vegs = [extract_name_and_text(line) for line in veg_lines]

    return {
        "vegetation": {
            "explanation": explanation,
            "veg1": build_veg_obj(vegs[0]) if len(vegs) > 0 else None,
            "veg2": build_veg_obj(vegs[1]) if len(vegs) > 1 else None,
            "veg3": build_veg_obj(vegs[2]) if len(vegs) > 2 else None,
        }
    }