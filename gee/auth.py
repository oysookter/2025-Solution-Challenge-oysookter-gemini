import os
import ee

def init_gee():
    try:
        ee.Initialize(project=os.getenv("GEE_PROJECT_ID"))
        print("✅ Earth Engine initialized.")
    except Exception:
        print("🌐 Run 'earthengine authenticate' manually if not already done.")