import logging
import time
from pathlib import Path

import diskcache as dc
import numpy as np
import pandas as pd
import requests
import typer
from bs4 import BeautifulSoup
from sane_rich_logging import setup_logging

app = typer.Typer()

DEFAULT_URL = "https://www.fuelfinder.dk/listprices.php"

# Set up the cache directory in ~/.cache
cache_directory = Path.home() / ".cache" / "fuelfinder_cache"
cache = dc.Cache(cache_directory)

TTL = 300  # Time-to-live for cache entries in seconds (5 minutes)


def fetch_gas_prices(url: str):
    # Check if the response is in the cache
    if url in cache and "timestamp" in cache:
        current_time = time.time()
        cached_time = cache["timestamp"]
        logging.debug(f"Cache found for URL: {url}, checking age...")

        # Check if the cached data is still valid
        if current_time - cached_time < TTL:
            logging.debug("Cache is still valid, returning cached data.")
            return cache[url]

    logging.debug("Cache is expired or not found, fetching data from the URL.")

    # Define headers to mimic a browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Make the request with headers and parse the HTML content using BeautifulSoup
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the table headers and rows
    table = soup.find("table")
    headers = [header.get_text(strip=True) for header in table.find_all("th")]
    rows = [
        [cell.get_text(strip=True) for cell in row.find_all("td")]
        for row in table.find_all("tr")[1:]
    ]
    logging.debug("Successfully fetched and parsed the table from the URL.")

    # Create DataFrame, clean up data, set index, and convert dtypes in a chain
    df = (
        pd.DataFrame(rows, columns=headers)
        .replace(r"\u200b", "", regex=True)
        .replace("", np.nan)
        .set_index("Benzinselskab")
        .apply(pd.to_numeric, errors="coerce", axis=1)
        .convert_dtypes()
    )

    # Cache the response with the current timestamp
    cache[url] = df
    cache["timestamp"] = time.time()
    logging.debug("Data has been cached successfully.")

    return df


@app.command()
def main(
    url: str = typer.Option(
        DEFAULT_URL,
        envvar="FUELLIST_URL",
        help="The URL to fetch gas prices from, can also be set via the environment variable FUELLIST_URL.",
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging."),
):
    if debug:
        setup_logging(log_level="DEBUG")
    try:
        gas_prices_df = fetch_gas_prices(url)
        print(gas_prices_df.to_json())
    except requests.exceptions.HTTPError as e:
        logging.error(f"An HTTP error occurred: {e}")
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    app()
