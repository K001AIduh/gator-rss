package main

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"gator/internal/config"
	"gator/internal/database"
	"gator/internal/rss"

	"github.com/google/uuid"
	_ "github.com/lib/pq"
)

// state holds the application state
type state struct {
	db  *database.Queries
	cfg *config.Config
}

// command represents a CLI command
type command struct {
	name string
	args []string
}

// commands holds all registered command handlers
type commands struct {
	handlers map[string]func(*state, command) error
}

// register adds a new command handler
func (c *commands) register(name string, f func(*state, command) error) {
	c.handlers[name] = f
}

// run executes a command if it exists
func (c *commands) run(s *state, cmd command) error {
	handler, exists := c.handlers[cmd.name]
	if !exists {
		return fmt.Errorf("unknown command: %s", cmd.name)
	}
	return handler(s, cmd)
}

// middlewareLoggedIn is a middleware that ensures a user is logged in
func middlewareLoggedIn(handler func(s *state, cmd command, user database.User) error) func(*state, command) error {
	return func(s *state, cmd command) error {
		// Get the current user from the config
		currentUser := s.cfg.CurrentUserName
		if currentUser == "" {
			return errors.New("you must be logged in to use this command")
		}

		// Get the user from the database
		user, err := s.db.GetUser(context.Background(), currentUser)
		if err != nil {
			return fmt.Errorf("failed to get current user: %w", err)
		}

		// Call the handler with the user
		return handler(s, cmd, user)
	}
}

// handlerLogin handles the login command
func handlerLogin(s *state, cmd command) error {
	if len(cmd.args) < 1 {
		return errors.New("username is required")
	}

	username := cmd.args[0]

	// Check if the user exists in the database
	_, err := s.db.GetUser(context.Background(), username)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return fmt.Errorf("user %s does not exist", username)
		}
		return fmt.Errorf("failed to get user: %w", err)
	}

	err = s.cfg.SetUser(username)
	if err != nil {
		return fmt.Errorf("failed to set user: %w", err)
	}

	fmt.Printf("Logged in as %s\n", username)
	return nil
}

// handlerRegister handles the register command
func handlerRegister(s *state, cmd command) error {
	if len(cmd.args) < 1 {
		return errors.New("username is required")
	}

	username := cmd.args[0]

	// Check if the user already exists
	_, err := s.db.GetUser(context.Background(), username)
	if err == nil {
		return fmt.Errorf("user %s already exists", username)
	} else if !errors.Is(err, sql.ErrNoRows) {
		return fmt.Errorf("failed to check if user exists: %w", err)
	}

	// Create the user
	now := time.Now().UTC()
	user, err := s.db.CreateUser(context.Background(), database.CreateUserParams{
		ID:        uuid.New(),
		CreatedAt: now,
		UpdatedAt: now,
		Name:      username,
	})
	if err != nil {
		return fmt.Errorf("failed to create user: %w", err)
	}

	// Set the user in the config
	err = s.cfg.SetUser(username)
	if err != nil {
		return fmt.Errorf("failed to set user: %w", err)
	}

	fmt.Printf("User %s created successfully\n", username)
	fmt.Printf("User details: %+v\n", user)
	return nil
}

// handlerReset handles the reset command
func handlerReset(s *state, cmd command) error {
	// Delete all users from the database
	err := s.db.DeleteAllUsers(context.Background())
	if err != nil {
		return fmt.Errorf("failed to reset database: %w", err)
	}

	fmt.Println("Database reset successfully")
	return nil
}

// handlerUsers handles the users command
func handlerUsers(s *state, cmd command) error {
	// Get all users from the database
	users, err := s.db.GetUsers(context.Background())
	if err != nil {
		return fmt.Errorf("failed to get users: %w", err)
	}

	if len(users) == 0 {
		fmt.Println("No users found")
		return nil
	}

	// Get the current user from the config
	currentUser := s.cfg.CurrentUserName

	// Print each user, indicating the current one
	for _, user := range users {
		if user.Name == currentUser {
			fmt.Printf("* %s (current)\n", user.Name)
		} else {
			fmt.Printf("* %s\n", user.Name)
		}
	}

	return nil
}

// handlerAgg handles the agg command
func handlerAgg(s *state, cmd command) error {
	if len(cmd.args) < 1 {
		return errors.New("time between requests is required (e.g. 10s, 1m)")
	}

	timeBetweenRequestsStr := cmd.args[0]
	timeBetweenRequests, err := time.ParseDuration(timeBetweenRequestsStr)
	if err != nil {
		return fmt.Errorf("invalid duration format: %w", err)
	}

	fmt.Printf("Collecting feeds every %v\n", timeBetweenRequests)

	// Create a ticker that ticks at the specified interval
	ticker := time.NewTicker(timeBetweenRequests)
	defer ticker.Stop()

	// Run immediately and then on each tick
	for ; ; <-ticker.C {
		if err := scrapeFeeds(s); err != nil {
			fmt.Printf("Error scraping feeds: %v\n", err)
		}
	}
}

