from fastapi import FastAPI, Query, HTTPException
from gee.auth import init_gee
from gee.fire_damage import analyze_fire_damage_ratio
from gee.fire_event import get_forest_fire_events
from gee.recovery_rate import predict_recovery_rate
from gee.ndvi_point import get_ndvi_at_point
from gemini.vegetation import vegetation_at_point
from utils.constants import NDVI_BEFORE_DATE, NDVI_AFTER_DATE

app = FastAPI()

# GEE 초기화는 앱 시작 시 1회
init_gee()

@app.get("/", tags=["Root"])
def root():
    return {"message": "🌲 산불 복구 서비스에 오신 것을 환영합니다."}

# 아직 적용안된 코드
@app.get("/fire-events", tags=["Fire"])
def get_fire_event_data():
    events = get_forest_fire_events()
    return {"event": events}

@app.get("/fire-damage", tags=["Damage"])
def get_damage_rate(
    lat: float = Query(..., description="위도"),
    lon: float = Query(..., description="경도")
):
    damage = analyze_fire_damage_ratio(lat, lon)
    return {
        "lat": lat,
        "lon": lon,
        "damage": round(damage, 2)
    }

@app.get("/ndvi-recovery", tags=["Recovery"])
def get_recovery_rate(
    lat: float = Query(..., description="위도"),
    lon: float = Query(..., description="경도")
):
    recovery = predict_recovery_rate(lat, lon)
    return {
        "lat": lat,
        "lon": lon,
        "recovery": recovery
    }

@app.get("/vegetation", tags=["Vegetation"])
def get_vegetation_report(
    lat: float = Query(..., description="위도"),
    lon: float = Query(..., description="경도")
):
    ndvi_value = get_ndvi_at_point(lat, lon, before_date=NDVI_BEFORE_DATE, after_date=NDVI_AFTER_DATE)
    if ndvi_value is None:
        raise HTTPException(status_code=400, detail="해당 위치에서 NDVI 값을 가져오지 못했습니다.")
    
    vegetation = vegetation_at_point(lat, lon, ndvi_value)
    return {
        "lat": lat,
        "lon": lon,
        "ndvi": round(ndvi_value, 3),
        **vegetation
    }