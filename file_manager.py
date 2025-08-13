import os
import re
from typing import List, Dict

class FileManager:
    """
    Manages creating the folder structure and saving files.
    Sort by difficulty and tags.
    """

    def __init__(self, base_path: str):
        self.base_path = base_path

    def sanitize_filename(self, s: str) -> str:
        """
        Clean string to be a safe filename.
        """
        return re.sub(r'[\\/:"*?<>|]+', "", s)

    def get_extension(self, language: str) -> str:
        """
        Map submission language to file extension.
        Defaults to .txt if unknown.
        """
        mapping = {
            "python": "py",
            "python3": "py",
            "cpp": "cpp",
            "c++": "cpp",
            "java": "java",
            "javascript": "js",
            "typescript": "ts",
            "c": "c",
            "ruby": "rb",
            "swift": "swift",
            "go": "go",
            "scala": "scala",
            "kotlin": "kt",
            "rust": "rs",
            "php": "php",
        }
        ext = mapping.get(language.lower())
        return ext if ext else "txt"

    def save_submission(self, submission: Dict):
        """
        Save a single submission into the folder structure:
        base_path/difficulty/tag1_tag2/.../problem_title.ext
        """

        difficulty = submission.get("difficulty", "Unknown")
        tags = submission.get("tags", [])
        title = submission.get("title", "unknown_problem")
        code = submission.get("code", "")
        lang = submission.get("lang", "txt")

        # Sanitize parts
        difficulty = self.sanitize_filename(difficulty)
        clean_title = self.sanitize_filename(title)
        clean_tags = [self.sanitize_filename(tag) for tag in tags]
        # Use first tag if exists, otherwise "misc"
        tag_folder = clean_tags[0] if clean_tags else "misc"

        # Compose folder path
        folder_path = os.path.join(self.base_path, difficulty, tag_folder)
        os.makedirs(folder_path, exist_ok=True)

        ext = self.get_extension(lang)
        file_path = os.path.join(folder_path, f"{clean_title}.{ext}")

        with open(file_path, "w", encoding="utf-8") as f:
            # Insert a header comment with title and URL
            comment_style = self.get_comment_style(ext)
            header_lines = [
                f"{comment_style} Title: {title}",
                f"{comment_style} URL: {submission.get('url', '')}",
                f"{comment_style} Tags: {', '.join(tags)}",
                f"{comment_style} Difficulty: {difficulty}",
                ""
            ]
            f.write("\n".join(header_lines))
            f.write(code)
        return file_path

    def generate_readme_in_folder(self, base_folder: str, submissions: List[Dict]):
        """
        Create a README.md inside base_folder listing the problems it contains.
        """
        readme_path = os.path.join(base_folder, "README.md")
        lines = ["# LeetCode Problems Summary\n"]

        for sub in submissions:
            title = sub.get("title", "Unknown")
            url = sub.get("url", "")
            difficulty = sub.get("difficulty", "Unknown")
            tags = sub.get("tags", [])
            lines.append(f"- [{title}]({url}) — Difficulty: {difficulty} — Tags: {', '.join(tags)}")

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def get_comment_style(self, ext: str) -> str:
        """Returns the comment symbol based on language extension."""
        if ext in {"py", "sh", "rb"}:
            return "#"
        elif ext in {"js", "ts", "java", "cpp", "c", "cs", "go", "kt", "rs", "php"}:
            return "//"
        else:
            return "#"
