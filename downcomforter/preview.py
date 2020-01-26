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
