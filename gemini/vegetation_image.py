import requests
from typing import Optional

def search_image_url_wikimedia(query: str) -> Optional[str]:
    """
    Wikimedia API를 이용해 식물명에 해당하는 첫 번째 이미지 URL을 반환.
    영문 이름 또는 학명을 기준으로 검색합니다.
    """
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "piprop": "original",
        "titles": query.strip().title()
    }

    try:
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]
            else:
                print(f"[🔍 No image found for '{query}']")
    except requests.exceptions.RequestException as e:
        print(f"[❌ Wikimedia API error] '{query}': {e}")
    except Exception as e:
        print(f"[❗ Unexpected error] '{query}': {e}")

    return None