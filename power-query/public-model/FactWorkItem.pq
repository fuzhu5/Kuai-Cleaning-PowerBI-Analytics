// Load the anonymised work-item fact and enforce its public data contract.
let
    // Read the portable sample CSV from the configured repository folder.
    Source = Csv.Document(
        File.Contents(pSampleDataFolder & "\work_items.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    // Promote headers and apply business-safe Australian data types.
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"Billing Period Start", type date},
            {"Billing Period End", type date},
            {"Work Item Key", type text},
            {"Work Item Type", type text},
            {"Service Date", type date},
            {"Property Key", type text},
            {"Client", type text},
            {"Work Category", type text},
            {"Worker Key", type text},
            {"Default Worker Key", type text},
            {"Assignment Overridden", type logical},
            {"Approved Client Price", Currency.Type},
            {"Approved Worker Price", Currency.Type},
            {"Cost", Currency.Type},
            {"Business Income", Currency.Type},
            {"Pricing Status", type text},
            {"Price Approved At", type datetimezone},
            {"Worker Price Overridden", type logical},
            {"Ready For Billing", type logical},
            {"No Payment", type logical},
            {"Public Holiday Flag", type logical},
            {"Source File", type text}
        },
        "en-AU"
    ),
    // Add the shared key used by the billing-period dimension.
    AddPeriodKey = Table.AddColumn(
        Typed,
        "Billing Period Key",
        each Date.ToText([Billing Period Start], "yyyyMMdd") & "-" & Date.ToText([Billing Period End], "yyyyMMdd"),
        type text
    ),
    // Recalculate the accounting identity for row-level quality monitoring.
    AddReconciliationVariance = Table.AddColumn(
        AddPeriodKey,
        "Reconciliation Variance",
        each [Approved Client Price] - [Approved Worker Price] - [Cost] - [Business Income],
        Currency.Type
    )
in
    AddReconciliationVariance
