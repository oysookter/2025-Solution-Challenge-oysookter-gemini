import ee

def get_ndvi_at_point(lat: float, lon: float, before_date: str, after_date: str):
    try:
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(1000)  # 1km boundary

        # Surface Reflectance + latest version
        collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
            .filterBounds(region) \
            .filterDate(before_date, after_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))  # Less clouds

        # masking function: earse waterSCL=6) 
        def mask_water(image):
            scl = image.select("SCL")
            water_mask = scl.neq(6)  # 6 = Water
            return image.updateMask(water_mask)

        collection = collection.map(mask_water)

        # calc median image
        image = collection.median()

        # calc NDVI (NIR - RED) / (NIR + RED)
        ndvi = image.normalizedDifference(['B8', 'B4']).rename("NDVI")

        # return NDVI average
        value = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=30
        ).get("NDVI")

        ndvi_value = value.getInfo()
        if ndvi_value is None:
            print(f"⚠️ NDVI is None at {lat}, {lon} during {before_date} ~ {after_date}")
            return None

        return ndvi_value

    except Exception as e:
        print(f"❌ NDVI Calc Error: {e}")
        return None