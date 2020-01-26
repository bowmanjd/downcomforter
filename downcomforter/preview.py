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
from livereload import Server

from . import down
from . import matter


def make_app(filename):
    def app(env, start_response):
        conf, content = matter.load_matter(filename)
        output = down.md_to_html(content.format(**conf)).encode("utf-8")

        start_response(
            "200 OK",
            [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Content-Length", str(len(output))),
            ],
        )

        return [output]

    return app


if __name__ == "__main__":
    filename = sys.argv[1]
    print(filename)
    server = Server(make_app(filename))
    server.watch(filename)
    server.serve()
