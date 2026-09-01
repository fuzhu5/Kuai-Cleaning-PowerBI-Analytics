// Derive one privacy-safe dimension row per property.
let
    // Keep stable attributes only; period-varying quotes stay in the snapshot fact.
    Source = FactPropertyPeriodSnapshot,
    KeepColumns = Table.SelectColumns(Source, {"Property Key", "Property Label"}),
    DistinctRows = Table.Distinct(KeepColumns, {"Property Key"})
in
    DistinctRows
