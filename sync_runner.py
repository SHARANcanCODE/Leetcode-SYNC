import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from leetcode_sync.config import Config
from leetcode_sync.leetcode_api import LeetCodeAPI
from leetcode_sync.file_manager import FileManager
from leetcode_sync.git_manager import GitManager
from leetcode_sync.scheduler import Scheduler

def sync_submissions():
    print("Starting LeetCode submissions sync...")
    base_path = Config.get_github_repo_path()
    api = LeetCodeAPI()
    fm = FileManager(base_path)

    # We fetch first 50 accepted submissions only; can extend later with pagination
    submissions = api.fetch_accepted_submissions(limit=50, offset=0)
    print(f"Fetched {len(submissions)} accepted submissions.")

    # Save all submissions, track files and per-folder submissions for README
    folder_map = {}
    for sub in submissions:
        file_path = fm.save_submission(sub)
        folder = Path(file_path).parent
        folder_map.setdefault(folder, []).append(sub)

    # Generate README.md per folder
    for folder, subs in folder_map.items():
        fm.generate_readme_in_folder(str(folder), subs)

    # Commit and push changes to git
    gm = GitManager(base_path)
    gm.commit_and_push()

def main():
    sync_interval = Config.get_sync_interval_minutes()
    scheduler = Scheduler(sync_interval, sync_submissions)
    scheduler.start()

    print("LeetCode Sync Tool running. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting LeetCode Sync Tool.")

if __name__ == "__main__":
    main()
