from collections.abc import Callable, Sequence
from typing import Any

import litellm
import rich
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

import llm_cli as lc
import llm_cli.config as lcc
import llm_cli.utils as lcu
from llm_cli.interactive._usage import usage_panel


async def output(
    prompt: str,
    *,
    prefix: str | None = None,
    sanitize: Callable[[str], str] | None = lcu.extract_between_tags,
    stop: str | Sequence[str] | None = None,
    title: str | Text | None = None,
) -> litellm.ModelResponse:
    cfg: lcc.Config = lcc.get_config()
    router: litellm.Router = cfg.router.router
    messages: list[dict[str, Any]] = [{"role": "user", "content": prompt}]
    if prefix:
        messages.append({"role": "assistant", "content": prefix, "prefix": True})
    stream: litellm.CustomStreamWrapper = await router.acompletion(
        **cfg.completion.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude_none=True
        ),
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
        stop=stop,
    )  # pyright: ignore [reportAssignmentType]
    chunks: list[litellm.ModelResponse] = []
    response: litellm.ModelResponse = litellm.ModelResponse()
    with Live(transient=True) as live:
        title: Text | None = _make_title(title, model=stream.model)
        async for chunk in stream:
            chunk: litellm.ModelResponse
            chunks.append(chunk)
            response = litellm.stream_chunk_builder(chunks)  # pyright: ignore [reportAssignmentType]
            content: str = _get_content(response, prefix=prefix, sanitize=sanitize)
            live.update(
                Group(
                    Panel(content, title=title, title_align="left", expand=False),
                    usage_panel(response, expand=False),
                )
            )
    content: str = _get_content(response, prefix=prefix, sanitize=sanitize)
    print(content)
    rich.print(Panel(lc.pretty_usage(response), expand=False))
    return response


def _make_title(title: str | Text | None, model: str | None = None) -> Text | None:
    if isinstance(title, Text):
        return title
    title: str | None = title or model
    if title is None:
        return None
    return Text(title, style="bold cyan")


def _get_content(
    resp: litellm.ModelResponse,
    *,
    prefix: str | None = None,
    sanitize: Callable[[str], str] | None = lcu.extract_between_tags,
) -> str:
    content: str = litellm.get_content_from_model_response(resp)
    if prefix and not content.startswith(prefix):
        content = prefix + content
    if sanitize:
        content = sanitize(content)
    return content
