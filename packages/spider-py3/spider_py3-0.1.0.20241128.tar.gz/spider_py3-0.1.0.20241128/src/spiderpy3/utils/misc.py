from typing import Any
from htmlmin import minify


def compressed_html(html: str, **kwargs: Any) -> str:
    return minify(html, **kwargs)
