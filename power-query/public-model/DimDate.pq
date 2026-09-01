// Generate a continuous service-date dimension for time intelligence.
let
    // Create one row per day across the observed service-date range.
    ServiceDates = List.RemoveNulls(List.Combine({FactWorkItem[Service Date], FactManualEntry[Service Date]})),
    StartDate = List.Min(ServiceDates),
    EndDate = List.Max(ServiceDates),
    Dates = List.Dates(StartDate, Duration.Days(EndDate - StartDate) + 1, #duration(1, 0, 0, 0)),
    ToTable = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}),
    Typed = Table.TransformColumnTypes(ToTable, {{"Date", type date}}),
    // Add Australian calendar labels and operational weekday attributes.
    AddYear = Table.AddColumn(Typed, "Year", each Date.Year([Date]), Int64.Type),
    AddMonthNumber = Table.AddColumn(AddYear, "Month Number", each Date.Month([Date]), Int64.Type),
    AddMonth = Table.AddColumn(AddMonthNumber, "Month", each Date.ToText([Date], "MMM yyyy", "en-AU"), type text),
    AddMonthStart = Table.AddColumn(AddMonth, "Month Start", each Date.StartOfMonth([Date]), type date),
    AddMonthEnd = Table.AddColumn(AddMonthStart, "Month End", each Date.EndOfMonth([Date]), type date),
    AddYearMonthSort = Table.AddColumn(AddMonthEnd, "Year Month Sort", each Date.Year([Date]) * 100 + Date.Month([Date]), Int64.Type),
    AddMonthCoverage = Table.AddColumn(
        AddYearMonthSort,
        "Month Coverage",
        each if [Month Start] < Date.StartOfMonth(StartDate) or [Month End] > Date.EndOfMonth(EndDate)
            then "Partial month"
            else "Full month",
        type text
    ),
    AddWeekStart = Table.AddColumn(AddMonthCoverage, "Week Start", each Date.StartOfWeek([Date], Day.Monday), type date),
    AddDayName = Table.AddColumn(AddWeekStart, "Day", each Date.DayOfWeekName([Date], "en-AU"), type text),
    AddIsWeekend = Table.AddColumn(AddDayName, "Is Weekend", each Date.DayOfWeek([Date], Day.Monday) >= 5, type logical)
in
    AddIsWeekend
