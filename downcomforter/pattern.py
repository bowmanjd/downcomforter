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

from . import matter
from . import down
from . import highlight

# brace_re = re.compile(r"{([^}]+)}")
brace_re = re.compile(r"{(?!content)([^}]+)}")


def double_braces(text):
    escaped = brace_re.sub(r"{{\1}}", text)
    return escaped


def codedown(content):
    coded = highlight.codedoc(content)
    html = down.parse(coded)
    return html


def loader(filename=None, conf={}, content=""):
    """Load file, related files, and build document"""
    # Done if no more files
    if filename is None:
        return conf, content
    p = Path(filename)
    # Split front matter and raw content
    new_conf, new_content = matter.load_matter(p)
    # ensure raw content is now html
    if p.suffix == ".md":
        new_content = codedown(new_content)
    try:
        label = conf["include"].pop(filename)
    except KeyError:
        pass
    else:
        if label != "parent":
            conf[label] = new_content
        else:
            new_content = double_braces(new_content).format(content=content)

    label = conf.get("include", {}).get(filename, "")
    includes = new_conf.pop("include", {})
    for label, pathname in includes.items():
        if label == "parent":
            conf = {"content": "", **new_conf, **conf}
        else:
            conf = {label: new_content, **conf, **new_conf}


def tpl(content, template=None):
    if template is None:
        return content
    else:
        template = double_braces(template)
        content = template.format(content=content)
        return tpl(content)
