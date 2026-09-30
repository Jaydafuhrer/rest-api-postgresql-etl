import os

from sqlalchemy import URL, BigInteger, Text, create_engine

SCHEMA = "api_etl"

TABLE_TYPES = {
    "posts": {
        "userId": BigInteger(),
        "postId": BigInteger(),
        "postTitle": Text(),
        "postBody": Text(),
    },
    "comments": {
        "postId": BigInteger(),
        "commentId": BigInteger(),
        "userEmail": Text(),
        "commentBody": Text(),
    },
}


def create_database_engine():
    password = os.environ.get("DB_PASSWORD")

    if not password:
        raise ValueError(
            "Set DB_PASSWORD in your PyCharm run configuration"
        )

    url = URL.create(
        drivername="postgresql+psycopg",
        username=os.environ.get("DB_USER", "postgres"),
        password=password,
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ.get("DB_NAME", "data_warehouse"),
    )

    return create_engine(
        url,
        pool_pre_ping=True,
        hide_parameters=True,
        connect_args={"connect_timeout": 10},
    )


def load_to_postgres(df, table_name, connection):
    if table_name not in TABLE_TYPES:
        raise ValueError(f"Unsupported table: {table_name}")

    if df.empty:
        raise ValueError(f"Cannot load an empty {table_name} dataset")

    df.to_sql(
        name=table_name,
        con=connection,
        schema=SCHEMA,
        if_exists="replace",
        index=False,
        dtype=TABLE_TYPES[table_name],
        chunksize=500,
    )

    print(f"Prepared {len(df)} rows for {SCHEMA}.{table_name}")