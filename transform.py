import pandas as pd


def validate_ids(df, columns, unique_column):
    for column in columns:
        values = pd.to_numeric(df[column], errors="raise")

        if values.isna().any():
            raise ValueError(f"Missing identifier in {column}")

        if ((values <= 0) | (values % 1 != 0)).any():
            raise ValueError(
                f"{column} must contain positive whole numbers"
            )

        df[column] = values.astype("int64")

    if df[unique_column].duplicated().any():
        raise ValueError(f"Duplicate {unique_column} values")


def transform_posts(posts_df):
    required = ["userId", "id", "title", "body"]

    missing = set(required) - set(posts_df.columns)
    if missing:
        raise ValueError(f"Missing post columns: {sorted(missing)}")

    df = posts_df[required].copy().rename(columns={
        "id": "postId",
        "title": "postTitle",
        "body": "postBody",
    })

    validate_ids(df, ["userId", "postId"], "postId")
    return df


def transform_comments(comments_df):
    required = ["postId", "id", "email", "body"]

    missing = set(required) - set(comments_df.columns)
    if missing:
        raise ValueError(f"Missing comment columns: {sorted(missing)}")

    df = comments_df[required].copy().rename(columns={
        "id": "commentId",
        "email": "userEmail",
        "body": "commentBody",
    })

    validate_ids(df, ["postId", "commentId"], "commentId")
    return df