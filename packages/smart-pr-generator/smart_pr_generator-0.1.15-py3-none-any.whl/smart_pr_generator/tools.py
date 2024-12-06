import os
from langchain_core.tools import tool

from .helpers.jira_client import JiraClient


@tool
def fetch_jira_issue(jira_issue_id: str):
    """jira에서 이슈를 가져옵니다."""
    print("🔍 JIRA 이슈 정보를 가져오는 중...")
    if not isinstance(jira_issue_id, str):
        print("❌ JIRA 이슈 ID는 문자열이어야 합니다.")
        return None
    jira = JiraClient(email=os.environ.get("JIRA_EMAIL"), api_token=os.environ.get("JIRA_API_TOKEN"))
    results = jira.fetch_issue(jira_issue_id)
    print(f"✅ JIRA 이슈 정보 가져오기 완료 ({jira_issue_id})")
    return results
