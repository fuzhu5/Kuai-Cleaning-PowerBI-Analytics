// Combine every private Job and Task period export through one reusable function.
let
    // Discover CSV files and retain only the two supported naming patterns.
    Files = Folder.Files(pPrivateSourceFolder),
    WorkItemFiles = Table.SelectRows(
        Files,
        each [Extension] = ".csv" and
            (Text.StartsWith([Name], "kuai_jobs_") or Text.StartsWith([Name], "kuai_tasks_"))
    ),

    // Invoke the typed transformation and infer record type from the controlled filename.
    AddTransformed = Table.AddColumn(
        WorkItemFiles,
        "Data",
        each fnTransformWorkItem(
            [Content],
            [Name],
            if Text.StartsWith([Name], "kuai_jobs_") then "Job" else "Task"
        ),
        type table
    ),

    // Append all periods and add model-friendly conformed keys.
    Combined = Table.Combine(AddTransformed[Data]),
    RenameColumns = Table.RenameColumns(
        Combined,
        {
            {"job_id", "Work Item Key"}, {"work_item_type", "Work Item Type"},
            {"service_date", "Service Date"}, {"property_id", "Property Key"},
            {"completed_by_id", "Worker Key"}, {"approved_client_price", "Approved Client Price"},
            {"approved_worker_price", "Approved Worker Price"}, {"cost", "Cost"},
            {"business_income", "Business Income"}, {"pricing_status", "Pricing Status"},
            {"source_file", "Source File"}
        },
        MissingField.Ignore
    )
in
    RenameColumns
