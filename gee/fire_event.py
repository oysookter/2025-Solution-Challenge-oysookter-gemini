import os
import requests
from dotenv import load_dotenv
import xmltodict

# 240301 - 240401
def get_forest_fire_events():
    load_dotenv()
    service_key = os.getenv("OPEN_API_KEY")

    url = "http://apis.data.go.kr/1400000/forestStusService/getfirestatsservice"
    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": "10",
        "searchStDt": "20240301",
        "searchEdDt": "20240401"
    }

    response = requests.get(url, params=params)
    fire_data = response.content

    # XML → dict
    inner_json = xmltodict.parse(fire_data)

    # Direct access from the dict (items['item'])
    items = inner_json['response']['body']['items']['item']
    fires = []

    # Treat a single item as a list
    if isinstance(items, dict):
        items = [items]

    for item in items:
        try:
            date = f"{item.get('startyear', '0000')}-{item.get('startmonth', '01').zfill(2)}-{item.get('startday', '01').zfill(2)}"
            area = float(item.get("damagearea") or 0.0)
            cause = item.get("firecause", "미상")

            # Safe address part extraction
            locsi = item.get("locsi", "")
            locgungu = item.get("locgungu", "")
            locmenu = item.get("locmenu", "")
            locdong = item.get("locdong", "")
            locbunji = item.get("locbunji", "")

            # Assembling addresses
            parts = [locsi, locgungu]
            if locmenu and locmenu != locgungu:
                parts.append(locmenu)
            parts.extend([locdong, locbunji])
            address = ' '.join(filter(None, parts))  # Except blank

            fires.append({
                "date": date,
                "area": area,
                "cause": cause,
                "address": address
            })

        except Exception as e:
            print(f"⚠️ Item Processing Error: {e}")
            continue
    return fires