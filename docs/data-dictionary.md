# What the fields mean

This is a short guide to the public data. The dates and amounts are real. Worker, Property, Client and source-file labels are anonymous.

## Jobs and Tasks: `FactWorkItem`

| Field | Meaning |
|---|---|
| Billing Period Start / End | Start and end of the closed 14-day period |
| Work Item Key | Unique public ID for one Job or Task |
| Work Item Type | Job or Task |
| Service Date | Real service date from the source file |
| Property Key | Anonymous Property ID |
| Client | Client 1, Client 2 or Client 3 |
| Work Category | Broad category created from the private description before the description was removed |
| Worker Key | Anonymous assigned Worker ID |
| Default Worker Key | Anonymous default Worker ID |
| Assignment Overridden | Whether the assigned Worker was changed manually |
| Approved Client Price | Real amount approved for charging |
| Approved Worker Price | Real amount approved for worker pay |
| Cost | Real extra cost |
| Business Income | Client Price minus Worker Price minus Cost |
| Pricing Status | How the price or Task was handled |
| Price Approved At | Real approval time from the source file |
| Worker Price Overridden | Whether worker pay was changed manually |
| Ready For Billing | Whether the source system considered it ready |
| No Payment | Whether it was marked as no payment |
| Public Holiday Flag | Whether the source carried a public-holiday name |
| Reconciliation Variance | Difference after checking the financial rule; expected to be zero |
| Source File | Safe public label for the period file |

## Manual adjustments: `FactManualEntry`

| Field | Meaning |
|---|---|
| Manual Entry Key | Anonymous ID for one adjustment |
| Service Date | Real source date |
| Adjustment Category | Positive or negative adjustment |
| Allocation | Person or Business |
| Worker Key | Anonymous Worker when the adjustment belongs to a person |
| Approved Client Price | Real client-side adjustment |
| Approved Worker Price | Real worker-side adjustment |
| Cost | Real extra cost |
| Business Income | Financial result of the adjustment |
| Status | Active or cancelled |
| Approved Or Updated At | Real source audit time |

The table also has Billing Period, Reconciliation Variance and Source File fields that work the same way as the Work Item table.

## Property by period: `FactPropertyPeriodSnapshot`

| Field | Meaning |
|---|---|
| Property Key / Label | Anonymous Property identity |
| Billing Period Start / End | Period when the snapshot was seen |
| Job Count / Task Count | Activity recorded for the Property in that period |
| Bedrooms / Bathrooms | Available Property size information |
| Quoted Client Price | Real client quote |
| Quoted Worker Price | Real worker quote |
| Quote Start / End | Real source dates for the quote |

## The smaller supporting tables

- `DimDate`: Date, Year, Month, Month Start, Month End, Full or Partial Month, Week Start, Day and Weekend flag.
- `DimBillingPeriod`: Period dates, display label and order number.
- `DimWorker`: Worker Key and Worker 01–08 label.
- `DimClient`: Client 1, Client 2 and Client 3.
- `DimProperty`: Property Key and public Property label.
