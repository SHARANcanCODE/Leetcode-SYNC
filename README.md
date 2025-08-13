# LeetCode Sync Tool

## What is this project?

LeetCode Sync Tool is a Python-based automation project that:
- Fetches your accepted LeetCode submissions using LeetCode's web API with session authentication.
- Saves accepted solutions locally into a clean folder structure sorted by difficulty and problem tags.
- Automatically commits and pushes these changes to a GitHub repository.
- Supports scheduled periodic syncing (e.g., daily) to keep your local codebase and GitHub repo up-to-date.

## Use Case

This tool is ideal for developers who:
- Want to maintain an organized local backup of their LeetCode solutions.
- Want to showcase their data structures & algorithms (DSA) skills with real solved problems in a structured way on GitHub.
- Desire automation that integrates coding practice with GitHub portfolio updates without manual effort.

## How it Demonstrates Skills

- Deep integration with LeetCode's unofficial GraphQL API and web API.
- Uses Python for API interaction, data parsing, and file management.
- Automates Git using GitPython for commit and push workflows.
- Implements modular, clean, and scalable code architecture.
- Shows real-world tool-building and scheduling using Python scheduling libraries.
- Securely manages sensitive credentials via environment variables.

## How to Run

1. **Clone this repo locally**

git clone <repo-url>
cd LeetCodeSyncTool

2. **Setup environment variables**

Create a `.env` file or export the following variables (replace with your LeetCode browser cookies):

export LEETCODE_SESSION="your_leetcode_session_cookie"
export LEETCODE_CSRF_TOKEN="your_csrftoken_cookie"
export GITHUB_REPO_PATH="/path/to/local/git/repo"
export SYNC_INTERVAL_MINUTES=1440 # optional, default is daily


3. **Install dependencies**

python3 -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
pip install -r requirements.txt


4. **Initialize and run sync**

python scripts/sync_runner.py

The tool will fetch accepted submissions, save them locally, commit, and push changes to your GitHub repo. It will keep syncing periodically.

## GitHub Sync

- Local repo path specified by `GITHUB_REPO_PATH`.  
- The tool stages all changes, commits with a default message, and pushes to the remote origin.  
- Use your existing GitHub repository linked to the path or create a new one (see next section).  
- Git automation is powered by the GitPython library.

---

## Git Setup Instructions

### Initialize Git repo (run in VS Code terminal):

cd /path/to/your/leetcode_submissions
git init
git branch -M main
git add .
git commit -m "Initial commit"


### Create GitHub repo & push using GitHub CLI:

gh auth login # Login if not done already
gh repo create <repo-name> --public --source=. --remote=origin --push


This will create repo on GitHub, add remote, and push the initial commit.

---

## VS Code Terminal Setup Commands

python3 -m venv venv

Activate virtualenv (Linux/Mac)
source venv/bin/activate

Activate virtualenv (Windows PowerShell)
.\venv\Scripts\Activate.ps1

Install dependencies
pip install -r requirements.txt

Run the sync script
python scripts/sync_runner.py

---

This project provides a real-world productivity tool combining DSA problem solving, Python scripting, and GitHub automation, ideal to show in your portfolio or reference in your resume.



