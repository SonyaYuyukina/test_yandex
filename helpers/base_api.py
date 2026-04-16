import requests
import time
from config import OAUTH_TOKEN, BASE_URL

class BaseApi:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {
            "Authorization": f"OAuth {OAUTH_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _send_request(self, method, endpoint, **kwargs):
        url = f'{self.base_url}{endpoint}'
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response

    def get_request(self, endpoint, **kwargs):
        return self._send_request('GET', endpoint, **kwargs)

    def post_request(self, endpoint, **kwargs):
        return self._send_request('POST', endpoint, **kwargs)

    def put_request(self, endpoint, **kwargs):
        return self._send_request('PUT', endpoint, **kwargs)

    def delete_request(self, endpoint, **kwargs):
        return self._send_request('DELETE', endpoint, **kwargs)

    def wait_for_operation(self, operation_url, timeout=30, interval=1):
        for i in range(timeout):
            operation_response = self.get_request(operation_url.replace(self.base_url, ""))
            if operation_response.status_code == 200:
                status = operation_response.json().get("status")
                if status != "in-progress":
                    return status == 'success'
            time.sleep(interval)