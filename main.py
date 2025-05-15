from fastapi import FastAPI, Query, HTTPException
from gee.auth import init_gee
from gee.fire_damage import analyze_fire_damage_ratio
from gee.fire_event import get_forest_fire_events
from gee.recovery_rate import predict_recovery_rate
from gee.ndvi_point import get_ndvi_at_point
from gemini.vegetation import vegetation_at_point
from utils.constants import NDVI_BEFORE_DATE, NDVI_AFTER_DATE

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_gee()

@app.get("/", tags=["Root"])
def root():
    return {"message": "🌲 Welcome to our wildfire recovery platform."}

@app.get("/fire-events", tags=["Fire"])
def get_fire_event_data():
    try:
        events = get_forest_fire_events()
        return {"event": events}
    except Exception as e:
        return {"error": f"Failed to retrieve fire events: {str(e)}"}

@app.get("/fire-damage", tags=["Damage"])
def get_damage_rate(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    damage = analyze_fire_damage_ratio(lat, lon)
    if damage is None:
        raise HTTPException(status_code=400, detail="Unable to calculate fire damage at the given location.")
    
    return {
        "lat": lat,
        "lon": lon,
        "damage": round(damage, 2)
    }

@app.get("/ndvi-recovery", tags=["Recovery"])
def get_recovery_rate(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    recovery = predict_recovery_rate(lat, lon)
    if recovery is None:
        raise HTTPException(status_code=400, detail="Unable to calculate NDVI recovery at the given location.")
    
    return {
        "lat": lat,
        "lon": lon,
        "recovery": round(recovery, 2)
    }

@app.get("/ndvi-recovery", tags=["Recovery"])
def get_recovery_rate(lat: float, lon: float):
    result = predict_recovery_rate(lat, lon)
    
    if result is None:
        raise HTTPException(status_code=400, detail="NDVI recovery rate could not be calculated for this location.")

    return {
        "lat": lat,
        "lon": lon,
        **result
    }
