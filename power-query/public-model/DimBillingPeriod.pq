// Build a conformed dimension for the business's closed 14-day billing periods.
let
    // Union period keys from both transaction facts.
    WorkPeriods = Table.SelectColumns(FactWorkItem, {"Billing Period Key", "Billing Period Start", "Billing Period End"}),
    ManualPeriods = Table.SelectColumns(FactManualEntry, {"Billing Period Key", "Billing Period Start", "Billing Period End"}),
    Combined = Table.Distinct(Table.Combine({WorkPeriods, ManualPeriods}), {"Billing Period Key"}),
    Sorted = Table.Sort(Combined, {{"Billing Period Start", Order.Ascending}}),
    // Add a sortable index and human-readable display label.
    AddPeriodIndex = Table.AddIndexColumn(Sorted, "Period Index", 1, 1, Int64.Type),
    AddPeriodLabel = Table.AddColumn(
        AddPeriodIndex,
        "Billing Period",
        each Date.ToText([Billing Period Start], "dd MMM") & " - " & Date.ToText([Billing Period End], "dd MMM yyyy"),
        type text
    )
in
    AddPeriodLabel
