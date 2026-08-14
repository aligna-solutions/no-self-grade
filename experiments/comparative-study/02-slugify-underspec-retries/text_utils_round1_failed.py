import re


def slugify(text):
    """Convert an arbitrary string into a URL-safe slug.

    Rules:
    - lowercase the text
    - spaces become hyphens
    - non-alphanumeric characters (other than the hyphens we just
      introduced) are removed
    """
    text = text.lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    return text


if __name__ == "__main__":
    tests = [
        ("Hello World", "hello-world"),
        ("  Python   Rocks!!  ", "-python-rocks-"),
        ("C++ is Fun (really)", "c-is-fun-really"),
        ("Already-slugged_value", "already-slugged_value".replace("_", "")),
    ]

    for text, expected in tests:
        result = slugify(text)
        status = "OK" if result == expected else "MISMATCH"
        print(f"{status}: slugify({text!r}) -> {result!r} (expected {expected!r})")
