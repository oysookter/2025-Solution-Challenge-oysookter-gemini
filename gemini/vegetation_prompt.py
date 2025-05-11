import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# gemini
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model_name = os.getenv("GEMINI_MODEL", "models/gemini-1.5-pro")

def generate_vegetation_prompt(lat: float, lon: float, ndvi: float) -> str:
    return f"""
위도 {lat}, 경도 {lon} 위치의 NDVI 값은 {round(ndvi, 3)}입니다.

이 값을 기반으로 NDVI에 대한 간단한 설명(3줄)과 함께, 해당 지역에서 서식할 가능성이 있는 식물 3가지를 알려줘.

각 식물은 다음 형식으로 작성해줘:

* **[한글 이름] / [영문 또는 학명]**: [간단한 설명]
"""