import ee

def analyze_fire_damage_ratio(lat: float, lon: float):
    try:
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(10000)  # 10km boundary

        # Sentinel-2
        before = ee.ImageCollection("COPERNICUS/S2") \
            .filterBounds(region) \
            .filterDate("2021-03-01", "2021-04-01") \
            .median()

        after = ee.ImageCollection("COPERNICUS/S2") \
            .filterBounds(region) \
            .filterDate("2024-03-01", "2024-04-01") \
            .median()

        # NDVI calc
        ndvi_before = before.normalizedDifference(['B8', 'B4']).rename("ndvi_before")
        ndvi_after = after.normalizedDifference(['B8', 'B4']).rename("ndvi_after")
        ndvi_diff = ndvi_after.subtract(ndvi_before).rename("ndvi_diff")

        # damage masking (NDVI reduction <= -0.2)
        burned_mask = ndvi_diff.lt(-0.2)

        # pixel area
        pixel_area = ee.Image.pixelArea()

        # entire area
        total_area = pixel_area.reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=region,
            scale=30,
            maxPixels=1e9
        ).getInfo()["area"]

        # damage area
        burned_area = pixel_area.updateMask(burned_mask).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=region,
            scale=30,
            maxPixels=1e9
        ).getInfo()["area"]

        # damage rate calc (%)
        damage_ratio = (burned_area / total_area) * 100

        return round(damage_ratio, 2)
    
    except Exception as e:
        print(f"fire damage analysis error: {e}")
        return None