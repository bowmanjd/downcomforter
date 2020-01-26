import re
from pathlib import Path

delimiter = re.compile(r"^---(json|toml|yaml)?$", re.MULTILINE)


def matter(text):
    result = delimiter.split(text, 2)
    front = {}
    try:
        _, lang, frontmatter, _, content = result
    except ValueError:
        pass
    else:
        if lang == "json":
            import json

            front = json.loads(frontmatter)
    return front, content.strip()


def load_matter(filename):
    p = Path(filename)
    with p.open() as f:
        text = f.read()
    return matter(text)


if __name__ == "__main__":
    import sys

    conf, content = load_matter(sys.argv[1])
    print(content.format(**conf))
