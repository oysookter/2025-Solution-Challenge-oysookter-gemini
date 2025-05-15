import re
from vegetation_image import search_image_url_wikimedia

def extract_scientific_name(name: str) -> str:
    match = re.search(r"\(([^)]+)\)", name)
    return match.group(1).strip() if match else name.strip()

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