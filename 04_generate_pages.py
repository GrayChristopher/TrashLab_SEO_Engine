import csv
import os
import subprocess
import sys
from jinja2 import Environment, FileSystemLoader

DATA_FILE = "02_generated_content.csv"
VALIDATOR_FILE = "03_validate_content.py"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"

print("Running content validation...")

result = subprocess.run(
    [sys.executable, VALIDATOR_FILE]
)

if result.returncode != 0:
    print("Generation stopped: content failed validation.")
    sys.exit(1)

print()

os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR)
)

template = env.get_template("page.html")

with open(
    DATA_FILE,
    newline="",
    encoding="utf-8"
) as f:
    markets = list(csv.DictReader(f))

print("PROGRAMMATIC SEO GENERATION")
print("-" * 40)

generated = 0

for market in markets:
    html = template.render(
        city=market["city"],
        state=market["state"],
        keyword=market["keyword"],
        primary_segment=market["primary_segment"],
        secondary_segment=market["secondary_segment"],
        market_angle=market["market_angle"],
        hero_copy=market["hero_copy"],
        operations_copy=market["operations_copy"],
        local_copy=market["local_copy"],
        meta_description=market["meta_description"]
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        f'{market["slug"]}.html'
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    generated += 1

    print(
        f'✓ {market["city"]}, {market["state"]} '
        f'→ {market["slug"]}.html'
    )

print("-" * 40)
print(
    f"GENERATION COMPLETE: "
    f"{generated}/{len(markets)} pages generated"
)
