# REST API to PostgreSQL ETL Pipeline

A modular Python pipeline that extracts posts and comments from
JSONPlaceholder, transforms the responses with pandas, and loads
them into PostgreSQL.

## Verified execution

A successful local run extracted, transformed, and committed:

- 100 posts
- 500 comments

## Pipeline stages

### Extract
- Fetch posts and comments using Requests.
- Apply connection and read timeouts.
- Reject HTTP errors and unexpected response structures.
- Convert JSON responses into pandas DataFrames.

### Transform
- Select and rename columns.
- Validate required columns.
- Convert identifiers to positive integers.
- Reject duplicate post and comment identifiers.
- Check that every comment references an extracted post.

### Load
- Read database credentials from environment variables.
- Use explicit PostgreSQL column types.
- Refresh both tables within one transaction.
- Dispose of the database engine after execution.

## Project files

| File | Purpose |
|---|---|
| `main.py` | Coordinates the pipeline |
| `extract.py` | API requests and JSON extraction |
| `transform.py` | DataFrame transformations and validation |
| `load.py` | Database configuration and loading |
| `requirements.txt` | Project dependencies |
| `sql/validation.sql` | Database verification queries |

## Setup

Requires Python 3.9 or later and a running PostgreSQL database.
Dependencies must support the chosen Python version.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a PostgreSQL database or use an existing one.
The default database name is `data_warehouse`.

Set connection variables in your PyCharm run configuration:

| Variable | Default |
|---|---|
| `DB_HOST` | `localhost` |
| `DB_PORT` | `5432` |
| `DB_USER` | `postgres` |
| `DB_NAME` | `data_warehouse` |
| `DB_PASSWORD` | Required |

The script reads environment variables directly.
It does not automatically load a `.env` file.

Run:

```bash
python main.py
```

The pipeline creates the `api_etl` schema and its destination tables.
The database user needs permission to create the schema and tables.

## Destination tables

- `api_etl.posts`: userId, postId, postTitle, postBody
- `api_etl.comments`: postId, commentId, userEmail, commentBody

Column names use mixed case and require double quotes in SQL.

## Loading behavior

This is a full-refresh pipeline. Each successful run drops and
recreates its destination tables using pandas `to_sql`.

Both tables are loaded in one PostgreSQL transaction. If a load
fails, the transaction rolls back.

Do not attach dependent views or custom constraints to these
tables without changing the refresh strategy.

## Limitations

- JSONPlaceholder provides synthetic demonstration data.
- Execution is manual.
- Requests have timeouts but no retry policy.
- Identifier and relationship checks run in Python; database
  primary and foreign keys are not created.
- Text fields are not checked for email format or content quality.
- Automated tests and CI have not yet been added.

## Data source

[JSONPlaceholder](https://jsonplaceholder.typicode.com/)

## Author

Aderinwale John O.