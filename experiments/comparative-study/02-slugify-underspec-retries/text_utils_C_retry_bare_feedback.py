import re


def slugify(text):
    """Convert an arbitrary string into a URL-safe slug.

    Rules:
    - lowercase the text
    - spaces become hyphens
    - non-alphanumeric characters (other than the hyphens we just
      introduced) are removed
    - runs of hyphens collapse to one, and leading/trailing hyphens
      are stripped, so stray whitespace or punctuation at the edges
      (or punctuation sitting next to a space) doesn't leak hyphens
      into the result
    """
    text = text.lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text


if __name__ == "__main__":
    tests = [
        ("Hello World", "hello-world"),
        ("  Python   Rocks!!  ", "python-rocks"),
        ("C++ is Fun (really)", "c-is-fun-really"),
        ("Already-slugged_value", "already-slugged_value".replace("_", "")),
        ("Trailing punctuation!!!", "trailing-punctuation"),
        ("--Leading and trailing--", "leading-and-trailing"),
        ("multiple   spaces  and---dashes", "multiple-spaces-and-dashes"),
        ("", ""),
    ]

    for text, expected in tests:
        result = slugify(text)
        status = "OK" if result == expected else "MISMATCH"
        print(f"{status}: slugify({text!r}) -> {result!r} (expected {expected!r})")
