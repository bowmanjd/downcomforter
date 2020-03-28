# Copyright 2020 Jonathan Bowman
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import functools
import importlib
import re
from pathlib import Path

from . import matter
from . import down
from . import highlight

BRACE_RE = re.compile(r"{([^}]+)}")
TPL_RE = re.compile(r"(?!{content}){([^}]+)}")


def escape_braces(text, pattern=BRACE_RE):
    escaped = pattern.sub(r"{{\1}}", text)
    return escaped


def codedown(content):
    coded = highlight.codedoc(content)
    html = down.mdparse(coded)
    return html


@functools.lru_cache(maxsize=32)
def import_helper(filepath):
    spec = importlib.util.spec_from_file_location(f"helper.{filepath.stem}", filepath)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return helper


def prepare_helpers(conf, directory):
    helpers = conf.pop("helpers", {})
    helper_methods = conf.get("helper_methods", {})
    for filename, method in helpers.items():
        filepath = (directory / filename).resolve()
        helper = import_helper(filepath)
        func = getattr(helper, method)
        helper_methods[method] = func
        # conf[method] = func(conf)
    conf["helper_methods"] = helper_methods
    return conf


def call_helpers(conf):
    helper_methods = conf.get("helper_methods", {})
    for name, func in helper_methods.items():
        conf[name] = func(conf)
    return conf


def merge(conf, content):
    conf = call_helpers(conf)
    return content.format(**conf)


def parse_includes():
    pass


def prepare_includes(conf, directory):
    includes = conf.get("include", {})
    try:  # get next filename from includes, if any
        filename, label = includes.popitem()
        filepath = (directory / filename).resolve()
        includes[filepath] = label
    except KeyError:
        filepath = None
    return filepath, conf


def get_include_label(filename, conf):
    try:
        label = conf["include"].pop(filename)
    except KeyError:
        label = None
    return label


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
    # check if this filename was included by previous
    label = get_include_label(filename, conf)
    if label is None:  # not an include
        conf = {**conf, **new_conf}
        content = new_content
    elif label == "parent":  # refers to parent template
        # place existing content within loaded new template
        template = escape_braces(new_content, TPL_RE)
        content = template.format(content=content)
        # merge previous vars into template vars
        conf = {**new_conf, **conf}
    else:  # refers to child snippet
        # assign to template var by label; merge in child vars
        conf = {label: new_content, **conf, **new_conf}

    # check front matter for helpers
    conf = prepare_helpers(conf, p.parent)

    # check front matter for includes
    filepath, conf = prepare_includes(conf, p.parent)

    return loader(filepath, conf, content)


if __name__ == "__main__":
    pass
