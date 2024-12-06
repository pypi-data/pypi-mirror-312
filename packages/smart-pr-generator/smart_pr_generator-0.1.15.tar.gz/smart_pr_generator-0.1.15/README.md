# Smart Pull Request Generator

Smart Pull Request Generator는 GitHub와 JIRA를 통합하여 스마트한 풀 리퀘스트를 생성하는 도구입니다. 이 도구는 개발자가 더 효율적으로 작업할 수 있도록 돕습니다.

## 설치 방법

### 설치하기

```sh
pip install --upgrade smart-pr-generator
```

### 로컬에 CLI 설치하기

다음 명령어를 사용하여 로컬에 설치할 수 있습니다:

```sh
pip install .

# 개발 모드로 설치
pip install -e .
```

### GitHub에서 설치하기

GitHub 저장소에서 직접 설치하려면 다음 명령어를 사용하세요:

```sh
pip install git+https://github.com/jeongsk/Smart-PR-Generator.git
```

## 필수 설정

### GitHub 토큰 발급 받기

GitHub 토큰을 발급 받으려면 [GitHub 토큰 설정 페이지](https://github.com/settings/tokens)로 이동하세요.

### JIRA API 토큰 발급 받기

JIRA API 토큰을 발급 받으려면 [JIRA API 토큰 설정 페이지](https://id.atlassian.com/manage-profile/security/api-tokens)로 이동하세요.

### 환경 변수 설정

다음 환경 변수를 설정해야 합니다:

```env
export SMART_PR_GENERATOR_API_KEY="LAAS API KEY"

export GITHUB_TOKEN="개인 깃허브 토큰"

export JIRA_EMAIL="지라 개인 이메일 주소"
export JIRA_API_TOKEN="지라 개인 API 액세스 토큰"
```

환경 변수를 설정하는 방법은 세 가지가 있습니다:
1. `~/.zshrc` 파일에 환경 변수를 추가합니다.
2. `~/.smart-pr-generator` 파일을 생성하고 위의 환경 변수를 추가합니다.
3. 프로젝트 루트에 `.env` 파일을 생성하고 위의 환경 변수를 추가합니다.

## 프로젝트 구조

- `smart_pr_generator/`: 주요 소스 코드가 포함된 디렉토리입니다.
  - `__init__.py`: 패키지 초기화 파일입니다.
  - `agents.py`: 에이전트 관련 기능을 포함합니다.
  - `config.py`: 설정 관련 기능을 포함합니다.
  - `main.py`: 프로그램의 진입점입니다.
  - `prompts.py`: 사용자 프롬프트 관련 기능을 포함합니다.
  - `tools.py`: 도구 관련 기능을 포함합니다.
  - `helpers/`: 보조 기능을 포함한 디렉토리입니다.
    - `__init__.py`: 보조 기능 초기화 파일입니다.
    - `get_git_info.py`: Git 정보 수집 기능을 포함합니다.
    - `github_client.py`: GitHub 클라이언트 기능을 포함합니다.
    - `is_tool_calling.py`: 도구 호출 여부를 확인하는 기능을 포함합니다.
    - `jira_client.py`: JIRA 클라이언트 기능을 포함합니다.
- `tests/`: 테스트 코드가 포함된 디렉토리입니다.
  - `test_main.py`: 메인 기능에 대한 테스트를 포함합니다.

## 사용 예시

설치 및 환경 변수 설정 후, 다음과 같은 명령어로 Smart Pull Request Generator를 사용할 수 있습니다:

```sh
# 사용 명령어 Pull Request
$ spr
```

## 기여하기

기여를 원하신다면, 이 저장소를 포크하고 풀 리퀘스트를 보내주세요. 기여는 언제나 환영입니다!

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
