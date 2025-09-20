import gitlab
from .logger import get_logger


class GitLabClient:
    """
    A client for interacting with a GitLab project and uploading files.
    """

    def __init__(self, url: str, token: str, project_id: int,
                 output_file: str, branch: str = "master",
                 commit_message: str = "Update stats") -> None:
        self.branch = branch
        self.commit_message = commit_message
        self.output_file = output_file
        self.logger = get_logger(self.__class__.__name__)

        self.gl = gitlab.Gitlab(url, private_token=token)
        self.project = self.gl.projects.get(project_id)

    def upload(self, content: str) -> None:
        """
        Create or update a file in the GitLab repository.
        """
        try:
            f = self.project.files.get(file_path=self.output_file, ref=self.branch)
            f.content = content
            f.save(branch=self.branch, commit_message=self.commit_message)
            self.logger.info("File '%s' updated in GitLab.", self.output_file)
        except gitlab.exceptions.GitlabGetError:
            self.project.files.create({
                "file_path": self.output_file,
                "branch": self.branch,
                "content": content,
                "commit_message": self.commit_message
            })
            self.logger.info("File '%s' created in GitLab.", self.output_file)
