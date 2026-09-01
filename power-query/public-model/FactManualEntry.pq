// Load privacy-safe manual adjustments as a separate financial fact.
let
    // Read the published adjustment sample.
    Source = Csv.Document(
        File.Contents(pSampleDataFolder & "\manual_entries.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    // Promote headers and enforce dates, timestamps and currency types.
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"Billing Period Start", type date},
            {"Billing Period End", type date},
            {"Manual Entry Key", type text},
            {"Service Date", type date},
            {"Adjustment Category", type text},
            {"Allocation", type text},
            {"Worker Key", type text},
            {"Approved Client Price", Currency.Type},
            {"Approved Worker Price", Currency.Type},
            {"Cost", Currency.Type},
            {"Business Income", Currency.Type},
            {"Status", type text},
            {"Approved Or Updated At", type datetimezone},
            {"Source File", type text}
        },
        "en-AU"
    ),
    // Create the conformed billing-period key.
    AddPeriodKey = Table.AddColumn(
        Typed,
        "Billing Period Key",
        each Date.ToText([Billing Period Start], "yyyyMMdd") & "-" & Date.ToText([Billing Period End], "yyyyMMdd"),
        type text
    ),
    // Validate the same accounting identity used by the work-item fact.
    AddReconciliationVariance = Table.AddColumn(
        AddPeriodKey,
        "Reconciliation Variance",
        each [Approved Client Price] - [Approved Worker Price] - [Cost] - [Business Income],
        Currency.Type
    )
in
    AddReconciliationVariance
