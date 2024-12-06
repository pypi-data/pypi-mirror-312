from pathlib import Path
from typing import Optional

from smart_pr_generator.prompts import DEFAULT_PULL_REQUEST_TEMPLATE

def get_pull_request_template(project_root: str) -> Optional[str]:
    """
    프로젝트 루트 경로에서 PR 템플릿을 찾아 내용을 반환합니다.
    템플릿이 없으면 None을 반환합니다.
    """
    possible_paths = [
        '.github/pull_request_template.md',
        '.github/PULL_REQUEST_TEMPLATE.md',
        'docs/pull_request_template.md',
        'PULL_REQUEST_TEMPLATE.md'
    ]

    root_path = Path(project_root)
    
    for template_path in possible_paths:
        full_path = root_path / template_path
        try:
            if full_path.is_file():
                return full_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading template at {full_path}: {e}")
    
    return DEFAULT_PULL_REQUEST_TEMPLATE

# 사용 예시
if __name__ == "__main__":
    template = get_pull_request_template(".")
    if template:
        print("Found PR template:")
        print(template)
    else:
        print("No PR template found")