// scrapeFeeds fetches the next feed and saves its posts
func scrapeFeeds(s *state) error {
	// Get the next feed to fetch
	feed, err := s.db.GetNextFeedToFetch(context.Background())
	if err != nil {
		return fmt.Errorf("failed to get next feed to fetch: %w", err)
	}

	// Mark the feed as fetched
	err = s.db.MarkFeedFetched(context.Background(), feed.ID)
	if err != nil {
		return fmt.Errorf("failed to mark feed as fetched: %w", err)
	}

	// Fetch the feed
	fmt.Printf("Fetching feed: %s (%s)\n", feed.Name, feed.Url)
	rssFeed, err := rss.FetchFeedWithContext(context.Background(), feed.Url)
	if err != nil {
		return fmt.Errorf("failed to fetch feed: %w", err)
	}

	// Print feed info
	fmt.Printf("Feed: %s\n", rssFeed.Channel.Title)
	fmt.Printf("Found %d items\n", len(rssFeed.Channel.Items))

	// Save each post to the database
	savedCount := 0
	for _, item := range rssFeed.Channel.Items {
		// Parse the publication date
		var publishedAt sql.NullTime
		pubDate, err := rss.ParseDate(item.PubDate)
		if err == nil {
			publishedAt = sql.NullTime{
				Time:  pubDate,
				Valid: true,
			}
		}

		// Create description as sql.NullString
		var description sql.NullString
		if item.Description != "" {
			description = sql.NullString{
				String: item.Description,
				Valid:  true,
			}
		}

		// Create the post
		now := time.Now().UTC()
		_, err = s.db.CreatePost(context.Background(), database.CreatePostParams{
			ID:          uuid.New(),
			CreatedAt:   now,
			UpdatedAt:   now,
			Title:       item.Title,
			Url:         item.Link,
			Description: description,
			PublishedAt: publishedAt,
			FeedID:      feed.ID,
		})

		if err != nil {
			// If it's a unique constraint violation, just ignore it
			if strings.Contains(err.Error(), "duplicate key value violates unique constraint") {
				continue
			}
			fmt.Printf("Error saving post: %v\n", err)
		} else {
			savedCount++
		}
	}

	fmt.Printf("Saved %d new posts\n", savedCount)
	fmt.Printf("Next fetch in %v\n\n", time.Now().Add(time.Second))
	return nil
}

// handlerAddFeed handles the addfeed command
func handlerAddFeed(s *state, cmd command, user database.User) error {
	// Check if we have the required arguments
	if len(cmd.args) < 2 {
		if len(cmd.args) == 0 {
			return errors.New("feed name and URL are required")
		}
		return errors.New("feed URL is required")
	}

	feedName := cmd.args[0]
	feedURL := cmd.args[1]

	// Create the feed
	now := time.Now().UTC()

	var feed database.Feed
	// Check if the feed already exists
	existingFeed, err := s.db.GetFeedByURL(context.Background(), feedURL)
	if err == nil {
		// Feed already exists
		feed = existingFeed
	} else if errors.Is(err, sql.ErrNoRows) {
		// Feed doesn't exist, create it
		feed, err = s.db.CreateFeed(context.Background(), database.CreateFeedParams{
			ID:        uuid.New(),
			CreatedAt: now,
			UpdatedAt: now,
			Name:      feedName,
			Url:       feedURL,
			UserID:    user.ID,
		})
		if err != nil {
			return fmt.Errorf("failed to create feed: %w", err)
		}
	} else {
		return fmt.Errorf("failed to check if feed exists: %w", err)
	}

	// Automatically follow the feed
	feedFollow, err := s.db.CreateFeedFollow(context.Background(), database.CreateFeedFollowParams{
		ID:        uuid.New(),
		CreatedAt: now,
		UpdatedAt: now,
		UserID:    user.ID,
		FeedID:    feed.ID,
	})
	if err != nil {
		return fmt.Errorf("failed to follow feed: %w", err)
	}

	fmt.Printf("Feed added successfully\n")
	fmt.Printf("Feed details: %+v\n", feed)
	fmt.Printf("Following feed: %s\n", feedFollow.FeedName)
	return nil
}

// handlerFeeds handles the feeds command
func handlerFeeds(s *state, cmd command) error {
	// Get all feeds with associated users from the database
	feeds, err := s.db.GetFeedsWithUsers(context.Background())
	if err != nil {
		return fmt.Errorf("failed to get feeds: %w", err)
	}

	if len(feeds) == 0 {
		fmt.Println("No feeds found")
		return nil
	}

	// Print each feed with its details
	for _, feed := range feeds {
		fmt.Printf("Feed: %s\n", feed.Name)
		fmt.Printf("URL: %s\n", feed.Url)
		fmt.Printf("Added by: %s\n", feed.UserName)
		fmt.Println("---")
	}

	return nil
}

