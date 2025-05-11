# gemini/vegetation.py
from gemini.vegetation_prompt import generate_vegetation_prompt
from gemini.vegetation_parser import parse_vegetation_response
import google.generativeai as genai
import os

model_name = os.getenv("GEMINI_MODEL", "models/gemini-1.5-pro")

def vegetation_at_point(lat: float, lon: float, ndvi: float):
    try: 
        prompt = generate_vegetation_prompt(lat, lon, ndvi)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        print("🧠 Gemini 응답 원문:\n", response.text)  # ✅ Gemini가 뭐라고 응답했는지 확인

        result = parse_vegetation_response(response.text)
        print("🌿 파싱 결과:\n", result)  # ✅ 실제 파싱된 결과 출력
        return result

    except Exception as e:
        return {"error": f"Gemini 오류: {str(e)}"}
