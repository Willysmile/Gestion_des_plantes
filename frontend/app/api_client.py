import requests
from app.config import API_BASE_URL, API_TIMEOUT, DEBUG
from requests.exceptions import RequestException

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
    
    def get(self, endpoint: str):
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json(), None
        except RequestException as e:
            if DEBUG:
                print(f"API Error: {e}")
            return None, str(e)
    
    def health_check(self):
        data, error = self.get("/health")
        return error is None

api_client = APIClient()
