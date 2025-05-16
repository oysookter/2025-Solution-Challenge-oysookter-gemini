# vegetation_prompt.py

def generate_vegetation_prompt(lat: float, lon: float, ndvi: float) -> str:
    return f"""
The NDVI value at latitude {lat}, longitude {lon} is {round(ndvi, 3)}.

Based on this value, briefly explain in 3 lines what this NDVI level indicates in terms of vegetation density and condition.

Then, list 3 plant species that are likely to grow in this region.

* Only use scientific (Latin) names. Do not use common or English names.
* Each plant must follow this format:

- **[Scientific Name]**: [Brief ecological description]

Do not include any Korean or common names. Only scientific names must be shown.
"""