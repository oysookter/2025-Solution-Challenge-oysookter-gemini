import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# gemini
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model_name = os.getenv("GEMINI_MODEL", "models/gemini-1.5-pro")

def vegetation_at_point(lat: float, lon: float, ndvi: float):
    prompt = f"""
위도 {lat}, 경도 {lon} 위치의 NDVI 값은 {round(ndvi, 3)}입니다.

이 값을 기반으로 ndvi에 대한 설명 3줄과 함께 해당 지역에서 서식하는 식생을 세 가지 알려줘.
"""
    try:
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)     # ✅ prompt만 전달
        return response.text
    except Exception as e:
        return f"Gemini API 오류: {e}"