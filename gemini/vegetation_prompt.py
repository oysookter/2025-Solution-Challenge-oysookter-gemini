import os
import google.generativeai as genai

def generate_vegetation_prompt(lat: float, lon: float, ndvi: float) -> str:
    return f"""
The NDVI value at latitude {lat}, longitude {lon} is {round(ndvi, 3)}.

Based on this value, please provide a brief 3-line explanation of what the NDVI level indicates.

Then, list 3 plant species that are likely to grow in this region.

Each plant should be formatted like this:

* **[Scientific or English Name]**: [Brief description]

Do not include Korean names.
"""