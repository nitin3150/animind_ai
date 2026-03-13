import re

def code_extractor(raw: str) -> str:
    pattern = re.compile(
        r"```(?:python|py)?\s*\n(.*?)```",
        re.DOTALL | re.IGNORECASE
    )
    match  = pattern.search(raw)
    if match:
        return match.group(1).strip()

    stripped = raw.strip()

    return stripped