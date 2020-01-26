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
