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

import sys
import importlib.resources

from livereload import Server

from . import down
from . import matter
from . import highlight


def make_app(mdfilename, cssfilename=None, tplfilename=None):
    def app(env, start_response):
        if env.get("PATH_INFO").endswith("css"):
            if cssfilename is None:
                pass
                output = importlib.resources.read_text(__package__, "style.css")
            else:
                with open(cssfilename) as f:
                    output = f.read().encode("utf-8")
                content_type = "text/css"
        else:
            conf, content = matter.load_matter(mdfilename)
            coded = highlight.codedoc(content)
            html = down.md_to_html(coded, tplfilename)
            output = html.format(**conf).encode("utf-8")
            content_type = "text/html"

        start_response(
            "200 OK",
            [
                ("Content-Type", f"{content_type}; charset=utf-8"),
                ("Content-Length", str(len(output))),
            ],
        )

        return [output]

    return app


if __name__ == "__main__":
    md = sys.argv[1]
    css = sys.argv[2]
    print(md)
    server = Server(make_app(md, css))
    server.watch(md)
    server.serve(host="0.0.0.0")
