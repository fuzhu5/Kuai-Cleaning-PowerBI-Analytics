// Combine private Manual Entry exports while tolerating headerless empty periods.
let
    // Declare the manual-entry data contract used by every period file.
    ExpectedColumns = {
        "billing_term_start", "billing_term_end", "manual_entry_id", "service_date",
        "description", "allocation", "completed_by_id", "completed_by",
        "approved_client_price", "approved_worker_price", "cost", "business_income",
        "status", "approved_or_updated_at"
    },

    // Define a local transformation that returns the declared empty schema when needed.
    TransformFile = (Content as binary, SourceFile as text) as table =>
        let
            Parsed = try Csv.Document(Content, [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]) otherwise #table({}, {}),
            Promoted = if Table.RowCount(Parsed) = 0 then #table(ExpectedColumns, {}) else Table.PromoteHeaders(Parsed, [PromoteAllScalars = true]),
            ContractColumns = Table.SelectColumns(Promoted, ExpectedColumns, MissingField.UseNull),
            Typed = Table.TransformColumnTypes(
                ContractColumns,
                {
                    {"billing_term_start", type date}, {"billing_term_end", type date},
                    {"manual_entry_id", type text}, {"service_date", type date},
                    {"description", type text}, {"allocation", type text},
                    {"completed_by_id", type text}, {"completed_by", type text},
                    {"approved_client_price", Currency.Type}, {"approved_worker_price", Currency.Type},
                    {"cost", Currency.Type}, {"business_income", Currency.Type},
                    {"status", type text}, {"approved_or_updated_at", type datetimezone}
                },
                "en-AU"
            ),
            AddSourceFile = Table.AddColumn(Typed, "source_file", each SourceFile, type text)
        in
            AddSourceFile,

    // Discover the supported extracts and invoke the local transformation.
    Files = Folder.Files(pPrivateSourceFolder),
    ManualFiles = Table.SelectRows(Files, each [Extension] = ".csv" and Text.StartsWith([Name], "kuai_manual_entries_")),
    AddTransformed = Table.AddColumn(ManualFiles, "Data", each TransformFile([Content], [Name]), type table),

    // Append all non-empty period records into one auditable fact.
    Combined = Table.Combine(AddTransformed[Data])
in
    Combined
