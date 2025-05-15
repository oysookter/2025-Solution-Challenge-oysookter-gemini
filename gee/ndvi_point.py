import ee

def get_ndvi_at_point(lat: float, lon: float, before_date: str, after_date: str):
    try:
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(1000)  # 1km boundary

        collection = ee.ImageCollection("COPERNICUS/S2") \
            .filterBounds(region) \
            .filterDate(before_date, after_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))  # Optionally remove clouds

        def mask_water(image):
            scl = image.select("SCL")
            water_mask = scl.neq(6)  # Except water
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
        print(f"NDVI Calc Error: {e}")
        return None