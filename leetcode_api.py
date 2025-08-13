import requests
from typing import List, Dict
from .config import Config

class LeetCodeAPI:
    """
    Handles fetching accepted submissions of authenticated user from LeetCode GraphQL API.
    """

    GRAPHQL_URL = "https://leetcode.com/graphql"

    def __init__(self):
        # Create session with session cookie and CSRF token headers for auth
        self.session = requests.Session()
        self.session.cookies.set("LEETCODE_SESSION", Config.get_leetcode_session())
        self.session.cookies.set("csrftoken", Config.get_csrf_token())
        self.session.headers.update({
            "Referer": "https://leetcode.com",
            "x-csrftoken": Config.get_csrf_token(),
            "User-Agent": "LeetCode Sync Tool - Python"
        })

    def fetch_accepted_submissions(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        Fetches user's accepted submissions (limit and offset for pagination).
        Returns a list of submissions, each includes:
        - id, title, titleSlug, lang, code, difficulty, tags, submittedAt, url
        """
        query = """
        query userProfileSubmitRecords($limit: Int!, $offset: Int!) {
          submissionList(limit: $limit, offset: $offset, lastKey: null) {
            submissions {
              id
              title
              titleSlug
              lang
              status
              timestamp
              isPending
              url
              code
              __typename
            }
            hasNext
          }
          questionTopics(titleSlug: "", first: 100) {
            edges {
              node {
                name
                slug
              }
            }
          }
        }
        """

        # But this raw query does not yield details needed. Instead, we use a known query to get accepted submissions:
        graphql_query = '''
            query userProfileSubmissions($limit: Int!, $offset: Int!) {
              userStatus {
                username
              }
              submissionCalendar {
                streak
              }
              recentAcSubmissionList(limit: $limit) {
                id
                title
                titleSlug
                timestamp
                lang
                isPending
                __typename
              }
              allQuestionsCount {
                difficulty
                count
              }
              matchedUser(username: "") {
                submitStatsGlobal {
                  acSubmissionNum {
                    difficulty
                    count
                    submissions
                  }
                }
              }
            }
        '''

        # To fetch detailed accepted submissions, we will use a known approach:
        # We fetch from "https://leetcode.com/api/submissions/?offset=0&limit=50" which returns JSON with submissions.
        # This is simpler and supported by the web frontend.

        offset = offset
        limit = limit
        submissions_url = f"https://leetcode.com/api/submissions/?offset={offset}&limit={limit}&lastkey="

        resp = self.session.get(submissions_url)
        if resp.status_code != 200:
            raise ConnectionError(f"Failed to fetch submissions, status {resp.status_code}")

        data = resp.json()
        submissions = data.get("submissions_dump", [])

        # Filter accepted submissions and map relevant fields
        accepted_submissions = []
        for s in submissions:
            if s.get("status_display") == "Accepted":
                accepted_submissions.append({
                    "id": s.get("id"),
                    "title": s.get("title"),
                    "titleSlug": s.get("title_slug"),
                    "lang": s.get("lang"),
                    "timestamp": s.get("timestamp"),
                    "code": None,  # we will fetch code separately by submission id
                    "difficulty": None, # fetched later
                    "tags": [],       # fetched later
                    "url": f"https://leetcode.com/problems/{s.get('title_slug')}/"
                })

        # For each accepted submission, we fetch the code and metadata details
        for submission in accepted_submissions:
            submission_id = submission["id"]
            submission["code"] = self.fetch_submission_code(submission_id)
            # Fetch problem metadata like difficulty and tags
            metadata = self.fetch_problem_metadata(submission["titleSlug"])
            submission["difficulty"] = metadata.get("difficulty", "Unknown")
            submission["tags"] = metadata.get("tags", [])

        return accepted_submissions

    def fetch_submission_code(self, submission_id: int) -> str:
        """
        Fetch code content for a single submission by ID.
        This endpoint returns the raw code in response.
        """
        url = f"https://leetcode.com/submissions/detail/{submission_id}/check/"
        resp = self.session.get(url)
        if resp.status_code != 200:
            print(f"Warning: Failed to fetch code for submission {submission_id}")
            return ""
        # The website returns JSON with a 'code' key that holds submission code
        # but this API is behind auth, returns JSON
        try:
            data = resp.json()
            # The actual code is in the 'code' key of the 'submission' object sometimes
            # However, testing shows 'code' is present in 'submissions'
            return data.get("code", "")
        except Exception as e:
            print(f"Error parsing submission code json for {submission_id}: {e}")
            return ""

    def fetch_problem_metadata(self, title_slug: str) -> Dict:
        """
        Fetch problem metadata (difficulty, tags) from LeetCode public problem API
        """
        url = f"https://leetcode.com/graphql"
        query = """
          query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
              difficulty
              topicTags {
                name
                slug
              }
            }
          }
        """
        variables = {"titleSlug": title_slug}
        resp = self.session.post(url, json={"query": query, "variables": variables})
        if resp.status_code != 200:
            return {"difficulty": "Unknown", "tags": []}
        data = resp.json()
        question = data.get("data", {}).get("question", {})
        difficulty = question.get("difficulty") or "Unknown"
        tag_nodes = question.get("topicTags", [])
        tags = [tag.get("name") for tag in tag_nodes if tag.get("name")]
        return {"difficulty": difficulty, "tags": tags}
