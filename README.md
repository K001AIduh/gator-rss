# Gator RSS Feed Aggregator

Gator is a command-line RSS feed aggregator written in Go that helps you keep track of your favorite websites' updates in one place.

## Features

- User management system
- Add and manage RSS feeds
- Follow/unfollow feeds
- Automatically fetch and store posts from feeds
- Browse posts from feeds you follow
- Simple command-line interface

## Requirements

- Go 1.16 or later
- PostgreSQL 13 or later

## Installation

### Installing from Source

1. Clone this repository or download the source code
2. Install the CLI with:

```bash
go install
```

Alternatively, you can build it locally:

```bash
go build -o gator
```

### Database Setup

Gator requires PostgreSQL for storing feeds, posts, and user data.

1. Create a new PostgreSQL database:

```bash
createdb gator
```

2. The application will automatically run migrations when started.

## Configuration

Gator uses a configuration file stored at `~/.gatorconfig.json`. The file will be created automatically when you first use the application, but you can also create it manually:

```json
{
  "database_url": "postgres://postgres:postgres@localhost:5432/gator?sslmode=disable",
  "current_user": ""
}
```

Replace the database URL with your actual PostgreSQL connection string.

## Usage

### User Management

Register a new user:

```
gator register <username>
```

Log in as a user:

```
gator login <username>
```

List all users:

```
gator users
```

### Managing Feeds

Add a new feed:

```
gator addfeed "<feed_name>" "<feed_url>"
```

Example:

```
gator addfeed "TechCrunch" "https://techcrunch.com/feed/"
```

List all feeds in the database:

```
gator feeds
```

### Following Feeds

Follow a feed by URL:

```
gator follow "<feed_url>"
```

Unfollow a feed:

```
gator unfollow "<feed_url>"
```

List feeds you're following:

```
gator following
```

### Working with Posts

Start the feed aggregator to fetch posts (with a specified interval between requests):

```
gator agg <interval>
```

Example (fetch every 10 minutes):

```
gator agg 10m
```

Browse posts from feeds you follow:

```
gator browse [limit]
```

Example (show 10 posts):

```
gator browse 10
```

## Example Workflow

```bash
# Register a new user
gator register johndoe

# Add some feeds
gator addfeed "TechCrunch" "https://techcrunch.com/feed/"
gator addfeed "Hacker News" "https://news.ycombinator.com/rss"
gator addfeed "Boot.dev Blog" "https://blog.boot.dev/index.xml"

# List the feeds you're following
gator following

# Start the aggregator to fetch posts (runs continuously)
gator agg 30m

# In another terminal, browse your posts
gator browse 20
```

## Interval Format

The `agg` command accepts interval strings in Go's duration format:

- `10s` - 10 seconds
- `5m` - 5 minutes
- `1h` - 1 hour
- `1h30m` - 1 hour and 30 minutes

## Contributing

Contributions are welcome! Feel free to submit a pull request.
