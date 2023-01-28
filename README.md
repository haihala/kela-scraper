# Kela-scraper

Tool to get a list of emails from Kela therapeut list.


## Setup

```sh
python -m venv venv
./venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Go to the kela therapeut list and download the page with all therapists
2. (while venv active) `python scrape.py <downloaded_page.htm> --fields email phone --location <name of the city you want to scrape for>`
