
import pandas as pd
import re
import sys

INPUT_FILE = "build2/generated_content.csv"

REQUIRED_FIELDS = [
    "city",
    "state",
    "slug",
    "keyword",
    "primary_segment",
    "secondary_segment",
    "market_angle",
    "hero_copy",
    "operations_copy",
    "local_copy",
    "meta_description",
]

df = pd.read_csv(INPUT_FILE)

errors = []

print("CONTENT VALIDATION")
print("-" * 40)

# 1. Required fields
for field in REQUIRED_FIELDS:
    if field not in df.columns:
        errors.append(f"Missing column: {field}")

# 2. Expected row count
if len(df) != 25:
    errors.append(f"Expected 25 rows, found {len(df)}")

# 3. Blank values
for field in REQUIRED_FIELDS:
    if field in df.columns:
        blank_count = df[field].isna().sum() + (df[field].astype(str).str.strip() == "").sum()
        if blank_count > 0:
            errors.append(f"{field}: {blank_count} blank values")

# 4. Basic unsupported numeric-claim guardrail
content_fields = [
    "hero_copy",
    "operations_copy",
    "local_copy",
    "meta_description",
]

number_pattern = re.compile(r"\b\d+(?:\.\d+)?%?\b")

for idx, row in df.iterrows():
    for field in content_fields:
        text = str(row[field])
        if number_pattern.search(text):
            errors.append(
                f"Row {idx + 1} ({row['city']}): numeric claim found in {field}"
            )

# 5. Prohibited claim patterns
prohibited_patterns = [
    r"\bcustomers? in\b",
    r"\btrusted by\b",
    r"\bmarket leader\b",
    r"\bnumber one\b",
    r"\b#1\b",
]

for idx, row in df.iterrows():
    combined = " ".join(str(row[field]).lower() for field in content_fields)

    for pattern in prohibited_patterns:
        if re.search(pattern, combined):
            errors.append(
                f"Row {idx + 1} ({row['city']}): prohibited claim pattern '{pattern}'"
            )

if errors:
    print(f"FAILED: {len(errors)} validation issue(s)")
    print()
    for error in errors:
        print("✗", error)

    sys.exit(1)

print(f"✓ Required fields complete")
print(f"✓ Expected row count: {len(df)}")
print("✓ No unsupported numeric claims")
print("✓ No prohibited customer/market claims")
print(f"✓ {len(df)}/{len(df)} records passed validation")
