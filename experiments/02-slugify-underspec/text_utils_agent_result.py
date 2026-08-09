import re


def slugify(text):
    """Convert an arbitrary string into a URL-safe slug.

    - Lowercases the text
    - Replaces whitespace runs with hyphens
    - Strips characters that aren't alphanumeric or hyphens
    - Collapses repeated hyphens and trims leading/trailing hyphens
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


if __name__ == "__main__":
    tests = [
        ("Hello World!", "hello-world"),
        ("  Multiple   Spaces  ", "multiple-spaces"),
        ("C++ & Python: A Love Story", "c-python-a-love-story"),
        ("Already-Slugged-123", "already-slugged-123"),
        ("Ünïcödé Test", "ncd-test"),
    ]

    for input_text, expected in tests:
        result = slugify(input_text)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] slugify({input_text!r}) -> {result!r} (expected {expected!r})")
