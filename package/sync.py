import time
from datetime import datetime, timedelta, timezone
from .google_client import GoogleClient
from .gitlab_client import GitLabClient


class SyncService:
    def __init__(self,
                 spreadsheet_id: str,
                 credentials: dict,
                 gitlab_url: str,
                 gitlab_token: str,
                 gitlab_project_id: int,
                 output_file: str,
                 check_interval: int = 600,
                 branch: str = "master",
                 commit_message: str = "Update stats"):
        """
        credentials : dict
            JSON-ключ сервисного аккаунта (в виде dict)
        """
        self.google = GoogleClient(spreadsheet_id, credentials)
        self.gitlab = GitLabClient(
            url=gitlab_url,
            token=gitlab_token,
            project_id=gitlab_project_id,
            output_file=output_file,
            branch=branch,
            commit_message=commit_message
        )
        self.check_interval = check_interval
        self.last_check = datetime.now(timezone.utc) - timedelta(minutes=11)
        self.last_update = datetime.now(timezone.utc) - timedelta(minutes=check_interval)

    def run_once(self):
        """Выполнить одну синхронизацию"""
        updated_dt = datetime.fromisoformat(
            self.google.get_last_update().replace("Z", "+00:00")
        )

        print(f"[INFO] Last check: {self.last_check.isoformat()}")
        print(f"[INFO] Sheet updated: {updated_dt.isoformat()}")

        if updated_dt > self.last_update:
            print("[INFO] Найдены изменения, обновляем...")
            content = self.google.fetch_data()
            self.gitlab.upload(content)
            self.last_check = datetime.now(timezone.utc)
            print(f"[INFO] Файл обновлён в GitLab. Новое время last_check: {self.last_check.isoformat()}")
        else:
            print("[INFO] Изменений нет.")

    def run_forever(self):
        """Запускать синхронизацию в цикле"""
        while True:
            self.run_once()
            time.sleep(self.check_interval)
