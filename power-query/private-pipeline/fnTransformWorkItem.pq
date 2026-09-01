// Standardise one private Job or Task export into the shared work-item contract.
(Content as binary, SourceFile as text, WorkItemType as text) as table =>
let
    // Declare the schema so a zero-byte or headerless file returns a valid empty table.
    ExpectedColumns = {
        "billing_term_start", "billing_term_end", "job_id", "external_id", "service_date",
        "property_id", "property_address", "client_or_agent", "account", "description",
        "source_status", "completed_by_id", "completed_by", "default_worker",
        "worker_assignment_overridden", "approved_client_price", "approved_worker_price",
        "quoted_client_price", "quoted_worker_price", "client_price_override",
        "worker_price_override", "worker_price_overridden", "cost", "business_income",
        "pricing_status", "price_approved_at", "approved_fees", "extra_payment",
        "ready_for_billing", "no_payment", "public_holiday"
    },

    // Parse UTF-8 CSV content and promote its first row when records exist.
    Parsed = try Csv.Document(Content, [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]) otherwise #table({}, {}),
    Promoted = if Table.RowCount(Parsed) = 0
        then #table(ExpectedColumns, {})
        else Table.PromoteHeaders(Parsed, [PromoteAllScalars = true]),

    // Enforce column presence to make schema drift visible and deterministic.
    ContractColumns = Table.SelectColumns(Promoted, ExpectedColumns, MissingField.UseNull),
    Typed = Table.TransformColumnTypes(
        ContractColumns,
        {
            {"billing_term_start", type date}, {"billing_term_end", type date},
            {"job_id", type text}, {"external_id", type text}, {"service_date", type date},
            {"property_id", type text}, {"property_address", type text}, {"client_or_agent", type text},
            {"account", type text}, {"description", type text}, {"source_status", type text},
            {"completed_by_id", type text}, {"completed_by", type text}, {"default_worker", type text},
            {"worker_assignment_overridden", type logical}, {"approved_client_price", Currency.Type},
            {"approved_worker_price", Currency.Type}, {"quoted_client_price", Currency.Type},
            {"quoted_worker_price", Currency.Type}, {"client_price_override", Currency.Type},
            {"worker_price_override", Currency.Type}, {"worker_price_overridden", type logical},
            {"cost", Currency.Type}, {"business_income", Currency.Type}, {"pricing_status", type text},
            {"price_approved_at", type datetimezone}, {"approved_fees", type text},
            {"extra_payment", type text}, {"ready_for_billing", type logical},
            {"no_payment", type logical}, {"public_holiday", type text}
        },
        "en-AU"
    ),

    // Add lineage and record-type columns before combining folder extracts.
    AddWorkItemType = Table.AddColumn(Typed, "work_item_type", each WorkItemType, type text),
    AddSourceFile = Table.AddColumn(AddWorkItemType, "source_file", each SourceFile, type text)
in
    AddSourceFile
