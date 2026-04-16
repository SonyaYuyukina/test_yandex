import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

BASE_URL = "https://cloud-api.yandex.net/v1/disk"
TEST_FILES_DIR = "tests/test_files/"

OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")

if not OAUTH_TOKEN:
    raise ValueError("Токен не найден")
