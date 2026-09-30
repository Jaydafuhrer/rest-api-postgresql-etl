-- Connect to the database used by the pipeline.

-- Row counts
SELECT 'posts' AS dataset, COUNT(*) AS total_rows
FROM api_etl.posts
UNION ALL
SELECT 'comments', COUNT(*)
FROM api_etl.comments;

-- Duplicate post IDs: expect zero rows
SELECT "postId", COUNT(*)
FROM api_etl.posts
GROUP BY "postId"
HAVING COUNT(*) > 1;

-- Duplicate comment IDs: expect zero rows
SELECT "commentId", COUNT(*)
FROM api_etl.comments
GROUP BY "commentId"
HAVING COUNT(*) > 1;

-- Comments without a matching post: expect zero rows
SELECT c."commentId", c."postId"
FROM api_etl.comments AS c
LEFT JOIN api_etl.posts AS p
    ON p."postId" = c."postId"
WHERE p."postId" IS NULL;