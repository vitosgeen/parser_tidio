# Tidio Conversation Scraper

This script is designed for scraping and parsing conversation data from Tidio.

## Features

- Scrapes conversation data from Tidio
- Parses the scraped data for analysis
- Outputs the parsed data in a structured format

## fill .env
get key from page https://www.tidio.com/panel/inbox/conversations/solved/ with 
web developer tool when click "Export transcript to .CSV" 

must install chromium driver

## create venv 
```
python -m venv venv
source venv/bin/activate
# On Windows, use `venv\Scripts\activate`
```

## Installation
```
pip install -r requirements.txt
```

## Run
```
venv/bin/python main.py
```

## License

This project is licensed under the MIT License.