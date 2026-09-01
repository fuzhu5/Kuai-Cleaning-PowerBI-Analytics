# About the anonymised data

The CSV files in `sample/` keep the real dates and financial values from the cleaning-business exports. Identifying details were removed or renamed for the portfolio.

## What was changed

- Worker and Property IDs were replaced.
- Names, addresses, phone numbers, links and free-text instructions were removed.
- Source filenames were replaced with simple period labels.
- Dates and money values were kept unchanged.
- The business's three Clients are shown as Client 1, Client 2 and Client 3.

These changes allow the Power Query, model and DAX to be reviewed without publishing identities. The repository does publish the business's real totals for the covered period.

## Files in the folder

| File | What one row means | Rows |
|---|---|---:|
| `work_items.csv` | One Job or Task | 775 |
| `manual_entries.csv` | One manual financial adjustment | 41 |
| `property_periods.csv` | One Property in one Billing Period | 350 |
| `data_profile.json` | Counts, totals and check results for the release | One file |
| `business_insights.json` | Worker, Client and previous-period facts used in the written analysis | One file |

## What not to add

Do not copy the original exports into this repository. Do not add a file containing the mapping between anonymous IDs and real IDs. Do not publish a PBIX that has already loaded the private source.

If a new public field is added, run both Python checks again and review the field in plain language: could this identify a person, an address, a client or a private business instruction?
