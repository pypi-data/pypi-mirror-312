import os
import re
from typing import Optional

from jira import JIRA


class JiraClient:
    def __init__(self, email: Optional[str] = None, api_token: Optional[str] = None):
        self.server = "https://wantedlab.atlassian.net"
        self.email = email if email else os.environ.get("JIRA_EMAIL")
        self.api_token = api_token if api_token else os.environ.get("JIRA_API_TOKEN")
        self.client = self._initialize_client()

    def _initialize_client(self) -> JIRA:
        return JIRA(
            server=self.server,
            basic_auth=(self.email, self.api_token),
        )

    def _extract_jira_id(self, branch_name: str) -> Optional[str]:
        jira_id_match = re.search(r"([A-Z]+-\d+)", branch_name)
        if not jira_id_match:
            print("⚠️ 브랜치명에서 JIRA 이슈 ID를 찾을 수 없습니다.")
            return None
        return jira_id_match.group(1)

    def fetch_issue(self, jira_issue_id: str) -> Optional[dict]:
        jira_id = self._extract_jira_id(jira_issue_id)
        if not jira_id:
            return None

        try:
            issue_data = self.client.issue(jira_id)
            issue_info = {
                "id": jira_id,
                "title": issue_data.fields.summary,
                "description": issue_data.fields.description,
                "assignee": issue_data.fields.assignee.raw["displayName"]
                if issue_data.fields.assignee
                else "Unassigned",
                "status": issue_data.fields.status.raw["name"],
                "url": f"{self.server}/browse/{jira_id}",
            }

            return issue_info

        except Exception as e:
            print(f"❌ JIRA 이슈 정보 가져오기 실패: {str(e)}")
            return None
