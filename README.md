# TrashLab Programmatic SEO Engine

A working programmatic SEO pipeline that generates 25 landing pages for a waste-hauler software keyword cluster using structured market data, constrained content generation, deterministic validation, and a reusable HTML template.

## Overview

The pipeline follows this architecture:

```text
Structured Market Data
        ↓
Constrained Content Generation
        ↓
Saved Structured Content
        ↓
Deterministic Validation
        ↓
Reusable HTML Template
        ↓
25 Generated SEO Pages
```

The keyword cluster used for this prototype is:

**Waste Hauler Software in [City, Texas]**

The objective is to demonstrate a repeatable generation system rather than manually creating individual landing pages.

## Project Structure

```text
01_markets.csv
02_generated_content.csv
03_validate_content.py
04_generate_pages.py
page.html
Output.zip
requirements.txt
README.md
```

### 01_markets.csv

Structured source data for 25 Texas markets.

Fields include:

- city
- state
- slug
- keyword
- primary segment
- secondary segment
- market angle

### 02_generated_content.csv

Stores the approved content layer used to generate each page.

Content fields include:

- hero copy
- operations copy
- local copy
- meta description

For this prototype, an LLM was used during development to help create the constrained content layer from structured inputs. The approved outputs were then persisted in the CSV so the publishing workflow remains reproducible and does not require a live LLM call.

In production, this layer could be replaced with an API-based generation step while retaining the same schema, validation, and publishing layers.

### 03_validate_content.py

Runs deterministic QA before any pages are generated.

The validator checks:

- required fields
- expected record count
- blank values
- unsupported numeric claims
- prohibited customer or market claims

If validation fails, page generation stops.

### 04_generate_pages.py

Runs the publishing pipeline.

It:

1. Executes the validation layer.
2. Loads the approved structured content.
3. Loads the reusable HTML template.
4. Injects each market's content into the template.
5. Generates one HTML page per market.

### page.html

Reusable Jinja HTML template shared by all 25 pages.

The template controls page structure and presentation while the CSV controls market-specific content.

### Output.zip

Contains the 25 generated sample HTML pages produced by the pipeline.

Running `04_generate_pages.py` recreates these pages in an `output/` directory.

## Run the Pipeline

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python 04_generate_pages.py
```

Successful execution validates the content and generates all 25 HTML pages.

## Accuracy Guardrails

The prototype deliberately avoids unsupported local claims.

Generated content does not invent:

- customer counts
- market statistics
- local regulations
- company adoption claims
- unsupported city-specific facts

Missing market intelligence is treated as unknown rather than filled with fabricated content.

This keeps the generation layer useful while separating generative flexibility from factual validation.

## Scaling the System

The same architecture can expand from 25 pages to hundreds or thousands of market/service combinations.

```text
25 Texas city pages
        ↓
250 city + service combinations
        ↓
2,500+ market/service pages
```

At larger scale I would add:

- keyword research and search-volume prioritization
- authoritative geographic and market datasets
- automated LLM generation through an API
- duplicate-content detection
- content quality scoring
- internal-link generation
- canonical and technical SEO controls
- CMS publishing
- Search Console performance feedback
- scheduled content refreshes

A production architecture could look like:

```text
Keyword / Market Dataset
        ↓
Structured Content Brief
        ↓
LLM Generation API
        ↓
Deterministic Validation
        ↓
Quality Threshold / Review
        ↓
CMS Template
        ↓
Published SEO Page
        ↓
Search Performance Feedback
```

## Design Principle

**Use AI where generative flexibility is valuable. Use deterministic systems where reproducibility and factual accuracy matter.**
