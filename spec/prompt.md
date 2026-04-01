You are helping design and build a billing data parser.

Goal: design a billing data parser to examine Openreach's custom pipe-delimited files, identify the product the file relates to, identify the sections within the file, parse the data from each section based on that product's schema and then insert the data into the relevant table(s) in Postgres.

spec/billing_guide.doc details the schema of each product's file.

Components:

Each file will have one or more of the following sections in it. Which section the row relates to is indicated in the first column of each row
    * Header
    * Product Charges
    * Event Charges
    * Adjustments
    * Bill Summary

Each row then consists of up-to 60 columns depending on the record type, however which of these columns are actually used and what their contents consists of depends on the product and this information is listed in the billing guide.

The database schema for this parser has already been determined and is indicated in spec/db_schema.md

Start by creating a design plan for approval. Once I have approved this, you can then go on to build the app.

Design Rules:

* Use Python/Flask for the main application
* It must be able to check a folder for .dat files, then parse each one in turn before moving the completed ones to a different folder
* Database interaction will use Psycopg3, NOT an ORM. Implement database pooling.
* Follow PEP8 where possible and document all functions using Google-style docstrings
* If you require any additional Python libraries installed, let me know

Database:

* All tables are in the openreach schema of the database.
* You can use the postgres-test mcp server for testing.