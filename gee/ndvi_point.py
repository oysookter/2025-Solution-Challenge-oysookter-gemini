import ee

def get_ndvi_at_point(lat: float, lon: float, before_date: str, after_date: str):
    try:
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(1000)  # 1km 반경

        collection = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterBounds(region) \
            .filterDate(before_date, after_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))  # 선택적으로 구름도 제거

        def mask_water(image):
            scl = image.select("SCL")
            water_mask = scl.neq(6)  # SCL 값이 6(물)이 아닌 영역만 남김
            return image.updateMask(water_mask)

        collection = collection.map(mask_water)
        image = collection.median()

        ndvi = image.normalizedDifference(['B8', 'B4']).rename("NDVI")

        value = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=30
        ).get("NDVI")

        return value.getInfo()

    except Exception as e:
        print(f"NDVI 계산 오류: {e}")
        return None