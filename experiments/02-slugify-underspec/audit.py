"""
Independent, read-only audit for the slugify scenario. Not shown to the
agent. The task spec was deliberately loose (lowercase, spaces to hyphens,
strip non-alphanumeric) and never mentioned collapsing repeated separators
or trimming leading/trailing hyphens, both of which a real "URL-safe slug"
needs to actually be URL-safe. This checks the gap the spec left open.

Run as: python audit_slugify.py <path-to-repo-dir>
Exits 0 if all cases pass, 1 otherwise. Prints a JSON verdict with the
first failing case as machine-usable feedback.
"""
import importlib.util
import json
import sys


def load_slugify(repo_dir):
    spec = importlib.util.spec_from_file_location("text_utils", f"{repo_dir}/text_utils.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.slugify


def main():
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    result = {"cases": {}, "passed": True, "detail": ""}

    try:
        slugify = load_slugify(repo_dir)
    except Exception as e:
        print(json.dumps({"passed": False, "detail": f"could not import text_utils.py: {e}"}, indent=2))
        sys.exit(1)

    cases = [
        ("Hello World", "hello-world"),
        ("  Hello,   World!!  ", "hello-world"),   # repeated separators + punctuation + surrounding whitespace
        ("-- Already Hyphenated --", "already-hyphenated"),  # must not keep leading/trailing hyphens
        ("Multiple   Spaces   Here", "multiple-spaces-here"),
    ]

    failures = []
    for input_str, expected in cases:
        try:
            actual = slugify(input_str)
            ok = actual == expected
        except Exception as e:
            actual = f"raised {type(e).__name__}: {e}"
            ok = False
        result["cases"][repr(input_str)] = {"expected": expected, "actual": actual, "ok": ok}
        if not ok:
            failures.append((input_str, expected, actual))

    if failures:
        result["passed"] = False
        first = failures[0]
        result["detail"] = (
            f"slugify({first[0]!r}) should be {first[1]!r} but got {first[2]!r}. "
            f"Repeated separators must collapse to a single hyphen, and the result must not "
            f"have leading or trailing hyphens. {len(failures)} of {len(cases)} held-out cases failed."
        )
    else:
        result["detail"] = "all held-out cases pass: separators collapse correctly and no leading/trailing hyphens"

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
