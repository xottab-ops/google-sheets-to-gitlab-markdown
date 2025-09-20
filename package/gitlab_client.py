import gitlab


class GitLabClient:
    def __init__(self, url: str, token: str, project_id: int, output_file: str,
                 branch: str = "master", commit_message: str = "Update stats"):
        self.branch = branch
        self.commit_message = commit_message
        self.output_file = output_file

        self.gl = gitlab.Gitlab(url, private_token=token)
        self.project = self.gl.projects.get(project_id)

    def upload(self, content: str):
        """Создать/обновить файл"""
        try:
            f = self.project.files.get(file_path=self.output_file, ref=self.branch)
            f.content = content
            f.save(branch=self.branch, commit_message=self.commit_message)
        except gitlab.exceptions.GitlabGetError:
            self.project.files.create({
                "file_path": self.output_file,
                "branch": self.branch,
                "content": content,
                "commit_message": self.commit_message
            })