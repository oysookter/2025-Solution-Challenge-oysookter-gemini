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
        print("🧠 Gemini answer:\n", response.text)

        result = parse_vegetation_response(response.text)
        print("🌿 parsed result:\n", result)
        return result

    except Exception as e:
        return {"error": f"Gemini Error: {str(e)}"}