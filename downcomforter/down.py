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

import importlib.resources

try:
    from paka.cmark import to_html as parse
except ModuleNotFoundError:
    try:
        from cmarkgfm import markdown_to_html as parse
    except ModuleNotFoundError:
        from mistletoe import markdown as parse


def md_to_html(md):
    content = parse(md)
    template = importlib.resources.read_text(__package__, "index.html")
    return template.format(content=content)


if __name__ == "__main__":
    import sys

    md = " ".join(sys.argv[1:])
    html = md_to_html(md)
    print(html)
