// Summarise release-critical and operational data-quality checks.
let
    // Materialise the exception sets used by the scorecard.
    FinancialFailures = Table.SelectRows(FactWorkItem, each Number.Abs([Reconciliation Variance]) > 0.01),
    NegativeTransactions = Table.SelectRows(
        FactWorkItem,
        each [Approved Client Price] < 0 or [Approved Worker Price] < 0 or [Cost] < 0 or [Business Income] < 0
    ),
    MissingProperty = Table.SelectRows(FactWorkItem, each [Property Key] = null or [Property Key] = ""),
    MissingClient = Table.SelectRows(FactWorkItem, each [Client] = null or [Client] = ""),
    // Return one compact row per test for the Data Quality report page.
    Summary = #table(
        type table [Check = text, Result = text, Record Count = Int64.Type, Severity = text],
        {
            {"Financial reconciliation", if Table.RowCount(FinancialFailures) = 0 then "Pass" else "Fail", Table.RowCount(FinancialFailures), "Critical"},
            {"Negative work-item amounts", "Review", Table.RowCount(NegativeTransactions), "Warning"},
            {"Missing property key", if Table.RowCount(MissingProperty) = 0 then "Pass" else "Fail", Table.RowCount(MissingProperty), "Critical"},
            {"Missing Client", if Table.RowCount(MissingClient) = 0 then "Pass" else "Fail", Table.RowCount(MissingClient), "Critical"},
            {"Assignment overrides", "Monitor", Table.RowCount(Table.SelectRows(FactWorkItem, each [Assignment Overridden] = true)), "Information"},
            {"Worker price overrides", "Monitor", Table.RowCount(Table.SelectRows(FactWorkItem, each [Worker Price Overridden] = true)), "Information"}
        }
    )
in
    Summary
