import os

class Config:
    """
    Manages configuration and secrets for LeetCode Sync Tool, read from environment variables.
    Avoids hardcoding sensitive info.
    """

    @staticmethod
    def get_leetcode_session():
        """
        LeetCode session cookie value.
        """
        value = os.getenv("LEETCODE_SESSION")
        if not value:
            raise ValueError("LEETCODE_SESSION not set in environment variables")
        return value

    @staticmethod
    def get_csrf_token():
        """
        CSRF token required for LeetCode GraphQL queries, usually found as csrftoken cookie.
        """
        value = os.getenv("LEETCODE_CSRF_TOKEN")
        if not value:
            raise ValueError("LEETCODE_CSRF_TOKEN not set in environment variables")
        return value

    @staticmethod
    def get_github_repo_path():
        """
        Local path to the git repo for saving submissions.
        """
        value = os.getenv("GITHUB_REPO_PATH", "./leetcode_submissions")
        return value

    @staticmethod
    def get_sync_interval_minutes():
        """
        Sync interval in minutes, for scheduling.
        Default: 1440 (one day)
        """
        return int(os.getenv("SYNC_INTERVAL_MINUTES", "1440"))
