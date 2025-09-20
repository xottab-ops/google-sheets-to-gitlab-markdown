import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class GoogleClient:
    def __init__(self, spreadsheet_id: str, credentials: dict):
        """
        spreadsheet_id : str
            ID Google Sheets
        credentials : dict
            JSON-ключ сервисного аккаунта (как dict, не файл!)
        """
        self.spreadsheet_id = spreadsheet_id

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.metadata.readonly",
        ]
        creds = Credentials.from_service_account_info(credentials, scopes=scopes)
        self.gc = gspread.authorize(creds)
        self.drive_service = build("drive", "v3", credentials=creds)

    def fetch_data(self) -> str:
        """Собирает все таблицы в markdown"""
        sh = self.gc.open_by_key(self.spreadsheet_id)
        all_tables = []

        for worksheet in sh.worksheets():
            values = worksheet.get_all_values()
            if not values:
                continue

            df = pd.DataFrame(values[1:], columns=values[0])
            markdown = df.to_markdown(index=False, tablefmt="github")
            all_tables.append(f"## {worksheet.title}\n\n{markdown}\n")

        return "\n\n".join(all_tables)

    def get_last_update(self) -> str:
        """Возвращает ISO-время последнего обновления"""
        file = self.drive_service.files().get(
            fileId=self.spreadsheet_id,
            fields="modifiedTime"
        ).execute()
        return file["modifiedTime"]
