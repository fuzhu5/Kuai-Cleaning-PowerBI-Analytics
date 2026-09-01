# How to explain this project in an interview

## A short introduction

I built this project around a real cleaning-business workflow and a system I developed. The data arrived as four types of CSV across 14-day Billing Periods. My aim was to help the owner understand revenue, Business Income, worker workload, Clients, Properties and billing adjustments without manually comparing files.

I used Python to remove identifying fields while keeping the real dates and financial values, then checked the public files before release. In Power Query, I designed the repeated file import and handled empty files. In Power BI, I kept Jobs and Tasks together, kept manual adjustments separate, and treated Property data as a period snapshot. I then wrote DAX for worker averages, Client shares and previous Billing Period comparisons.

## The strongest business finding

The latest period looked weaker: revenue fell 2.0% and Business Income fell 3.3%. But the normal Work Items were slightly more valuable per item. The larger problem was a more negative manual adjustment. That changed the likely management action from “raise all prices” to “review the reason for the adjustments and the fall in work volume first”.

## Why Billing Period is the default

The business bills every 14 days, so that is the fairest direct comparison. Month is still available, but the first and last months are incomplete. I chose to label them clearly instead of pretending they were full months.

## How to explain the Worker page

The dashboard shows exactly how many Jobs and Tasks each Worker completed, the team average, average revenue and pay per Work Item, and each Worker's share of total work.

I would not call this productivity because the dataset has no hours, travel time or quality score. That limitation is part of the analysis, not a footnote.

## How to explain the Client page

The business has three Clients, shown publicly as Client 1, Client 2 and Client 3. The page compares their real revenue, margin, Work Items, Properties and latest-period change.

## Why the tables are separated

- Jobs and Tasks are combined because they share one work-item level and the same money fields.
- Manual adjustments stay separate because they may not represent a visit.
- Property data stays by Billing Period because quotes and activity can change over time.

## A simple live demo order

1. Open Business Overview and compare the latest two Billing Periods.
2. Show that average value per Work Item improved while manual adjustments worsened.
3. Open Workers and compare Worker 05 and Worker 06 with the team average.
4. Open Clients and show Client 1's fall and Client 3's growth.
5. Open Monthly Performance and explain why March and August are marked partial.
6. Finish on Billing Checks and show that the financial rule passes.
7. Open one Python block, one Power Query block and one DAX block to connect the report to the implementation.
