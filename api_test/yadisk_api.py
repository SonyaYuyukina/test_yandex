from tokenize import endpats

from api_test.base_api import BaseApi
import requests
import time

class YaDiskAPI(BaseApi):
    def create_folder_request(self, folder_path):
        endpoint = "/resources"
        params = {"path": folder_path}
        response = self.put_request(endpoint, params=params)
        return response

    def get_folder_content_request(self, folder_path):
        endpoint = "/resources"
        params = {"path": folder_path}
        response = self.get_request(endpoint, params=params)
        return response

    def upload_file_request(self, folder_path, file_path):
        endpoint = "/resources/upload"
        params = {"path": folder_path}
        response = self.get_request(endpoint, params=params)
        upload_url = response.json().get("href")
        with open(file_path, 'rb') as f:
            upload_response = requests.put(upload_url, files={"file": f})
        return upload_response

    def delete_file_or_folder_request(self, path_to_delete, is_permanent):
        endpoint = "/resources"
        params = {"path": path_to_delete, "permanently": is_permanent}
        response = self.delete_request(endpoint, params=params)
        if response.status_code == 202:
            operation_url = response.json().get("href")
            if operation_url:
                for i in range(30):
                    time.sleep(1)
                    operation_response = self.get_request(operation_url.replace(self.base_url, ""))
                    if operation_response.status_code == 200:
                        status = operation_response.json().get("status")
                        if status != "in-progress":
                            return status == 'success'
        return response.status_code == 204

    def get_trash_content_request(self, folder_path):
        endpoint = "/trash/resources"
        params = {"path": folder_path}
        response = self.get_request(endpoint, params=params)
        return response

    def restore_file_from_trash_request(self, file_name):
        endpoint = "/trash/resources/restore"
        params = {"path": {file_name}}
        response = self.put_request(endpoint, params=params)
        if response.status_code == 202:
            operation_url = response.json().get("href")
            if operation_url:
                for i in range(30):
                    time.sleep(1)
                    operation_response = self.get_request(operation_url.replace(self.base_url, ""))
                    if operation_response.status_code == 200:
                        status = operation_response.json().get("status")
                        if status != "in-progress":
                            return status == 'success'
        return response.status_code == 201
