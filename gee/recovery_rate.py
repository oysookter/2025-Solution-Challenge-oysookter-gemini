from gee.ndvi_point import get_ndvi_at_point

def predict_recovery_rate(lat: float, lon: float):
    try:       
        # NDVI 계산
        ndvi_pre = get_ndvi_at_point(lat, lon, "2021-03-01", "2021-04-01")
        ndvi_min = get_ndvi_at_point(lat, lon, "2023-03-01", "2023-05-01")
        ndvi_now = get_ndvi_at_point(lat, lon, "2024-04-01", "2024-04-30")

        # 회복률 계산
        if ndvi_pre == ndvi_min:
            recovery_rate = 0.0
        else:
            recovery_rate = (ndvi_now - ndvi_min) / (ndvi_pre - ndvi_min) * 100
            recovery_rate = max(0, min(recovery_rate, 100))  # 0~100 사이 제한

        # 상태 해석 추가
        if ndvi_now < ndvi_min:
            status = "악화됨"
        elif recovery_rate < 30:
            status = "회복 중"
        elif recovery_rate < 80:
            status = "부분 회복"
        else:
            status = "거의 회복"

        return {
            "ndvi_pre": round(ndvi_pre, 3),
            "ndvi_min": round(ndvi_min, 3),
            "ndvi_now": round(ndvi_now, 3),
            "recovery_rate": round(recovery_rate, 2),
            "status": status
        }

    except Exception as e:
        print(f"회복 예측률 계산 오류: {e}")
        return None