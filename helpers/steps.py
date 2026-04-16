import pytest
import requests
from config import TEST_FILES_DIR

class Actions:
    def create_folder(self, api, folder_name):
        create_result = api.create_folder_request(folder_name)
        assert create_result.status_code == 201, "Не удалось создать папку"

    def check_if_folder_exists(self, api, folder_name):
        content = api.get_folder_content_request("/").json()
        items = content.get("_embedded", {}).get("items", [])
        folder_names = [item["name"] for item in items if item["type"] == "dir"]
        assert folder_name in folder_names, "Созданная папка не найдена в корне диска"

    def delete_folder(self, api, folder_name):
        delete_result = api.delete_file_or_folder_request(f"/{folder_name}", "true")
        assert delete_result, "Не удалось удалить папку"
        with pytest.raises(requests.exceptions.HTTPError) as e:
            api.get_folder_content_request(f"/{folder_name}")
        assert e.value.response.status_code == 404, f"При поиске удаленной папки ожидалась ошибка 404, получили: {e.value}"

    def upload_file(self, api, file_name):
        upload_result = api.upload_file_request(f"/{file_name}", f"{TEST_FILES_DIR}{file_name}")
        assert upload_result.status_code == 201, "Не удалось загрузить файл"

    def check_if_file_exists(self, api, file_name, path="/"):
        content = api.get_folder_content_request(path).json()
        items = content.get("_embedded", {}).get("items", [])
        file_names = [item["name"] for item in items if item["type"] == "file"]
        assert file_name in file_names, f"Файл {file_name} не найден. Найдены файлы: {file_names}"

    def delete_file(self, api, file_name, is_permanent="true"):
        path = f"/{file_name}"
        delete_result = api.delete_file_or_folder_request(path, is_permanent)
        assert delete_result, "Не удалось удалить файл"

    def move_file(self, api, folder_name, file_name):
        path_to_move = f"/{folder_name}/{file_name}"
        move_result = api.move_file_request(path_to_move, file_name)
        assert move_result, "Не удалось переместить файл"