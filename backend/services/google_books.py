import requests

def search_books(query: str):
    """
    Searches for books using the Google Books API.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
    
    data = response.json()
    books = []
    
    if "items" in data:
        for item in data["items"]:
            volume_info = item.get("volumeInfo", {})
            books.append({
                "google_id": item.get("id"),
                "title": volume_info.get("title", "Unknown Title"),
                "author": ", ".join(volume_info.get("authors", ["Unknown Author"])),
                "description": volume_info.get("description", "No description available."),
                "published": True # Simplified
            })
            
    return books
