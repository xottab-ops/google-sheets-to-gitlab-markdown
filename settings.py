import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")


class Config:
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "example")
    GITLAB_URL = os.getenv("GITLAB_URL", "example")
    GITLAB_PROJECT_ID = int(os.getenv("GITLAB_PROJECT_ID", "12345678"))
    OUTPUT_FILE = os.getenv("OUTPUT_FILE", "README.MD")
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "600"))  # in seconds
    GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "example_token")