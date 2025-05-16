import requests
from typing import Optional

def search_image_url_wikimedia(query: str) -> Optional[str]:
    """
    Tries to fetch an image using exact title. If not found, falls back to search API.
    """
    def get_image_from_title(title: str) -> Optional[str]:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "piprop": "original",
            "titles": title
        }

        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]
        return None

    def get_image_from_search(query: str) -> Optional[str]:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "piprop": "original",
            "generator": "search",
            "gsrsearch": query,
            "gsrlimit": 1
        }

        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]
        return None

    try:
        # 우선 괄호 안 학명 추출
        clean_query = extract_scientific_name(query)

        image = get_image_from_title(clean_query)
        if image:
            return image

        print(f"[🔍 No exact match for '{clean_query}', trying search fallback]")
        return get_image_from_search(clean_query)

    except Exception as e:
        print(f"[❗ Wikimedia API error] '{query}': {e}")
        return None