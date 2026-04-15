import pytest

TEST_FOLDER_NAME = "pytest_test_folder_1234"
TEST_FILES_PATH = "tests/test_files/"
TEST_FILE_NAME = "text_file.txt"

def create_folder(api, folder_name):
    create_result = api.create_folder_request(folder_name)
    assert create_result.status_code == 201, "Не удалось создать папку"

def check_if_folder_exists(api, folder_name):
    content = api.get_folder_content_request("/").json()
    items = content.get("_embedded", {}).get("items", [])
    folder_names = [item["name"] for item in items if item["type"] == "dir"]
    assert folder_name in folder_names, "Созданная папка не найдена в корне диска"

def delete_folder(api, folder_name):
    delete_result = api.delete_file_or_folder_request(f"/{folder_name}", "true")
    assert delete_result, "Не удалось удалить папку"
    with pytest.raises(Exception) as e:
        api.get_folder_content_request(f"/{folder_name}")
    assert "404" in str(e.value), f"При поиске удаленной папки ожидалась ошибка 404, получили: {e.value}"

def upload_file(api, file_name):
    upload_result = api.upload_file_request(f"/{file_name}", f"{TEST_FILES_PATH}{file_name}")
    assert upload_result.status_code == 201, "Не удалось загрузить файл"

def check_if_file_exists(api, file_name):
    content = api.get_folder_content_request("/").json()
    items = content.get("_embedded", {}).get("items", [])
    file_names = [item["name"] for item in items if item["type"] == "file"]
    assert file_name in file_names, f"Файл {file_name} не найден. Найдены файлы: {file_names}"

def delete_file(api, file_name, is_permanent="true"):
    yadisk_path = f"/{file_name}"
    delete_result = api.delete_file_or_folder_request(yadisk_path, is_permanent)
    assert delete_result, "Не удалось удалить файл"

class TestYandexDiskAPI():
    @pytest.mark.collection
    @pytest.mark.create_and_delete_folder
    def test_create_and_delete_folder(self, api):
        create_folder(api, TEST_FOLDER_NAME)
        check_if_folder_exists(api, TEST_FOLDER_NAME)

        with pytest.raises(Exception) as e:
            api.create_folder_request(TEST_FOLDER_NAME)
        assert "409" in str(e.value), f"При создании папки с тем же именем ожидалась ошибка 409, получили: {e.value}"

        delete_folder(api, TEST_FOLDER_NAME)

    @pytest.mark.collection
    @pytest.mark.upload_and_delete_file
    @pytest.mark.parametrize("file_name", ["text_file.txt", "image.jpg"])
    def test_upload_and_delete_file(self, api, file_name):
        upload_file(api, file_name)
        check_if_file_exists(api, file_name)

        with pytest.raises(Exception) as e:
            api.upload_file_request(f"/{file_name}", file_name)
        assert "409" in str(e.value), f"При загрузке файла с тем же именем ожидалась ошибка 409, получили: {e.value}"

        delete_file(api, file_name)

    @pytest.mark.collection
    @pytest.mark.trash_delete_and_restore
    def test_trash_delete_and_restore(self, api):
        upload_file(api, TEST_FILE_NAME)
        check_if_file_exists(api, TEST_FILE_NAME)
        delete_file(api, TEST_FILE_NAME, is_permanent="false")

        trash_content = api.get_trash_content_request("/").json()
        items = trash_content.get("_embedded", {}).get("items", [])
        file_names = [item["name"] for item in items if item["type"] == "file"]
        assert TEST_FILE_NAME in file_names, f"Файл {TEST_FILE_NAME} не найден в корзине. Найдены файлы: {file_names}"

        #TODO: вытащить название файла и удалить по нему
        #api.restore_file_from_trash_request(TEST_FILE_NAME)
        #check_if_file_exists(api, TEST_FILE_NAME)









    #TODO: тест корзины - в загрузку файла - текст + картинка, в создание папок - на разных языках?,удаление, очистка, восстановление; тест перемещения файла; улучшить обработку ошибок - добавить try except везде, добавить аллюр для визуализации?