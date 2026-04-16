import pytest
from helpers.yadisk_api import YaDiskAPI
from helpers.steps import Actions

@pytest.fixture
def api():
    return YaDiskAPI()

@pytest.fixture
def actions():
    return Actions()

@pytest.fixture
def cleanup(api):
    created_content = []
    yield {
        "content": created_content,
    }
    for item in created_content:
        try:
            api.delete_file_or_folder_request(item, is_permanent="true")
        except Exception:
            pass
