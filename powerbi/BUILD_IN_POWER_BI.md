# Build the report in Power BI Desktop

This guide starts with a blank Power BI Desktop file and ends with a PBIP that can be checked and shown in the portfolio.

## 1. Save a new Power BI project

1. Open Power BI Desktop on Windows.
2. Create a blank report.
3. Save it as a Power BI Project (`.pbip`) inside this `powerbi` folder.
4. Keep credentials, cache files and PBIX files out of GitHub.

## 2. Load the public CSV files

For each file in `power-query/public-model`, create a Blank Query and paste the file into Advanced Editor. Name the query after the filename without `.pq`.

Use this order:

1. `pSampleDataFolder`
2. `FactWorkItem`
3. `FactManualEntry`
4. `FactPropertyPeriodSnapshot`
5. `DimProperty`
6. `DimWorker`
7. `DimClient`
8. `DimBillingPeriod`
9. `DimDate`
10. `DataQualityChecks`

Change `pSampleDataFolder` so it points to the repository's `data\sample` folder on your computer.

Load the detailed tables, supporting tables and Data Quality table. The folder setting itself does not need to appear in the report.

The files in `power-query/private-pipeline` show how the original repeated period files can be imported. Use them only with private local data. Never commit those source files.

## 3. Link the tables

Create the links listed in [How the tables fit together](../docs/model-design.md).

Use one-to-many links and let the smaller supporting table filter the detailed table. Add the Client link as well as Date, Billing Period, Worker and Property.

Mark `DimDate[Date]` as the Date table. Sort:

- `DimBillingPeriod[Billing Period]` by `Period Index`;
- `DimDate[Month]` by `Year Month Sort`.

## 4. Create the measure table

Create this calculated table and hide its generated Value column:

```DAX
// Give all report measures one easy-to-find home.
Measures = { BLANK() }
```

Copy the measures from `dax/measures.dax` into that table.

Use these formats:

- money: Australian dollars with two decimal places;
- counts: whole numbers;
- rates and shares: one decimal percentage;
- margin change: one decimal percentage point;
- financial variance: Australian dollars with two decimal places.

Hide raw money columns from the normal report view so visuals use the checked measures.

## 5. Add the time selector

Use Power BI's Field Parameter feature or create the table in `dax/time-grain-parameter.dax`.

Set Billing Period as the default. Use the parameter on the main trend chart so the user can switch to Month.

Add `Month Coverage Status` near the selector. March and August should say Partial month.

Keep Business Overview on Billing Period. Use the separate Monthly Performance page for month-on-month cards and comparable-month measures.

## 6. Build the nine pages

Follow [What each dashboard page should show](../docs/report-specification.md).

Build the pages in this order: Business Overview, Monthly Performance, Billing Period Trend, Worker Performance, Client Analysis, Property Analysis, Jobs and Tasks, Billing and Adjustments, and Billing Checks.

On Monthly Performance, use the month comparison measures and show the `Month Coverage Status`. On Worker Performance, add a reference line using `Average Work Items per Active Worker`. On Client Analysis, include `Revenue Change vs Previous Billing Period %` so each Client shows its own change.

Keep page text short. Use clear titles, a maximum of five cards and only one note when a chart needs context.

## 7. Run the DAX checks

Open DAX Query View and run each `EVALUATE` block in `dax/semantic-tests.dax` separately.

The public sample should return:

- 775 Work Items;
- 41 manual adjustments;
- 350 Property-period rows;
- 102 Properties;
- eight active Workers;
- 96.875 Work Items per active Worker;
- three Clients;
- latest Billing Period revenue of A$3,160.98;
- previous Billing Period revenue of A$3,224.51;
- latest Work Items of 58;
- financial variance within A$0.01.

## 8. Check the report like a user

Before taking screenshots:

1. Refresh every query.
2. Select one Worker and confirm the previous-period comparison stays on that Worker.
3. Select one Client and confirm the Client change is correct.
4. Switch between Billing Period and Month.
5. Confirm March and August are marked partial.
6. Confirm a Worker selection does not wrongly change the Property snapshot.
7. Check negative adjustments in cards and waterfalls.
8. Check titles, labels and warnings at 100% zoom.
9. Add useful alt text to each visual.

## 9. Finish the GitHub release

After the PBIP passes the checks:

1. save the PBIP project;
2. add real Power BI screenshots to `images`;
3. replace the design-preview wording in the main README;
4. record the Desktop version and date checked;
5. run the two Python checks again;
6. review the Git changes before pushing.

Do not publish to Power BI Service or change credentials unless that action has been clearly approved.
