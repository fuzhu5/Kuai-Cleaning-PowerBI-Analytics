// Create one row for each of the business's three Clients.
let
    // Keep only the Client label used by report filters and relationships.
    Source = Table.SelectColumns(FactWorkItem, {"Client"}),
    RemoveBlank = Table.SelectRows(Source, each [Client] <> null and [Client] <> ""),
    DistinctRows = Table.Distinct(RemoveBlank, {"Client"}),
    Sorted = Table.Sort(DistinctRows, {{"Client", Order.Ascending}})
in
    Sorted
