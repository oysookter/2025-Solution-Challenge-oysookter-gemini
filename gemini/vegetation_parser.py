from gemini.vegetation_image import search_image_url_wikimedia

def parse_vegetation_response(response_text: str):
    """
    Gemini 응답 텍스트를 파싱하여 structured JSON 형태로 반환.
    기대 응답 형식:
    * **Pinus densiflora**: Description...
    """

    lines = response_text.splitlines()
    explanation_lines = []
    veg_lines = []

    for line in lines:
        if line.startswith("* **"):
            veg_lines.append(line)
        else:
            cleaned_line = line.strip()
            if cleaned_line.startswith("*:"):
                cleaned_line = cleaned_line[2:].strip()
            explanation_lines.append(cleaned_line)

    explanation = "\n".join([line for line in explanation_lines if line]).strip()

    def extract_name_and_text(line):
        try:
            # 예: * **Pinus densiflora**: Description
            name = line.split("**")[1].strip().replace("*", "")
            text = line.split("**")[2].lstrip(": ").strip()
            return name, text
        except Exception as e:
            print(f"[Parsing Error] '{line}': {e}")
            return None, None

    vegs = [extract_name_and_text(line) for line in veg_lines]

    def build_veg_obj(veg):
        if veg is None or veg[0] is None:
            return None
        name, text = veg
        image_url = search_image_url_wikimedia(name)
        print(f"🔍 '{name}' → Image URL: {image_url}")
        return {
            "name": name,
            "text": text,
            "image": image_url
        }

    return {
        "vegetation": {
            "explanation": explanation,
            "veg1": build_veg_obj(vegs[0]) if len(vegs) > 0 else None,
            "veg2": build_veg_obj(vegs[1]) if len(vegs) > 1 else None,
            "veg3": build_veg_obj(vegs[2]) if len(vegs) > 2 else None,
        }
    }