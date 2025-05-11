from gemini.vegetation_image import search_image_url_wikimedia

def parse_vegetation_response(response_text: str):
    """
    Gemini 응답 텍스트를 파싱하여 structured JSON 형태로 반환.
    기대 응답 형식:
    * **소나무 / *Pinus densiflora***: 한국, 일본 등에 분포...
    """

    lines = response_text.splitlines()
    explanation_lines = []
    veg_lines = []

    for line in lines:
        if line.startswith("* **"):
            veg_lines.append(line)
        else:
            explanation_lines.append(line.strip())

    explanation = "\n".join([line for line in explanation_lines if line]).strip()

    def extract_name_and_text(line):
        try:
            # 예: * **소나무 / *Pinus densiflora***: 설명
            name_part = line.split("**")[1].strip()
            text = line.split("**")[2].lstrip(": ").strip()

            # 마크다운 이탤릭(*) 제거
            name_part = name_part.replace("*", "")

            # 한글/영문 이름 분리
            if "/" in name_part:
                kor_name, eng_name = [s.strip() for s in name_part.split("/", 1)]
            else:
                kor_name = eng_name = name_part

            return kor_name, eng_name, text
        except Exception as e:
            print(f"[파싱 오류] '{line}': {e}")
            return None, None, None

    vegs = [extract_name_and_text(line) for line in veg_lines]

    def build_veg_obj(veg):
        if veg is None or veg[0] is None:
            return None
        kor_name, eng_name, text = veg
        image_url = search_image_url_wikimedia(eng_name)
        print(f"🔍 [{kor_name}] 영어 이름 '{eng_name}' → 이미지 URL: {image_url}")
        return {
            "name": kor_name,
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