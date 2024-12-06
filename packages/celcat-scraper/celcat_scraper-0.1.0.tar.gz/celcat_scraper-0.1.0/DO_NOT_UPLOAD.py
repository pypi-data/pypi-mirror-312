import asyncio
from datetime import datetime, timedelta

from celcat_scraper import CelcatConfig, CelcatScraperAsync
import logging

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

async def main() -> None:
    """Retrieve Celcat calendar events from today to next week"""

    # Login details
    config = CelcatConfig(
        url = "https://services-web.cyu.fr",
        username = "e-ecoriou",
        password = "CE_etienne78_GY",
        include_holidays =True,
        rate_limit=3
    )

    # Create scraper instance and get events
    async with CelcatScraperAsync(config) as scraper:
        start_date = datetime.now()
        end_date = start_date + timedelta(days=2)

        file_path = 'store.json'
        events = scraper.deserialize_events(file_path)

        events = await scraper.get_calendar_events(start_date, end_date, previous_events=events)

        for event in events:
            print(event)
            print(f"Event: {event['category']} - {event['course']}")
            print(f"Time: {event['start']} to {event['end']}")
            print(f"Location: {', '.join(event['rooms'])}")
            print("---")

        scraper.serialize_events(events, file_path)

if __name__ == "__main__":
    asyncio.run(main())
