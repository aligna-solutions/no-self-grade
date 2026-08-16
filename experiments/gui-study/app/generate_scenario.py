import json
import random

random.seed(42)

N = 80
MISMATCH_INDICES = set(random.sample(range(N), 12))

rows = []
for i in range(N):
    sku = f"SKU-{i+1:03d}"
    expected_qty = random.randint(5, 500)
    if i in MISMATCH_INDICES:
        delta = random.choice([-1, 1]) * random.randint(1, 20)
        counted_qty = max(0, expected_qty + delta)
    else:
        counted_qty = expected_qty
    rows.append({
        "sku": sku,
        "expected_qty": expected_qty,
        "counted_qty": counted_qty,
        "checked": False,
        "status": "pending",
    })

with open("rows_seed.json", "w") as f:
    json.dump({"rows": rows, "submitted": False}, f, indent=2)

print(f"Generated {N} rows, {len(MISMATCH_INDICES)} mismatched (should be flagged).")
