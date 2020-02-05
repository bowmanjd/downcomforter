# Copyright 2020 Jonathan Bowman
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import re
from pathlib import Path

delimiter = re.compile(r"^---(json|toml|yaml)?$", re.MULTILINE)


def matter(text):
    result = delimiter.split(text, 2)
    front = {}
    content = ""
    try:
        _, lang, frontmatter, _, content = result
    except ValueError:
        content = text
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
