import os
from typing import Any, Dict, List, Sequence, Tuple

from langchain.agents.output_parsers.tools import ToolsAgentOutputParser
from langchain.schema import AIMessage
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers.tools import ToolAgentAction

from smart_pr_generator.tools import fetch_jira_issue


class PRGeneratorAgent:
    def __init__(self):
        self.agent = ChatOpenAI(
            model="gpt-4o",
            api_key=os.environ["LAAS_API_KEY"],
            base_url="https://api-laas.wanted.co.kr/api/preset/v2/",
            default_headers={
                "apiKey": os.environ["LAAS_API_KEY"],
                "project": "SMART_PR_GENERATOR",
            },
            extra_body={
                "hash": "e86358af60cf8366835060943349c2ab1954950253ab35d36abd2e7089d5f39a",
            },
        )
        self.tools_parser = ToolsAgentOutputParser()
        self.json_parser = JsonOutputParser()

    def generate_pr(self, branch: str, commits: List[str]) -> Dict[str, Any]:
        messages = [
            ("user", f"# Branch:\n {branch}\n\n# Commits:\n" + "\n".join(commits))
        ]

        answer = self._process_llm_response(messages)
        print("✅ AI 응답 생성 완료")
        return self.json_parser.invoke(answer)

    def _process_llm_response(self, messages: List[Tuple[str, str]]) -> AIMessage:
        response_message: AIMessage = self.agent.invoke(messages)

        if response_message.response_metadata["finish_reason"] == "tool_calls":
            for tool_call in response_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                if tool_name == "fetch_jira_issue":
                    tool_result = self._execute_tool(tool_name, tool_args)
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

                messages.extend(
                    [
                        response_message,
                        {
                            "role": "tool",
                            "name": tool_name,
                            "content": str(tool_result),
                            "tool_call_id": tool_call["id"],
                        },
                    ]
                )
                response_message = self.agent.invoke(messages)

        return response_message

    def _create_tool_calling_agent(llm: BaseLanguageModel, tools: Sequence[BaseTool]):
        if not hasattr(llm, "bind_tools"):
            raise ValueError(
                "This function requires a .bind_tools method be implemented on the LLM.",
            )
        llm_with_tools = llm.bind_tools(tools)
        agent = llm_with_tools | ToolsAgentOutputParser()
        return agent

    def _execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Any:
        if tool_name == "fetch_jira_issue":
            return fetch_jira_issue.invoke(tool_args)
        raise ValueError(f"Unknown tool: {tool_name}")


if __name__ == "__main__":
    branch = 'feature/PI-2435'
    commits = ["""e2a4b45 (HEAD -> feature/sandbox-create, origin/feature/sandbox-create) fix(sandbox-share-url.tsx): 버튼에 type 속성 추가하여 기본 동작 방지 fix(index.tsx): 샌드박스 URL이 존재할 때만 렌더링하도록 조건 추가
    73ab6bb refactor(create-sandbox-form.tsx): CreateSandboxForm 컴포넌트 삭제
    ffacfda fix(sandbox-params.tsx): onChange 핸들러에 e.target.value 전달
    c57b794 refactor(preset-sandbox): 불필요한 console.log 및 코드 제거 fix(api/sandbox): 잘못된 API 경로 수정 '/admin/sandbox/config/logo'로 변경
    dc9403b feat(sandbox-params.tsx): 입력 필드에 유효성 검사 및 오류 메시지 추가
    4cf630f feat(preset-sandbox): react-hook-form을 사용하여 폼 입력 기능 추가
    2a4d433 feat(preset-sandbox): 이미지 업로드 기능 추가 및 에러 메시지 개선
    e479005 refactor(index.tsx): 체크박스와 라벨을 FlexBox로 감싸 UI 개선 fix(index.tsx): 체크박스에 id 추가 및 라벨과 연결 fix(index.tsx): 사용 모델 정보 노출 라벨 추가 및 위치 변경
    1ecf334 feat(preset-sandbox): 가변 필드 추가 및 접근 설정 필드 위치 변경
    0c5dd05 refactor(preset-sandbox): DetailRowItem 컴포넌트 제거 및 FormField로 대체 feat(preset-sandbox): Checkbox 컴포넌트 추가하여 모델 정보 노출 설정 가능 style(preset-sandbox): 기본 정보 섹션의 Typography 제거 및 스타일 개선
    d927c74 refactor(preset-sandbox): 로고 표시 방식 개선 및 스타일 수정 fix(preset-sandbox): 로고 필드에 오류 메시지 추가 chore(preset-sandbox): 사용하지 않는 코드 주석 처리
    73cae12 feat(preset-sandbox): 폼 필드 추가 및 유효성 검사 메시지 구현
    f6c0869 refactor(preset-sandbox): 접근 설정 폼 위치 변경 및 불필요한 코드 제거
    2974330 refactor(preset-sandbox): 샌드박스 생성 및 업데이트 로직 통합 refactor(preset-sandbox): 접근 설정을 라디오 버튼으로 변경 style(sandbox-share-url): 버튼 크기 'small'로 
    조정 fix(preset-sandbox): 불필요한 import 제거 및 코드 정리 feat(preset-sandbox): 폼 제
    출 시 샌드박스 저장 기능 추가
    2daf195 refactor: rename from presetId to presetHash
    e4ed527 refactor(sandbox-share-url.tsx): 불필요한 TextInput 컴포넌트 제거
    3b186a2 style(index.tsx): 불필요한 Box import 제거 refactor(index.tsx): 주석 처리된 FlexBox 코드 제거 fix(index.tsx): '상태' 라벨을 '접근 설정'으로 변경
    49df740 style(index.tsx): FlexBox 컴포넌트를 주석 처리하여 UI 요소 숨김
    acaa996 refactor(sandbox-share-url.tsx): URL 복사 버튼과 새 탭 열기 버튼 구조 변경
    7674843 feat(preset-sandbox): 새로운 샌드박스 생성 폼 추가
    f8f0fed feat(hooks): 이미지 업로드 기능 추가
    4bc594f fix(api): 잘못된 타입 정의 수정"""]
    print(1, PRGeneratorAgent().generate_pr(branch, commits))