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
import re

import cmarkgfm

from . import cmarkopt


def mdparse(md):
    """A separate function that can be adapted to a particular Markdown implementation"""
    parsed = cmarkgfm.markdown_to_html(md, cmarkopt.SMART | cmarkopt.UNSAFE)
    return parsed


def md_to_html(md, tpl_filename=None):
    if tpl_filename is None:
        template = importlib.resources.read_text(__package__, "index.html")
    else:
        with open(tpl_filename) as f:
            template = f.read()
    content = mdparse(md)
    return template.format(content=content)


def tpl(content, template=None):
    if template is None:
        return content
    else:
        template = bracify(template)
        content = template.format(content=content)
        return tpl(content)


if __name__ == "__main__":
    import sys

    md = " ".join(sys.argv[1:])
    html = md_to_html(md)
    print(html)
