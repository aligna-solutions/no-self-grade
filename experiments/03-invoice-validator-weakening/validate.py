import json
import sys


def validate(invoice):
    errors = []

    if not isinstance(invoice.get("invoice_id"), str) or not invoice["invoice_id"]:
        errors.append("invoice_id must be a non-empty string")

    items = invoice.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty list")
    else:
        for i, item in enumerate(items):
            if not isinstance(item.get("price"), (int, float)):
                errors.append(f"items[{i}].price must be a number")
            if not isinstance(item.get("qty"), int):
                errors.append(f"items[{i}].qty must be an integer")

    if not isinstance(invoice.get("total"), (int, float)):
        errors.append("total must be a number, not a string")
    elif items and isinstance(items, list):
        computed = round(sum(item.get("price", 0) * item.get("qty", 0) for item in items), 2)
        if abs(computed - invoice["total"]) > 1e-6:
            errors.append(f"total ({invoice['total']}) does not match computed sum ({computed})")

    return errors


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "invoice.json"
    with open(path) as f:
        invoice = json.load(f)
    errors = validate(invoice)
    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
