-- name: CreatePost :one
INSERT INTO posts (id, created_at, updated_at, title, url, description, published_at, feed_id)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
RETURNING *;

-- name: GetPostByID :one
SELECT * FROM posts
WHERE id = $1;

-- name: ListPosts :many
SELECT * FROM posts
ORDER BY published_at DESC
LIMIT $1 OFFSET $2;

-- name: ListPostsByUser :many
SELECT p.*
FROM posts p
JOIN feed_follows ff ON p.feed_id = ff.feed_id
WHERE ff.user_id = $1
ORDER BY p.published_at DESC
LIMIT $2 OFFSET $3;
