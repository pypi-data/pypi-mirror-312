import requests
from typing import Literal

def request_api(api_url, api_key=None, method:Literal["post","get"]="get",**kwargs):
    """
    Fetches data from an API.

    Args:
        api_url (str): The URL of the API endpoint.
        token (str, optional): Authentication token for the API (if required).
        **kwargs: Additional parameters to be passed to the API.

    Returns:
        dict: The response data from the API as a dictionary, or None if an error occurs.
    """
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    try:
        if method == "get":
            response = requests.get(api_url, headers=headers, params=kwargs)
        else:
            response = requests.post(api_url, headers=headers, params=kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None