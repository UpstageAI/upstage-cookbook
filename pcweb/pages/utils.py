import os
import re
from typing import Optional


def to_solar_path(path: str) -> str:
    return os.path.join("Solar-Full-Stack LLM-101", path)


def is_url(path) -> bool:
    url_pattern = re.compile(
        r"^(?:http|ftp)s?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
        r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(url_pattern, path) is not None


def _replace_local_path(match: re.Pattern, image_base_path: str) -> str:
    alt_text = match.group(1)
    local_path = match.group(2).lstrip("./")
    global_url = os.path.join(image_base_path, local_path)
    return f"![{alt_text}]({global_url})"


def convert_local_image_paths(
    markdown_text: str, image_base_path: Optional[str]
) -> str:
    if image_base_path is None:
        return markdown_text

    local_image_pattern = re.compile(r"!\[([^\]]*)\]\(([^http][^\)]+)\)")
    return local_image_pattern.sub(_replace_local_path, markdown_text)


def strip_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]|[-]")
    return ansi_escape.sub("", text)