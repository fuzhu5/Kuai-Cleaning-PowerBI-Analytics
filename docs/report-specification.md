# Dashboard plan

The report has nine short pages. Each page answers one business question and avoids long explanation boxes.

| Page | Question | Main visuals |
|---|---|---|
| 1. Business Overview | Is the business improving? | Revenue, Business Income, margin and Work Items; latest vs previous Billing Period; revenue and income trend |
| 2. Monthly Performance | What changed each month? | Monthly KPI cards; revenue and income trend; Work Items and revenue per item; month table |
| 3. Billing Period Trend | What changed every 14 days? | Revenue, income and margin by Billing Period; previous-period changes; adjustment impact |
| 4. Worker Performance | How much did each worker do? | Items vs team average; Jobs and Tasks; pay; income; latest vs previous period |
| 5. Client Analysis | Which Client drives the result? | Revenue share; margin; Work Items; Properties; latest vs previous period |
| 6. Property Analysis | Which Properties need attention? | Top revenue; low-margin Properties; work volume; quote vs approved price; drill-through table |
| 7. Jobs and Tasks | What type of work changed? | Job and Task mix; category trend; average value; Task status; weekend share |
| 8. Billing and Adjustments | Did one-off entries change the result? | Work Item income to final income waterfall; adjustment trend; overrides; review table |
| 9. Billing Checks | Can the numbers be trusted? | Pass or Fail cards; row counts; negative amounts; missing keys; exception table |

## Page rules

- Use no more than five KPI cards on a page.
- Put the comparison in the title, such as “vs previous Billing Period”.
- Keep one short note only when the chart could be misunderstood.
- Use green and red for change, not decoration.
- Put filters in the same place. Use Billing Period on period pages and Month on the Monthly page.
- Let users click a Client, Worker or Property to filter the page.
- Add a reset button.

## Monthly page

Use Month as the main axis and show:

- Revenue;
- Business Income;
- margin;
- Work Items;
- revenue per Work Item;
- change from the previous comparable month.

March and August must show a clear `Partial` badge. Do not show a full-month percentage change for those two months.

## Worker page

Use one row per worker with these columns:

`Worker | Work Items | Jobs | Tasks | Revenue | Worker Pay | Business Income | Revenue per Item | Items vs Team Average | Latest vs Previous`

Add a single note: “Workload only. Hours, travel and quality are not available.”

## Client page

Show Client 1, Client 2 and Client 3. For each Client, show Work Item revenue, revenue share, margin, Work Items, Properties and latest-period change. Manual entries have no Client, so they stay out of this page.

## Property page

Start with two lists:

- highest revenue Properties;
- Properties with meaningful revenue and margin below 30%.

Clicking a Property should open its Billing Period history, Work Items, prices and margin.

## Billing Checks page

Keep the financial rule visible:

```text
Client Revenue - Worker Payout - Other Cost = Business Income
```

Show a large Pass or Fail result, followed by the records that need review.
