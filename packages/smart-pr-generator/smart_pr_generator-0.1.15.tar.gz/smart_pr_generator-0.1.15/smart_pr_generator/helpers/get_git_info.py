import subprocess
import sys
from typing import Optional


def get_git_info(no_verify: Optional[bool] = False):
    print("🔍 Git 정보를 확인하는 중...")
    try:
        # 1단계: symbolic-ref 사용
        try:
            default_branch = subprocess.check_output(
                ["git", "symbolic-ref", "refs/remotes/origin/HEAD"], text=True
            ).strip().split("/")[-1]
        except subprocess.CalledProcessError:
            # 2단계: remote show origin 사용
            try:
                remote_info = subprocess.check_output(
                    ["git", "remote", "show", "origin"], text=True
                )
                for line in remote_info.splitlines():
                    if "HEAD branch" in line:
                        default_branch = line.split()[-1]
                        break
                else:
                    # 3단계: 기본값 'main' 사용
                    print("⚠️ 기본 브랜치를 찾을 수 없어 'main'으로 가정합니다.")
                    default_branch = 'main'
            except subprocess.CalledProcessError:
                print("⚠️ 기본 브랜치를 찾을 수 없어 'main'으로 가정합니다.")
                default_branch = 'main'

        # 나머지 코드는 동일하게 유지
        if not no_verify:
            status = subprocess.check_output(
                ["git", "status", "--porcelain"], text=True
            ).strip()
            if status:
                print("❌ Error: 커밋되지 않은 변경사항이 있습니다. 먼저 커밋하거나 스태시해주세요.")
                sys.exit(1)

        commits = subprocess.check_output(
            ["git", "log", f"{default_branch}..HEAD", "--patch"], text=True
        ).strip()
        if not commits:
            print("❌ 현재 브랜치에 커밋이 없습니다.")
            sys.exit(1) 

        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
        remote = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"], text=True
        ).strip()

        if "git@github.com:" in remote:
            owner, repo = remote.split("git@github.com:")[-1].replace(".git", "").split("/")
        else:
            owner, repo = remote.replace(".git", "").split("github.com/")[-1].split("/")

        print(f"✅ Git 정보 확인 완료 (브랜치: {branch}, 기본 브랜치: {default_branch}, 저장소: {owner}/{repo})")
        return commits.split("\n"), branch, owner, repo, default_branch

    except Exception as e:
        print(f"❌ Git 에러: {str(e)}")
        sys.exit(1)
