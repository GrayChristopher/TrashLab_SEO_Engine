# TrashLab Programmatic SEO Engine

A working programmatic SEO pipeline that generates 25 landing pages for a
waste-hauler software keyword cluster from structured market data.

Built for the TrashLab Director, Demand Generation take-home exercise.

## Overview

The system separates page generation into four layers:

```text
Structured Market Data
        ↓
Constrained Content Generation
        ↓
Content Validation
        ↓
Reusable HTML Template
        ↓
25 Generated SEO Pages
```

The goal is to make page creation scalable without allowing the generation
layer to invent unsupported local facts.

## Keyword Cluster

The sample cluster targets:

**Waste Hauler Software in [City, Texas]**

Examples:

- Waste Hauler Software in Austin, Texas
- Waste Hauler Software in Houston, Texas
- Waste Hauler Software in Dallas, Texas

The dataset contains 25 Texas markets.

## Project Structure

```text
TrashLab-SEO-Engine/
├── markets.csv
├── generated_content.csv
├── generate_pages.py
├── validate_content.py
├── requirements.txt
├── templates/
│   └── page.html
└── output/
    ├── austin-tx.html
    ├── houston-tx.html
    ├── dallas-tx.html
    └── ... 25 generated pages
```

## 1. Structured Inputs

`markets.csv` contains the structured inputs used to define each page.

Core fields include:

- city
- state
- slug
- keyword
- primary_segment
- secondary_segment
- market_angle

This separates market and targeting decisions from presentation.

## 2. Content Generation

The content layer transforms structured inputs into four page-level content fields:

- hero_copy
- operations_copy
- local_copy
- meta_description

For this prototype, an LLM was used during development to help create the
constrained content layer and the resulting approved content is persisted in
`generated_content.csv`.

The publishing pipeline does not require a live LLM call.

In production, this layer could be replaced by an API-based generation step
while retaining the same structured schema, validation layer, and publishing workflow.

### Generation Guardrails

The content-generation process prohibits:

- invented statistics
- invented customers
- unsupported local regulations
- unsupported market characteristics
- claims that TrashLab has customers in a specific city
- keyword stuffing

This keeps generative flexibility separate from factual validation.

## 3. Content Validation

`validate_content.py` runs before pages can be generated.

The validator checks:

- required fields are present
- all 25 expected records exist
- required content fields are populated
- unsupported numeric claims are absent
- prohibited customer and market claims are absent

If validation fails, page generation stops.

## 4. Page Generation

`generate_pages.py`:

1. Runs the validation layer
2. Loads the approved structured content
3. Loads the reusable Jinja template
4. Injects each market's content variables
5. Writes one HTML page per market

The same template is used across all 25 pages while structured inputs control
the market, segment, operational angle, metadata, and page copy.

## 5. HTML Template

`templates/page.html` contains the reusable page design.

The template includes:

- SEO title and meta description
- market-specific hero
- segment-specific positioning
- operational use cases
- local-market section
- content accuracy guardrail
- conversion CTA
- responsive styling

The template is intentionally lightweight and dependency-free.

## Running the Pipeline

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate all pages:

```bash
python generate_pages.py
```

A successful run validates the content before generating the pages:

```text
CONTENT VALIDATION
----------------------------------------
✓ Required fields complete
✓ Expected row count: 25
✓ No unsupported numeric claims
✓ No prohibited customer/market claims
✓ 25/25 records passed validation

PROGRAMMATIC SEO GENERATION
----------------------------------------
...
GENERATION COMPLETE: 25/25 pages generated
```

Generated pages are written to `output/`.

## Scaling the System

The prototype uses 25 Texas markets, but page count is not hard-coded into the
template architecture.

Scaling means expanding the structured input layer rather than manually
creating additional pages.

For example:

```text
25 markets
    ↓
250 markets
    ↓
2,500 market / service combinations
```

At larger scale I would add:

- programmatic keyword research
- authoritative geographic and market datasets
- CMS publishing integration
- internal-link generation
- canonical URL management
- duplicate-content detection
- generation quality scoring
- automated SEO QA
- Search Console performance feedback
- scheduled content refreshes

## Production Architecture

```text
Keyword / Market Dataset
        ↓
Structured Content Brief
        ↓
LLM Generation API
        ↓
Deterministic Validation
        ↓
Human Review / Quality Threshold
        ↓
CMS Template
        ↓
Published SEO Page
        ↓
Search Performance Feedback
```

The key design principle is that the LLM is a generation component, not the
source of truth.

Structured data and deterministic validation remain responsible for factual
constraints and publishing safety.

## Design Principle

**Use AI where generative flexibility is valuable. Use deterministic systems
where reproducibility and factual accuracy matter.**
