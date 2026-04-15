import pytest
from api_test.yadisk_api import YaDiskAPI

@pytest.fixture
def api():
    return YaDiskAPI()

