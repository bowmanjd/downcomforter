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

brace_re = re.compile(r"{([^}]+)}")
tpl_re = re.compile(r"(?!{content}){([^}]+)}")


def escape_braces(text, pattern=brace_re):
    escaped = pattern.sub(r"{{\1}}", text)
    return escaped


def codedown(content):
    coded = highlight.codedoc(content)
    html = down.mdparse(coded)
    return html


def loader(filename=None, conf={}, content=""):
    """Load file, related files, and build document"""
    # Done if no more files
    if filename is None:
        return content.format(**conf)
    p = Path(filename)
    # Split front matter and raw content
    new_conf, new_content = matter.load_matter(p)
    # ensure raw content is now html
    if p.suffix == ".md":
        new_content = codedown(new_content)
    # check if this filename was included by previous
    try:
        label = conf["include"].pop(filename)
    except KeyError:  # not an include
        conf = {**conf, **new_conf}
        content = new_content
    else:  # if this is include, then:
        if label != "parent":  # refers to child snippet
            # assign to template var by label; merge in child vars
            conf = {label: new_content, **conf, **new_conf}
        else:  # refers to parent template
            # place existing content within loaded new template
            template = escape_braces(new_content, tpl_re)
            print(template)
            content = template.format(content=content)
            # merge previous vars into template vars
            conf = {**new_conf, **conf}
    # check front matter for includes
    includes = conf.get("include", {})
    try:  # get next filename from includes, if any
        print("Has include")
        filename, label = includes.popitem()
        print(filename)
        filepath = p.parent / filename
        includes[filepath] = label
    except KeyError:
        filepath = None
    return loader(filepath, conf, content)


if __name__ == "__main__":
    pass
