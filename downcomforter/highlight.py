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

import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer

from . import pattern

code_re = re.compile(r"^```([a-z]+)?$(.+?)^```$", re.S | re.M)
formatter = HtmlFormatter()


def codeblock(match):
    lang, code = match.groups()
    try:
        lexer = get_lexer_by_name(lang)
    except ValueError:
        lexer = TextLexer()
    highlighted = pygments.highlight(code, lexer, formatter)
    escaped = pattern.escape_braces(highlighted)
    return escaped


def codedoc(md):
    highlighted = code_re.sub(codeblock, md)
    return highlighted
