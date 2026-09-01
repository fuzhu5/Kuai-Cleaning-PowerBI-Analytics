// Create an anonymous worker dimension shared by both financial facts.
let
    // Collect worker keys from work items and manual adjustments.
    WorkItemWorkers = Table.SelectColumns(FactWorkItem, {"Worker Key"}),
    DefaultWorkers = Table.RenameColumns(
        Table.SelectColumns(FactWorkItem, {"Default Worker Key"}),
        {{"Default Worker Key", "Worker Key"}}
    ),
    ManualEntryWorkers = Table.SelectColumns(FactManualEntry, {"Worker Key"}),
    // Remove blank and duplicate worker keys.
    Combined = Table.Combine({WorkItemWorkers, DefaultWorkers, ManualEntryWorkers}),
    RemoveBlank = Table.SelectRows(Combined, each [Worker Key] <> null and [Worker Key] <> ""),
    DistinctRows = Table.Distinct(RemoveBlank, {"Worker Key"}),
    Sorted = Table.Sort(DistinctRows, {{"Worker Key", Order.Ascending}}),
    // Assign display labels that reveal no source names.
    AddWorkerLabel = Table.AddIndexColumn(Sorted, "Worker Number", 1, 1, Int64.Type),
    AddDisplayName = Table.AddColumn(AddWorkerLabel, "Worker", each "Worker " & Text.PadStart(Text.From([Worker Number]), 2, "0"), type text),
    Result = Table.RemoveColumns(AddDisplayName, {"Worker Number"})
in
    Result
