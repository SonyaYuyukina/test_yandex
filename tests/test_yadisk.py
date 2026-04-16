import pytest
import requests.exceptions

class TestYandexDiskAPI:
    @pytest.mark.collection
    @pytest.mark.create_and_delete_folder
    @pytest.mark.parametrize("folder_name", ["test_folder"])
    def test_create_and_delete_folder(self, api, actions, cleanup, folder_name):
        actions.create_folder(api, folder_name)
        cleanup["content"].append(folder_name)
        actions.check_if_folder_exists(api, folder_name)

        with pytest.raises(requests.exceptions.HTTPError) as e:
            api.create_folder_request(folder_name)
        assert e.value.response.status_code == 409, f"При создании папки с тем же именем ожидалась ошибка 409, получили: {e.value}"

        actions.delete_folder(api, folder_name)

    @pytest.mark.collection
    @pytest.mark.upload_and_delete_file
    @pytest.mark.parametrize("file_name", ["text_file.txt", "image.jpg"])
    def test_upload_and_delete_file(self, api, actions, file_name, cleanup):
        actions.upload_file(api, file_name)
        cleanup["content"].append(file_name)
        actions.check_if_file_exists(api, file_name)

        with pytest.raises(requests.exceptions.HTTPError) as e:
            api.upload_file_request(f"/{file_name}", file_name)
        assert e.value.response.status_code == 409, f"При загрузке файла с тем же именем ожидалась ошибка 409, получили: {e.value}"

        actions.delete_file(api, file_name)

    @pytest.mark.collection
    @pytest.mark.trash_delete_and_restore
    @pytest.mark.parametrize("file_name", ["text_file.txt"])
    def test_trash_delete_and_restore(self, api, actions, cleanup, file_name):
        actions.upload_file(api, file_name)
        cleanup["content"].append(file_name)
        actions.check_if_file_exists(api, file_name)
        actions.delete_file(api, file_name, is_permanent="false")

        trash_content = api.get_trash_content_request("/").json()
        items = trash_content.get("_embedded", {}).get("items", [])
        file_names = [item["name"] for item in items if item["type"] == "file"]
        assert file_name in file_names, f"Файл {file_name} не найден в корзине. Найдены файлы: {file_names}"

        for item in items:
            if item["type"] == "file" and item["name"] == file_name:
                restore_path = item["path"].replace("trash:/", "")
                api.restore_file_from_trash_request(restore_path)
                break

        actions.check_if_file_exists(api, file_name)

    @pytest.mark.collection
    @pytest.mark.replace_file
    @pytest.mark.parametrize("file_name, folder_name", [("text_file.txt", "test_folder")])
    def test_replace_file(self, api, actions, file_name, folder_name, cleanup):
        actions.upload_file(api, file_name)
        cleanup["content"].append(file_name)
        actions.check_if_file_exists(api, file_name)
        actions.create_folder(api, folder_name)
        cleanup["content"].append(folder_name)
        actions.check_if_folder_exists(api, folder_name)
        actions.move_file(api, folder_name, file_name)
        actions.check_if_file_exists(api, file_name, folder_name)