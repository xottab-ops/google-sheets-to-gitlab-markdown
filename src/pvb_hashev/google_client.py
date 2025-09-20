import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .logger import get_logger


class GoogleClient:
    """
    A client for fetching data and metadata from Google Sheets.
    """

    def __init__(self, spreadsheet_id: str, credentials: dict) -> None:
        """
        Parameters
        ----------
        spreadsheet_id : str
            Google Sheets document ID.
        credentials : dict
            Service account JSON key as a Python dictionary (not a file).
        """
        self.spreadsheet_id = spreadsheet_id
        self.logger = get_logger(self.__class__.__name__)

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.metadata.readonly",
        ]
        creds = Credentials.from_service_account_info(credentials, scopes=scopes)
        self.gc = gspread.authorize(creds)
        self.drive_service = build("drive", "v3", credentials=creds)

    def fetch_data(self) -> str:
        """
        Collect all worksheets and return their content as Markdown tables.
        """
        sh = self.gc.open_by_key(self.spreadsheet_id)
        all_tables = []

        for worksheet in sh.worksheets():
            values = worksheet.get_all_values()
            if not values:
                continue

            df = pd.DataFrame(values[1:], columns=values[0])
            markdown = df.to_markdown(index=False, tablefmt="github")
            all_tables.append(f"## {worksheet.title}\n\n{markdown}\n")

        self.logger.info("Fetched %d worksheets from Google Sheets.", len(all_tables))
        return "\n\n".join(all_tables)

    def get_last_update(self) -> str:
        """
        Get the ISO timestamp of the last update of the spreadsheet.
        """
        file = self.drive_service.files().get(
            fileId=self.spreadsheet_id,
            fields="modifiedTime"
        ).execute()
        return file["modifiedTime"]
