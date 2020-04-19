
def encode(text: str):
    return "*" * len(text)


def markInHtml(text: str):
    return '<mark style="background: #7aecec;">' + text + '</mark>'