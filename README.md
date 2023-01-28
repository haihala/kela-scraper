# Kela-scraper

Tool to get a list of emails from Kela therapist list.

## Setup

1. Install dependencies (preferably in a venv)
2. Run scrape.py

On linux/WSL:

```sh
python -m venv venv
./venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Go to the kela therapist list and download the page with all therapists (should be about 500 names)
2. See (while venv active) `python scrape.py --help`

## Troubleshooting

- File has to be utf-8 encoded.
- This will throw out websites in the email field
- The kela site is not really maintained and isn't exactly reliable with it's data
