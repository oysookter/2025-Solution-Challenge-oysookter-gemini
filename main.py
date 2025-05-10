from fastapi import FastAPI, Query
from gee.auth import init_gee
from gee.fire_damage import analyze_fire_damage_ratio           # 산불 피해 비율
from gee.fire_event import get_forest_fire_events               # 산불 발생 데이터 ( Open API )
from gee.recovery_rate import predict_recovery_rate             # 회복 비율 계산
from gee.ndvi_point import get_ndvi_at_point                    # 1km 반경 내 ndvi 수치 평균 계산
from gemini.ndvi_analysis import vegetation_at_point            # 식생 상태 분석 프롬프트

app = FastAPI()

# 임시 날짜 데이터 ( 240301 - 240401 ) 
before_date = "2024-03-01"
after_date = "2024-04-01"

# GEE 초기화는 앱 시작 시 1회
init_gee()

@app.get("/")
def root():
    return {"message": "🌲 산불 복구 서비스에 오신 것을 환영합니다."}

@app.get("/data", tags=["Fire"])
def get_fire_event_data():
    recovery = get_forest_fire_events()
    return {
        "event": recovery
    }
    
@app.get("/damage", tags=["Damage"])
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

@app.get("/recovery", tags=["Recovery"])
def get_recovery_date(
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
    lat: float = Query(...), 
    lon: float = Query(...)
):
    ndvi_value = get_ndvi_at_point(lat, lon, before_date=before_date, after_date=after_date)
    if ndvi_value is None:
        return {"error": "해당 위치에서 NDVI 값을 가져오지 못했습니다."}
    
    explanation = vegetation_at_point(lat, lon, ndvi_value)
    return {
        "lat": lat,
        "lon": lon,
        "ndvi": round(ndvi_value, 3),
        "explanation": explanation
    }
