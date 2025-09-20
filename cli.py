from package import SyncService
import json

def main():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    service = SyncService(
        spreadsheet_id="test",
        credentials=credentials,
        gitlab_url="https://gitlab.example.com",
        gitlab_token="gitlab-test-token",
        gitlab_project_id=67,
        output_file="VISIT_STATS.MD",
        check_interval=600,
        branch="master",
        commit_message="Sync from Google"
    )

    # Если нужно один раз:
    service.run_once()

    # Если нужен бесконечный цикл:
    # service.run_forever()


if __name__ == "__main__":
    main()