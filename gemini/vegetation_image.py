import requests

def search_image_url_wikimedia(query: str) -> str | None:
    """
    Searches Wikimedia for the first image of the plant based on scientific name.
    Returns the image URL or None if not found.
    """
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
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]
        return None
    except Exception as e:
        print(f"[🌐 image search error] '{query}': {e}")
        return None