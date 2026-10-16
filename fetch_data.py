"""Refresh the rent snapshot from SpareRoom's published city averages."""

import argparse
import csv
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
SOURCE_URL = "https://www.spareroom.co.uk/content/info-landlords/average-rent-uk-top-cities/"
CITY_NAMES = {
    "London (Inner)", "Edinburgh", "Bath", "Oxford", "Cambridge", "York",
    "Bristol", "Manchester", "Gloucester", "Birmingham", "Leeds",
    "Liverpool", "Sheffield", "Hull",
}
CITY_ALIASES = {"Kingston-upon-Hull (Hull)": "Hull"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.page_text = []
        self.current_row = None
        self.current_cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.current_row = []
        elif tag in {"td", "th"} and self.current_row is not None:
            self.current_cell = []

    def handle_endtag(self, tag):
        if tag in {"td", "th"} and self.current_cell is not None:
            self.current_row.append(" ".join("".join(self.current_cell).split()))
            self.current_cell = None
        elif tag == "tr" and self.current_row is not None:
            self.rows.append(self.current_row)
            self.current_row = None

    def handle_data(self, data):
        self.page_text.append(data)
        if self.current_cell is not None:
            self.current_cell.append(data)


def fetch_rents():
    request = Request(
        SOURCE_URL,
        headers={"User-Agent": "GraduateRentAffordability/1.0 (data refresh)"},
    )
    with urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8", errors="replace")

    parser = PageParser()
    parser.feed(page)
    header_index = next(
        (
            index
            for index, row in enumerate(parser.rows)
            if any(cell.strip().lower() == "city" for cell in row)
            and any("average monthly room rent" in cell.lower() for cell in row)
        ),
        None,
    )
    if header_index is None:
        raise RuntimeError("Could not find the city rent table on the SpareRoom page")

    header = parser.rows[header_index]
    city_column = next(i for i, cell in enumerate(header) if cell.strip().lower() == "city")
    rent_column = next(i for i, cell in enumerate(header) if "average monthly room rent" in cell.lower())
    rents = {}
    for row in parser.rows[header_index + 1:]:
        if max(city_column, rent_column) >= len(row):
            continue
        city = CITY_ALIASES.get(row[city_column].strip(), row[city_column].strip())
        amount = re.search(r"[\d,]+", row[rent_column])
        if city in CITY_NAMES and amount:
            rents[city] = int(amount.group().replace(",", ""))

    if rents.keys() != CITY_NAMES:
        missing = sorted(CITY_NAMES - rents.keys())
        raise RuntimeError(f"SpareRoom rent table is missing expected cities: {missing}")

    page_text = " ".join(parser.page_text)
    period_match = re.search(r"with\s+(Q[1-4]\s+\d{4})\s+data", page_text, re.IGNORECASE)
    if not period_match:
        raise RuntimeError("Could not identify the data quarter on the SpareRoom page")
    period = " ".join(period_match.group(1).upper().split())
    return rents, period


def main():
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "rents.csv",
        help="where to save the rent snapshot (default: data/rents.csv)",
    )
    args = argument_parser.parse_args()

    rents, period = fetch_rents()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as rent_file:
        writer = csv.writer(rent_file)
        writer.writerow(("city", "rent_gbp", "period", "source_url"))
        for city in sorted(rents):
            writer.writerow((city, rents[city], period, SOURCE_URL))
    print(f"Saved {len(rents)} city rents for {period} to {args.output}")


if __name__ == "__main__":
    main()