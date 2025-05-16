from typing import Optional, Tuple, Dict
from gemini.vegetation_image import search_image_url_wikimedia

def extract_name_and_text(line: str) -> Optional[Tuple[str, str]]:
    try:
        name = line.split("**")[1].strip()
        desc = line.split("**")[2].lstrip(": ").strip()
        return name, desc
    except Exception as e:
        print(f"[⚠️ Parsing error] '{line}': {e}")
        return None


def build_veg_obj(veg: Optional[Tuple[str, str]]) -> Optional[Dict[str, str]]:
    if veg is None or not veg[0]:
        return None

    name, text = veg
    image_url = search_image_url_wikimedia(name)
    print(f"🔍 {name} → {image_url}")
    return {"name": name, "text": text, "image": image_url}


def parse_vegetation_response(response_text: str) -> Dict[str, Dict]:
    lines = response_text.splitlines()
    explanation_lines = []
    veg_lines = []

    for line in lines:
        if line.startswith("* **"):
            veg_lines.append(line)
        else:
            explanation_lines.append(line.strip())

    explanation = "\n".join(filter(None, explanation_lines))
    vegs = [extract_name_and_text(line) for line in veg_lines[:3]]
    veg_objs = [build_veg_obj(veg) for veg in vegs]

    return {
        "vegetation": {
            "explanation": explanation,
            "veg1": veg_objs[0] if len(veg_objs) > 0 else None,
            "veg2": veg_objs[1] if len(veg_objs) > 1 else None,
            "veg3": veg_objs[2] if len(veg_objs) > 2 else None,
        }
    }