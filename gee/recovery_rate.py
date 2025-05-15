from gee.ndvi_point import get_ndvi_at_point
from utils.constants import NDVI_DATE_RANGES

def predict_recovery_rate(lat: float, lon: float):
    try:       
        pre_start, pre_end = NDVI_DATE_RANGES["pre"]
        min_start, min_end = NDVI_DATE_RANGES["min"]
        now_start, now_end = NDVI_DATE_RANGES["now"]
    
        # NDVI calc
        ndvi_pre = get_ndvi_at_point(lat, lon, pre_start, pre_end)
        ndvi_min = get_ndvi_at_point(lat, lon, min_start, min_end)
        ndvi_now = get_ndvi_at_point(lat, lon, now_start, now_end)

        # None check
        if None in (ndvi_pre, ndvi_min, ndvi_now):
            raise ValueError("NDVI values could not be calculated.")

        # Recovery rate calc
        if ndvi_pre == ndvi_min:
            recovery_rate = 0.0
        else:
            recovery_rate = (ndvi_now - ndvi_min) / (ndvi_pre - ndvi_min) * 100
            recovery_rate = max(0, min(recovery_rate, 100))  # 0~100 limit

        # explanation
        if ndvi_now < ndvi_min:
            status = "Worsening"
        elif recovery_rate < 30:
            status = "In Recovery"
        elif recovery_rate < 80:
            status = "Partial Recovery"
        else:
            status = "Almost Recovered"

        return {
            "ndvi_pre": round(ndvi_pre, 3),
            "ndvi_min": round(ndvi_min, 3),
            "ndvi_now": round(ndvi_now, 3),
            "recovery_rate": round(recovery_rate, 2),
            "status": status
        }

    except Exception as e:
        print(f"Recovery Prediction Rate Calc Error: {e}")
        return None