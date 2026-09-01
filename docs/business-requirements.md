# What the dashboard needs to answer

## Who this is for

The main user is the cleaning-business owner. The person preparing billing and the person assigning workers may also use it.

They should not need to understand the source files. The dashboard should tell them what happened, what changed, and where they need to look next.

## The main questions

1. How much revenue and Business Income did the latest Billing Period produce?
2. How does that compare with the previous Billing Period?
3. Did the result change because of work volume, average value or manual adjustments?
4. How many Jobs and Tasks did each worker complete?
5. How does each worker compare with the team average?
6. How much was each worker paid, and what was the average per Work Item?
7. Which Clients and Properties bring in the most revenue?
8. Which Clients grew or fell compared with the previous Billing Period?
9. Are the financial numbers balanced and ready to review?
10. Which records need a billing review?

## The numbers and what they mean

| Number | Plain meaning | How it is calculated |
|---|---|---|
| Client Revenue | Amount approved to charge | Work Item revenue plus active manual revenue adjustments |
| Worker Payout | Amount approved to pay workers | Work Item pay plus active manual worker adjustments |
| Other Cost | Extra business costs | Costs recorded against Work Items and active manual entries |
| Business Income | Amount left for the business | Client Revenue minus Worker Payout minus Other Cost |
| Business Margin | Share of revenue left for the business | Business Income divided by Client Revenue |
| Work Items | Jobs and Tasks completed or recorded | Count of rows in the Work Item table |
| Average Work Items per Worker | A simple workload reference | Work Items divided by active workers |
| Assignment Override Rate | How often the default worker was changed | Overridden Work Items divided by all Work Items |
| Client Revenue Share | Dependence on each Client | Client revenue divided by all Work Item revenue |
| Client Count | Number of Clients in the business | Distinct Client labels in Work Items; expected result is three |
| Financial Balance | Whether the four money fields agree | Revenue minus pay minus cost minus Business Income |

## Time comparison rule

The default comparison is the latest closed 14-day Billing Period against the previous closed Billing Period.

Month is an optional view. If the first or last month is incomplete, the report must say so. It should never compare a partial month with a full month without a warning or a like-for-like measure.

## When the project is ready

The report is ready to present when:

- all ten period files load without manual repair;
- empty Manual Entry files do not break the refresh;
- financial totals balance within A$0.01;
- every public Work Item ID is unique;
- Worker, Client and Property totals agree with the source profile;
- the previous-period cards return the expected values;
- the model contains Client 1, Client 2 and Client 3;
- every page opens cleanly in Power BI Desktop.
