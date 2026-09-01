// Combine property snapshots at one property per closed billing period.
let
    // Declare the property-period schema independently of any one source file.
    ExpectedColumns = {
        "billing_term_start", "billing_term_end", "property_id", "property_address",
        "client_or_agent", "job_count", "task_count", "completed_by", "bedrooms",
        "bathrooms", "quoted_client_price", "quoted_worker_price", "quote_start", "quote_end"
    },

    // Parse, type and label each property file before it is appended.
    TransformFile = (Content as binary, SourceFile as text) as table =>
        let
            Parsed = Csv.Document(Content, [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            Promoted = Table.PromoteHeaders(Parsed, [PromoteAllScalars = true]),
            ContractColumns = Table.SelectColumns(Promoted, ExpectedColumns, MissingField.UseNull),
            Typed = Table.TransformColumnTypes(
                ContractColumns,
                {
                    {"billing_term_start", type date}, {"billing_term_end", type date},
                    {"property_id", type text}, {"property_address", type text},
                    {"client_or_agent", type text}, {"job_count", Int64.Type}, {"task_count", Int64.Type},
                    {"completed_by", type text}, {"bedrooms", Int64.Type}, {"bathrooms", Int64.Type},
                    {"quoted_client_price", Currency.Type}, {"quoted_worker_price", Currency.Type},
                    {"quote_start", type date}, {"quote_end", type date}
                },
                "en-AU"
            ),
            AddSourceFile = Table.AddColumn(Typed, "source_file", each SourceFile, type text)
        in
            AddSourceFile,

    // Discover, transform and append all matching period snapshots.
    Files = Folder.Files(pPrivateSourceFolder),
    PropertyFiles = Table.SelectRows(Files, each [Extension] = ".csv" and Text.StartsWith([Name], "kuai_properties_")),
    AddTransformed = Table.AddColumn(PropertyFiles, "Data", each TransformFile([Content], [Name]), type table),
    Combined = Table.Combine(AddTransformed[Data])
in
    Combined
