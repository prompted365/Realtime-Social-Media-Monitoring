# Real-Time Web Scraping for Sentiment Analysis of Any Brand Name using Multi-Threading

## Overview

This project performs real-time web scraping and sentiment analysis on any specified brand name or topic across various social media platforms. It utilizes multi-threading for parallel processing, Playwright for web automation, SQLite for data storage, Pandas for data manipulation, and Transformers for sentiment analysis using a pre-trained model.

## Purpose

The purpose of this project is to provide users with real-time sentiment analysis and the number of posts or comments related to any given brand name or topic. Users are alerted via email in case of any significant changes in sentiment.

## Prerequisites

- **Programming Languages**: Python
- **Libraries**: transformers, playwright, sqlite3, pandas, smtlib, etc. (refer to Requirements.txt)
- **Web Scraping Knowledge**: Playwright
- **Virtual Environment**: Optional
- **Python Version**: 3.9+

## Setup

1. **Playwright Setup**
    - Install Playwright: `pip install playwright && playwright install chromium`
    - Browser Configuration: Use Chromium if possible
    - Headless Mode: False
    - Usage: Web automation for login to websites like Twitter, Facebook, or LinkedIn and site context scraping after login.

2. **Pandas Setup**
    - Installation: `pip install pandas`
    - Usage: Data manipulation, creating DataFrames, and sentiment analysis.

3. **SQLite Setup**
    - Installation: Pre-built with Python
    - Usage: Storing scraped data and sentiment analysis results.

4. **Transformers Setup**
    - Installation: `pip install transformers`
    - Setup: `pipeline('sentiment analysis')`
    - Usage: Implementing sentiment analysis on scraped text.

5. **Multi-Threaded Setup**
    - Usage: Parallel processing of multiple threads for simultaneous web scraping.

6. **Facebook Scraping Module**
    - Prerequisites: Facebook login account
    - Scraping: Extract live posts of the latest searched brands or names
    - Storage: SQLite3 database
    - API: No external API used

7. **Twitter Scraping Module**
    - Prerequisites: Twitter login account
    - Scraping: Extract live posts of the latest searched brands or names
    - Storage: SQLite3 database
    - API: No external API used

8. **Reddit Scraping Module**
    - Prerequisites: No login required
    - Scraping: Extract live posts of the latest searched brands or names
    - Storage: SQLite3 database
    - API: No external API used

9. **Quora Scraping Module**
    - Prerequisites: No login required
    - Scraping: Extract live posts of the latest searched brands or names
    - Storage: SQLite3 database
    - API: No external API used

## How it Works

1. Run `python main.py <query>` to launch the orchestrator. Agents are loaded automatically from the `agents/` package and executed concurrently.

2. Use the `--limit` flag to control the number of posts scraped per agent. Results are written to the SQLite database defined by `SOCIAL_DB_PATH` (defaults to `social_media.db`).

3. Sentiment analysis is performed via the analytics pipeline and stored alongside raw posts.

## Interface

Command Line Interface (CLI) - Can be implemented in GUI or Web-based interfaces.

## Additional Information

- Sentiment Analysis Model: [Transformers documentation](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)

### Required Environment Variables

Set the following variables before running the scrapers:

- `TWITTER_USERNAME` – username or email used for login
- `TWITTER_PASSWORD` – corresponding password
- `EMAIL_SENDER` – address used to send notification emails
- `EMAIL_PASSWORD` – password for the sending account

If these variables are missing, the Twitter and Facebook scrapers and the email sender raise a `ValueError`.

## Testing & Quality

Run `flake8` followed by `pytest` before committing changes:

```bash
flake8
pytest
```

## Development Setup

This repository includes a `.gitignore` file that excludes typical temporary files such as `__pycache__/`, `*.db`, and `.env` entries. Ensure your local environment respects these rules to keep commits clean.