// handlerFollow handles the follow command
func handlerFollow(s *state, cmd command, user database.User) error {
	// Check if we have the required argument
	if len(cmd.args) < 1 {
		return errors.New("feed URL is required")
	}

	feedURL := cmd.args[0]

	// Get the feed from the database
	feed, err := s.db.GetFeedByURL(context.Background(), feedURL)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return fmt.Errorf("feed with URL %s does not exist", feedURL)
		}
		return fmt.Errorf("failed to get feed: %w", err)
	}

	// Create the feed follow
	now := time.Now().UTC()
	feedFollow, err := s.db.CreateFeedFollow(context.Background(), database.CreateFeedFollowParams{
		ID:        uuid.New(),
		CreatedAt: now,
		UpdatedAt: now,
		UserID:    user.ID,
		FeedID:    feed.ID,
	})
	if err != nil {
		return fmt.Errorf("failed to follow feed: %w", err)
	}

	fmt.Printf("You are now following: %s\n", feedFollow.FeedName)
	return nil
}

// handlerFollowing handles the following command
func handlerFollowing(s *state, cmd command, user database.User) error {
	// Get all feed follows for the user
	feedFollows, err := s.db.GetFeedFollowsForUser(context.Background(), user.ID)
	if err != nil {
		return fmt.Errorf("failed to get feed follows: %w", err)
	}

	if len(feedFollows) == 0 {
		fmt.Println("You are not following any feeds")
		return nil
	}

	// Print each followed feed
	fmt.Println("You are following:")
	for _, ff := range feedFollows {
		fmt.Printf("* %s\n", ff.FeedName)
	}

	return nil
}

// handlerUnfollow handles the unfollow command
func handlerUnfollow(s *state, cmd command, user database.User) error {
	// Check if we have the required argument
	if len(cmd.args) < 1 {
		return errors.New("feed URL is required")
	}

	feedURL := cmd.args[0]

	// Delete the feed follow
	err := s.db.DeleteFeedFollow(context.Background(), database.DeleteFeedFollowParams{
		UserID: user.ID,
		Url:    feedURL,
	})
	if err != nil {
		return fmt.Errorf("failed to unfollow feed: %w", err)
	}

	fmt.Printf("You have unfollowed the feed: %s\n", feedURL)
	return nil
}

// handlerBrowse handles the browse command
func handlerBrowse(s *state, cmd command, user database.User) error {
	// Set default limit if not provided
	limit := 2
	if len(cmd.args) > 0 {
		var err error
		limit, err = strconv.Atoi(cmd.args[0])
		if err != nil {
			return fmt.Errorf("invalid limit: %w", err)
		}
	}

	// Get posts for the user
	posts, err := s.db.GetPostsForUser(context.Background(), database.GetPostsForUserParams{
		UserID: user.ID,
		Limit:  int32(limit),
	})
	if err != nil {
		return fmt.Errorf("failed to get posts: %w", err)
	}

	if len(posts) == 0 {
		fmt.Println("No posts found")
		return nil
	}

	// Print each post
	fmt.Printf("Found %d posts:\n\n", len(posts))
	for i, post := range posts {
		fmt.Printf("Post #%d: %s\n", i+1, post.Title)
		fmt.Printf("Feed: %s\n", post.FeedName)
		fmt.Printf("URL: %s\n", post.Url)

		if post.Description.Valid {
			desc := post.Description.String
			// Truncate long descriptions
			if len(desc) > 100 {
				desc = desc[:100] + "..."
			}
			fmt.Printf("Description: %s\n", desc)
		}

		if post.PublishedAt.Valid {
			fmt.Printf("Published: %v\n", post.PublishedAt.Time.Format(time.RFC1123))
		}
		fmt.Println("---")
	}

	return nil
}

func main() {
	// Read the configuration file
	cfg, err := config.Read()
	if err != nil {
		log.Fatalf("Failed to read config: %v", err)
	}

	// Open a connection to the database
	db, err := sql.Open("postgres", cfg.DBURL)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	// Create a new database queries instance
	dbQueries := database.New(db)

	// Create application state
	s := &state{
		db:  dbQueries,
		cfg: &cfg,
	}

	// Create commands registry
	cmds := commands{
		handlers: make(map[string]func(*state, command) error),
	}

	// Register commands
	cmds.register("login", handlerLogin)
	cmds.register("register", handlerRegister)
	cmds.register("reset", handlerReset)
	cmds.register("users", handlerUsers)
	cmds.register("agg", handlerAgg)
	cmds.register("addfeed", middlewareLoggedIn(handlerAddFeed))
	cmds.register("feeds", handlerFeeds)
	cmds.register("follow", middlewareLoggedIn(handlerFollow))
	cmds.register("following", middlewareLoggedIn(handlerFollowing))
	cmds.register("unfollow", middlewareLoggedIn(handlerUnfollow))
	cmds.register("browse", middlewareLoggedIn(handlerBrowse))

	// Get command line arguments
	args := os.Args

	// We need at least one argument (the command)
	if len(args) < 2 {
		fmt.Println("Error: command is required")
		os.Exit(1)
	}

	// Parse command and arguments
	cmd := command{
		name: args[1],
		args: args[2:],
	}

	// Run the command
	err = cmds.run(s, cmd)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}
