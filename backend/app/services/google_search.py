# app.services.google_search.py

import requests

def perform_search(query, api_key, cx):
    try:
        search_url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'q': query,
            'key': api_key,
            'cx': cx
        }
        
        response = requests.get(search_url, params=params)
        response.raise_for_status() # raises exception for http errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error: Request Exception while performing search: {e}")
        return {"error": "Search failed"}
    except Exception as e:
        print(f"Error: Exception while performing search: {e}")
        return {"error": "Search failed"}