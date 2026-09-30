from sqlalchemy import text

from extract import extract_posts, extract_comments
from transform import transform_posts, transform_comments
from load import create_database_engine, load_to_postgres


def run_pipeline():
    print("Starting extraction")
    posts_df = extract_posts()
    comments_df = extract_comments()

    print("Starting transformation")
    posts_df = transform_posts(posts_df)
    comments_df = transform_comments(comments_df)

    orphan_comments = ~comments_df["postId"].isin(posts_df["postId"])

    if orphan_comments.any():
        raise ValueError(
            f"{int(orphan_comments.sum())} comments reference "
            "posts absent from the extracted dataset"
        )

    engine = create_database_engine()

    try:
        with engine.begin() as connection:
            connection.execute(
                text("CREATE SCHEMA IF NOT EXISTS api_etl")
            )

            load_to_postgres(posts_df, "posts", connection)
            load_to_postgres(comments_df, "comments", connection)

        print(
            "ETL pipeline completed: "
            f"{len(posts_df)} posts and "
            f"{len(comments_df)} comments committed"
        )
    finally:
        engine.dispose()


if __name__ == "__main__":
    run_pipeline()