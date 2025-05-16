from typing import Optional, Tuple, Dict, List
from gemini.vegetation_image import search_image_url_wikimedia

def extract_name_and_text(line: str) -> Optional[Tuple[str, str]]:
    """
    ex: * **Pinus densiflora**: A hardy conifer...
    """
    try:
        # take scientific name
        name_part = line.split("**")[1].strip()
        text_part = line.split("**")[2].lstrip(": ").strip()
        return name_part, text_part
    except Exception as e:
        print(f"[⚠️ parsing error] '{line}': {e}")
        return None


def build_veg_obj(veg: Optional[Tuple[str, str]]) -> Optional[Dict]:
    """
    make dic including scientific name and img url
    """
    if veg is None or veg[0] is None:
        return None
    name, text = veg
    image_url = search_image_url_wikimedia(name)
    print(f"🔍 '{name}' → image: {image_url}")
    return {
        "name": name,
        "text": text,
        "image": image_url
    }


def parse_vegetation_response(response_text: str) -> Dict:
    """
    Gemini return explaination and 3 vegetations from entire text
    """
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

    vegetation_result = {
        "explanation": explanation,
        "veg1": veg_objs[0] if len(veg_objs) > 0 else None,
        "veg2": veg_objs[1] if len(veg_objs) > 1 else None,
        "veg3": veg_objs[2] if len(veg_objs) > 2 else None,
    }

    return {"vegetation": vegetation_result}