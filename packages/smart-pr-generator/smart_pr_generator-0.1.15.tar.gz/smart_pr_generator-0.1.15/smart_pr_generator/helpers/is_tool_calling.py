def is_tool_calling(response):
    # additional_kwargs에서 tool_calls 확인
    has_tool_calls_in_kwargs = bool(response.additional_kwargs.get("tool_calls"))

    # 최상위 레벨의 tool_calls 확인
    has_tool_calls_direct = bool(getattr(response, "tool_calls", None))

    return has_tool_calls_in_kwargs or has_tool_calls_direct
