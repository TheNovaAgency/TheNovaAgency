# Business Data Scraper

A Python-based scraper for gathering UK business data by town or postcode, focused on Essex. Collects company information from multiple sources including Companies House and Google Places API.

## Data Collected

- Company name
- Telephone
- Email
- Address
- Main Contact
- Type of Business
- Open Hours

## Project Structure

```
src/scraper/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── company.py
├── connectors/
│   ├── __init__.py
│   ├── companies_house.py
│   └── google_places.py
├── geocoding/
│   ├── __init__.py
│   └── geocoder.py
├── orchestrator/
│   ├── __init__.py
│   └── scraper.py
└── export/
    ├── __init__.py
    └── exporter.py
tests/
config/
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your API keys:
   ```
   COMPANIES_HOUSE_API_KEY=your_key_here
   GOOGLE_PLACES_API_KEY=your_key_here
   ```

## Usage

```python
from src.scraper.orchestrator.scraper import ScraperOrchestrator

orchestrator = ScraperOrchestrator()
results = orchestrator.scrape_by_postcode("CM1 1HT")
orchestrator.export_csv(results, "output/chelmsford_businesses.csv")
```

Or by town:

```python
results = orchestrator.scrape_by_town("Chelmsford")
orchestrator.export_json(results, "output/chelmsford_businesses.json")
```

## API Keys

- [Companies House API](https://developer.company-information.service.gov.uk/)
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview)

## License

Proprietary - TheNovaAgency
