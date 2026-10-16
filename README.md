# UK Graduate Rent Affordability

How much of a typical graduate's take-home pay goes on a room in different UK cities? This project compares published room rents with a £28,500 graduate salary and turns the results into a chart.

![Chart comparing rent affordability across UK cities](chart.png)

## Run it

Install the one required package and make the chart:

```bash
python -m pip install -r requirements.txt
python analysis.py
```

The rent figures are saved in `data/rents.csv`, so the chart can be recreated without an internet connection. To refresh them from SpareRoom first, run:

```bash
python fetch_data.py
python analysis.py
```

The refresh script reads SpareRoom's published city-rent table, records the latest quarter in the CSV, and keeps the source link with each row. The chart is written to `chart.png`.

## What the numbers mean

- **Salary:** £28,500, the median for full-time first-degree graduates in the 2022/23 HESA Graduate Outcomes cohort, around 15 months after graduating.
- **Take-home pay:** estimated after Income Tax and National Insurance using the 2025/26 England rates. This works out to about £2,003 a month.
- **Rent:** SpareRoom's average monthly room rent, including bills. The checked-in snapshot is Q3 2026.
- **Comparison:** monthly rent as a share of estimated take-home pay. The 30% line is a common rule of thumb, not a guarantee that a room is affordable.

The model uses one salary for every city. It does not include student loan repayments, pension contributions, or Scotland's different income-tax bands, so treat the percentages as a simple comparison rather than a personal budget.

## Sources

- Room rents: [SpareRoom average rents in UK cities](https://www.spareroom.co.uk/content/info-landlords/average-rent-uk-top-cities/)
- Graduate salary: [HESA Graduate Outcomes salary statistics](https://www.hesa.ac.uk/news/17-07-2025/sb272-higher-education-graduate-outcomes-statistics/salary)
- Tax and National Insurance: [Income Tax rates](https://www.gov.uk/income-tax-rates) and [National Insurance rates](https://www.gov.uk/national-insurance-rates-letters)

## GitHub files

Keep `analysis.py`, `fetch_data.py`, `data/rents.csv`, `requirements.txt`, `README.md`, `linkedin_post.md`, and `chart.png` in the repository. The CSV lets people rerun the analysis even if the source website is unavailable; the PNG appears in the README, and `linkedin_post.md` contains a ready-to-edit caption for sharing it.

Built by [Yogesh Dahiwal](https://www.linkedin.com/in/yogesh-dahiwal-145b2a245) · [Portfolio](https://yogesh-dahiwal.netlify.app)
