import os
import time
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import gitlab
from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from settings import Config

# ==== Настройки ====
SPREADSHEET_ID = Config.SPREADSHEET_ID
GITLAB_URL = Config.GITLAB_URL
GITLAB_PROJECT_ID = Config.GITLAB_PROJECT_ID
OUTPUT_FILE = Config.OUTPUT_FILE
CHECK_INTERVAL = Config.CHECK_INTERVAL
GOOGLE_CREDENTIALS_FILE = Config.GOOGLE_CREDENTIALS_FILE
GITLAB_TOKEN = Config.GITLAB_TOKEN

# ==== Авторизация в Google Sheets ====
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]
creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)
drive_service = build("drive", "v3", credentials=creds)

# ==== Авторизация в GitLab ====
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
project = gl.projects.get(GITLAB_PROJECT_ID)

# ==== Храним время последней проверки ====
last_check = datetime.now(timezone.utc) - timedelta(minutes=11)

def fetch_data():
    """Забираем данные со всех листов"""
    sh = gc.open_by_key(SPREADSHEET_ID)
    all_tables = []

    for worksheet in sh.worksheets():
        values = worksheet.get_all_values()
        if not values:
            continue

        df = pd.DataFrame(values[1:], columns=values[0])  # первая строка = заголовки
        markdown = df.to_markdown(index=False, tablefmt="github")

        table_md = f"## {worksheet.title}\n\n{markdown}\n"
        all_tables.append(table_md)

    return "\n\n".join(all_tables)


def upload_to_gitlab(content: str):
    """Загрузка markdown файла в GitLab"""
    try:
        f = project.files.get(file_path=OUTPUT_FILE, ref="master")
        f.content = content
        f.save(branch="master", commit_message="Change statistics")
    except gitlab.exceptions.GitlabGetError:
        project.files.create({
            "file_path": OUTPUT_FILE,
            "branch": "master",
            "content": content,
            "commit_message": "Change stats"
        })


def check_updates():
    global last_check

    # получаем метаданные из Google Drive API
    file = drive_service.files().get(
        fileId=SPREADSHEET_ID,
        fields="modifiedTime"
    ).execute()

    updated_dt = datetime.fromisoformat(file["modifiedTime"].replace("Z", "+00:00"))

    print(f"[INFO] Last check: {last_check.isoformat()}")
    print(f"[INFO] Sheet updated: {updated_dt.isoformat()}")

    if updated_dt > last_check:
        print("[INFO] Найдены изменения, обновляем...")
        content = fetch_data()
        upload_to_gitlab(content)
        last_check = datetime.now(timezone.utc)
        print(f"[INFO] Файл обновлён в GitLab. Новое время last_check: {last_check.isoformat()}")
    else:
        print("[INFO] Изменений нет.")


if __name__ == "__main__":
    while True:
        check_updates()
        time.sleep(CHECK_INTERVAL)