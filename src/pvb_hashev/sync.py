import time
from datetime import datetime, timedelta, timezone
from .google_client import GoogleClient
from .gitlab_client import GitLabClient
from .logger import get_logger


class SyncService:
    """
    A service that synchronizes Google Sheets content with a GitLab repository.
    """

    def __init__(self,
                 spreadsheet_id: str,
                 credentials: dict,
                 gitlab_url: str,
                 gitlab_token: str,
                 gitlab_project_id: int,
                 output_file: str,
                 check_interval: int = 600,
                 branch: str = "master",
                 commit_message: str = "Update stats") -> None:
        """
        Parameters
        ----------
        spreadsheet_id : str
            Google Sheets document ID.
        credentials : dict
            Service account JSON key as a Python dictionary.
        gitlab_url : str
            GitLab instance URL.
        gitlab_token : str
            GitLab personal access token.
        gitlab_project_id : int
            Target GitLab project ID.
        output_file : str
            Path to the file in the GitLab repository.
        check_interval : int, optional
            Interval between checks (in seconds). Default is 600.
        branch : str, optional
            Target Git branch. Default is "master".
        commit_message : str, optional
            Commit message for updates. Default is "Update stats".
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
        self.last_update = datetime.fromisoformat("1900-01-01T00:00:00+00:00")
        self.logger = get_logger(self.__class__.__name__)

    def run_once(self) -> None:
        """
        Run a single synchronization cycle.
        """

        updated_dt = datetime.fromisoformat(
            self.google.get_last_update().replace("Z", "+00:00")
        )

        self.logger.info("Last check: %s", self.last_check.isoformat())
        self.logger.info("Sheet updated: %s", updated_dt.isoformat())

        if updated_dt > self.last_update:
            self.logger.info("Changes detected, updating GitLab...")
            content = self.google.fetch_data()
            self.gitlab.upload(content)

            self.last_update = datetime.now(timezone.utc)
            self.logger.info("File updated in GitLab. New last_update: %s", self.last_update.isoformat())
        else:
            self.logger.info("No changes detected.")

        self.last_check = datetime.now(timezone.utc)

    def run_forever(self) -> None:
        """
        Continuously run synchronization in a loop.
        """
        self.logger.info("Starting continuous sync with interval %d seconds.", self.check_interval)
        while True:
            self.run_once()
            time.sleep(self.check_interval)
