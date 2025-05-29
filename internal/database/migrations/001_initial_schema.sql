-- +goose Up
-- SQL in this section is executed when the migration is applied

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    name TEXT NOT NULL
);

-- Create feeds table
CREATE TABLE feeds (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    name TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Create feed_follows table to track which users follow which feeds
CREATE TABLE feed_follows (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    feed_id UUID NOT NULL REFERENCES feeds(id) ON DELETE CASCADE,
    UNIQUE(user_id, feed_id)
);

-- Create posts table to store RSS feed posts
CREATE TABLE posts (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    description TEXT,
    published_at TIMESTAMP,
    feed_id UUID NOT NULL REFERENCES feeds(id) ON DELETE CASCADE
);

-- +goose Down
-- SQL in this section is executed when the migration is rolled back
DROP TABLE posts;
DROP TABLE feed_follows;
DROP TABLE feeds;
DROP TABLE users;
