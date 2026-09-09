import pandas as pd
import re
import sys

INPUT_FILE = "02_generated_content.csv"

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

CONTENT_FIELDS = [
    "hero_copy",
    "operations_copy",
    "local_copy",
    "meta_description",
]

PROHIBITED_PATTERNS = [
    r"\bcustomers? in\b",
    r"\btrusted by\b",
    r"\bmarket leader\b",
    r"\bnumber one\b",
    r"\b#1\b",
]

NUMBER_PATTERN = re.compile(r"\b\d+(?:\.\d+)?%?\b")


def main():
    print("CONTENT VALIDATION")
    print("-" * 40)

    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"✗ Missing input file: {INPUT_FILE}")
        sys.exit(1)

    errors = []

    # Check required columns
    for field in REQUIRED_FIELDS:
        if field not in df.columns:
            errors.append(f"Missing column: {field}")

    # Stop early if schema is broken
    if errors:
        print(f"FAILED: {len(errors)} validation issue(s)")
        print()

        for error in errors:
            print("✗", error)

        sys.exit(1)

    # Expected sample size
    if len(df) != 25:
        errors.append(f"Expected 25 rows, found {len(df)}")

    # Blank required values
    for field in REQUIRED_FIELDS:
        blank_count = (
            df[field].isna().sum()
            + (df[field].fillna("").astype(str).str.strip() == "").sum()
        )

        if blank_count > 0:
            errors.append(f"{field}: {blank_count} blank values")

    # Block unsupported numeric claims in generated copy
    for idx, row in df.iterrows():
        for field in CONTENT_FIELDS:
            text = str(row[field])

            if NUMBER_PATTERN.search(text):
                errors.append(
                    f"Row {idx + 1} ({row['city']}): "
                    f"numeric claim found in {field}"
                )

    # Block risky unsupported marketing claims
    for idx, row in df.iterrows():
        combined = " ".join(
            str(row[field]).lower()
            for field in CONTENT_FIELDS
        )

        for pattern in PROHIBITED_PATTERNS:
            if re.search(pattern, combined):
                errors.append(
                    f"Row {idx + 1} ({row['city']}): "
                    f"prohibited claim pattern '{pattern}'"
                )

    if errors:
        print(f"FAILED: {len(errors)} validation issue(s)")
        print()

        for error in errors:
            print("✗", error)

        sys.exit(1)

    print("✓ Required fields complete")
    print(f"✓ Expected row count: {len(df)}")
    print("✓ No unsupported numeric claims")
    print("✓ No prohibited customer/market claims")
    print(f"✓ {len(df)}/{len(df)} records passed validation")


if __name__ == "__main__":
    main()
