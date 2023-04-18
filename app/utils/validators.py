from typing import Callable, Any, Coroutine

from fastapi import Header


def validate_content_length(max_length: int) -> Callable[[int], Coroutine[Any, Any, int]]:
    async def valid_content_length(content_length: int = Header(..., lt=max_length)) -> int:
        return content_length

    return valid_content_length
