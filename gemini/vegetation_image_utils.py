# image_utils.py
import requests

def search_image_url_wikimedia(query: str) -> str | None:
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "piprop": "original",
        "titles": query
    }

    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        pages = data["query"]["pages"]
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]
    except Exception as e:
        print(f"[이미지 검색 오류] '{query}': {e}")
        return None