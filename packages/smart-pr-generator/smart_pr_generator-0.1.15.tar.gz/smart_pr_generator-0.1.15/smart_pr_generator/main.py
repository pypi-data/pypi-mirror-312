import argparse
import os

import requests
from packaging import version

from smart_pr_generator.agents import PRGeneratorAgent
from smart_pr_generator.config import Config
from smart_pr_generator.helpers import get_git_info
from smart_pr_generator.helpers.github_client import GitHubClient


VERSION = "0.1.15"


def check_package_updates():
    """현재 설치된 패키지와 PyPI의 최신 버전을 비교"""
    try:
        # PyPI API 호출
        response = requests.get("https://pypi.org/pypi/smart-pr-generator/json")
        if response.status_code == 200:
            latest_version = response.json()["info"]["version"]

            # 버전 비교
            update_available = version.parse(latest_version) > version.parse(VERSION)

        # 업데이트 메시지 출력
        if update_available:
            print("-" * 60)
            print("📦 패키지 업데이트가 필요합니다:")
            print(f"현재 버전: {VERSION}")
            print(f"최신 버전: {latest_version}")
            print("\n업데이트 명령어: pip install --upgrade smart-pr-generator")
            print("-" * 60)
            print("")
    except Exception:
        pass


# main() 함수 시작 부분에 추가
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=f"v{VERSION}",
        help="현재 버전을 출력합니다",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="커밋되지 않은 변경사항 체크를 스킵합니다",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="GitHub PR 생성 단계를 스킵합니다",
    )
    args = parser.parse_args()

    check_package_updates()

    Config().load_env_files()

    print("🚀 PR 생성 프로세스를 시작합니다...")

    commits, branch, owner, repo, default_branch = get_git_info(
        no_verify=args.no_verify
    )
    print(f"commits: {len(commits)}, branch: {branch}, owner: {owner}, repo: {repo}")

    print("🤖 AI로 PR 내용을 생성하는 중...")
    try:
        agent = PRGeneratorAgent()
        pr_data = agent.generate_pr(branch, commits)

        if args.test:
            print("🧪 테스트 모드: GitHub PR 생성을 스킵합니다")
            return

        print("📨 GitHub PR을 생성하는 중...")
        print(f"https://api.github.com/repos/{owner}/{repo}/pulls")
        github_client = GitHubClient(os.environ["GITHUB_TOKEN"])
        pr_response = github_client.create_pull_request(
            owner=owner,
            repo=repo,
            title=pr_data["title"],
            body=pr_data["description"],
            head=branch,
            base=default_branch,
        )
        pr_url = pr_response["html_url"]
        print("✨ PR이 성공적으로 생성되었습니다!")
        print(f"🔗 PR URL: {pr_url}")
    except Exception as e:
        print(f"❌ PR 생성 실패 (에러: {e})")


if __name__ == "__main__":
    main()
