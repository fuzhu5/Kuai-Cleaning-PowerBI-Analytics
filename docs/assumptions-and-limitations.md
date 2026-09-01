# What to keep in mind

## Choices made in the analysis

- Active manual adjustments are included in money totals.
- Jobs and Tasks are combined because each row represents one piece of work and the exported money fields match.
- Manual adjustments stay separate because they are not always service visits.
- Billing Period is the main time view because that is how the business closes its billing.
- Month is optional and edge months are marked as partial.
- Business Income is treated as Client Revenue minus Worker Payout minus Other Cost because every supplied row follows that rule.

## Things the dashboard should not claim

### It cannot measure worker productivity

The data shows Work Item count and money. It does not show hours worked, travel time, difficulty, rework, complaints or service quality.

### It cannot explain cause by itself

The dashboard can show that revenue fell or a Client changed. It cannot prove why without operational context from the owner.

### It should not be used for a confident forecast

Ten Billing Periods are enough to describe recent movement. They are not enough for a reliable long-term forecast.

## Public-data limits

The GitHub sample keeps the real dates and financial amounts. This makes the analysis truthful, but it also means the public repository reveals the business's actual totals for this period. Worker, Property and Client identities remain anonymous.

The privacy scan lowers the chance of accidental disclosure, but it is not a formal privacy certification. Any newly added column should be reviewed before publishing.

## Technical status

The Python scripts and public files have passed their local checks. The Power Query, DAX and report layout remain a draft until they are run and visually checked in Power BI Desktop.
