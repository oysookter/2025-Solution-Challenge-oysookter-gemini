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

    # 바로 dict에서 접근 (items['item']이 리스트)
    items = inner_json['response']['body']['items']['item']
    fires = []

    # 단일 item도 리스트로 처리
    if isinstance(items, dict):
        items = [items]

    for item in items:
        try:
            date = f"{item.get('startyear', '0000')}-{item.get('startmonth', '01').zfill(2)}-{item.get('startday', '01').zfill(2)}"
            area = float(item.get("damagearea") or 0.0)
            cause = item.get("firecause", "미상")

            # 안전한 주소 파트 추출
            locsi = item.get("locsi", "")
            locgungu = item.get("locgungu", "")
            locmenu = item.get("locmenu", "")
            locdong = item.get("locdong", "")
            locbunji = item.get("locbunji", "")

            # 주소 조립
            parts = [locsi, locgungu]
            if locmenu and locmenu != locgungu:
                parts.append(locmenu)
            parts.extend([locdong, locbunji])
            address = ' '.join(filter(None, parts))  # 빈 값 제외

            fires.append({
                "date": date,
                "area": area,
                "cause": cause,
                "address": address
            })

        except Exception as e:
            print(f"⚠️ 항목 처리 오류: {e}")
            continue
    return fires