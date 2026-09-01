# What was checked

Good-looking charts are not useful if the billing numbers cannot be trusted. This project checks the data before it reaches the report.

## What was found in the private extracts

The supplied files contain:

- 631 Jobs;
- 144 Tasks;
- 41 manual adjustments;
- 350 Property-by-period rows;
- ten closed Billing Periods.

The private review found:

- Job and Task IDs are unique;
- every financial row follows the expected money rule;
- four Manual Entry files are completely empty and have no useful header;
- 28 rows contain a negative financial amount;
- 64 Work Items have a worker assignment override;
- two Work Items have a worker-price override;
- descriptions contain names, phone numbers, addresses or operational instructions and should never be published.

## What the Python checks do

Before the public sample is shared, the scripts check:

1. the expected files exist;
2. the columns needed by Power BI are present;
3. the files contain rows;
4. Work Item IDs are unique;
5. the financial rule balances within A$0.01;
6. common phone, email, URL, address and known-name patterns are absent;
7. every code file contains a block comment;
8. README links point to real files;
9. there are no duplicate DAX measure names;
10. no Ruby scripts remain in the Python version of the project.

## What Power BI should display

The Billing Checks page should show:

- Financial balance: Pass;
- Work Items: 775;
- Manual adjustments: 41;
- Property-period rows: 350;
- anonymous Properties: 102;
- active Workers: 8;
- Clients: 3;
- records with negative financial amounts: 28.

## What still needs checking in Desktop

The Python tests cannot confirm how Power BI behaves. After the PBIP is built, check that:

- all queries refresh;
- the table links work as expected;
- the DAX tests return the expected numbers;
- previous Billing Period measures keep the selected Client or Worker;
- Month labels sort correctly;
- partial months are visible;
- no chart clips labels or hides important warnings.

The current evidence is a checked local snapshot. It is not a live connection to the operating system.
