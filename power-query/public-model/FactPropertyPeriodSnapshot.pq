// Load the periodic property snapshot at one property per billing period.
let
    // Read the anonymised property-period sample.
    Source = Csv.Document(
        File.Contents(pSampleDataFolder & "\property_periods.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    // Apply explicit types for property attributes, activity and quotes.
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"Billing Period Start", type date},
            {"Billing Period End", type date},
            {"Property Key", type text},
            {"Property Label", type text},
            {"Job Count", Int64.Type},
            {"Task Count", Int64.Type},
            {"Bedrooms", Int64.Type},
            {"Bathrooms", Int64.Type},
            {"Quoted Client Price", Currency.Type},
            {"Quoted Worker Price", Currency.Type},
            {"Quote Start", type date},
            {"Quote End", type date},
            {"Source File", type text}
        },
        "en-AU"
    ),
    // Add the conformed key used to analyse quote and activity changes by period.
    AddPeriodKey = Table.AddColumn(
        Typed,
        "Billing Period Key",
        each Date.ToText([Billing Period Start], "yyyyMMdd") & "-" & Date.ToText([Billing Period End], "yyyyMMdd"),
        type text
    )
in
    AddPeriodKey
