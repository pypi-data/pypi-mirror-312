# github_client.py
import os
from typing import Any, Dict, Optional

import requests


class GitHubError(Exception):
    """Base exception for GitHub API errors"""

    pass

class GitHubPRError(GitHubError):
    """Raised when PR not exist"""

    pass

class GitHubPRExistsError(GitHubError):
    """Raised when PR already exists"""

    pass


class GitHubAuthError(GitHubError):
    """Raised when authentication fails"""

    pass


class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token if token else os.environ["GITHUB_TOKEN"]
        self.base_url = "https://api.github.com"

    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str,
    ) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/pulls",
                headers={
                    "Authorization": f"token {self.token}",
                    "content-type": "application/json",
                },
                json={
                    "title": title,
                    "body": body,
                    "head": head,
                    "base": base,
                },
            )
            # print("status_code", response.status_code)

            if response.status_code == 401:
                raise GitHubAuthError(
                    "Authentication failed. Check your GitHub token")

            if response.status_code // 100 != 2:
                error_data = response.json() if response.content else {}
                print("error", error_data)
                if "422" in str(error_data.get("status", "")):
                    errors = error_data.get("errors", [])
                    if errors and errors[0].get("code") == "invalid":
                        raise GitHubPRError(
                            f"Branch '{head}' does not exist on remote. Please push your changes first."
                        )
                    raise GitHubPRExistsError(
                        f"Pull Request already exists: {head} → {base} "
                        f"(Status: {response.status_code})"
                    )

                if (error_data.get("errors")
                    and len(error_data["errors"]) > 0
                        and error_data["errors"][0].get("message")):
                    raise GitHubError(error_data["errors"][0]["message"])

            response.raise_for_status()
            return response.json()
        except ValueError as e:
            raise GitHubError(f"Failed to parse GitHub API response: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise GitHubError(f"GitHub API request failed: {str(e)}")
