import os
from git import Repo, GitCommandError

class GitManager:
    """
    Automates git operations: add, commit, push.
    """

    def __init__(self, repo_path: str):
        if not os.path.exists(repo_path):
            raise FileNotFoundError(f"Git repo path does not exist: {repo_path}")
        self.repo_path = repo_path
        self.repo = Repo(repo_path)

    def commit_and_push(self, commit_message: str = "Sync LeetCode accepted submissions"):
        """
        Stage all changes, commit, and push to origin main/master branch.
        """
        try:
            self.repo.git.add(all=True)
            if self.repo.is_dirty(untracked_files=True):
                self.repo.index.commit(commit_message)
                origin = self.repo.remotes.origin
                origin.push()
                print("Changes committed and pushed successfully.")
            else:
                print("No changes to commit.")
        except GitCommandError as e:
            print(f"Git operation failed: {e}")
