package service

import (
	"context"
	"log"
	"time"

	"gator/internal/database"
	"gator/internal/rss"
)

// FeedFetcher is a service that continuously fetches new posts from RSS feeds
type FeedFetcher struct {
	db         database.DBTX
	fetchDelay time.Duration
}

// NewFeedFetcher creates a new FeedFetcher
func NewFeedFetcher(db database.DBTX, fetchDelay time.Duration) *FeedFetcher {
	return &FeedFetcher{
		db:         db,
		fetchDelay: fetchDelay,
	}
}

// Start starts the feed fetcher service
func (f *FeedFetcher) Start(ctx context.Context) error {
	log.Println("Starting feed fetcher service")

	ticker := time.NewTicker(f.fetchDelay)
	defer ticker.Stop()

	// Do an initial fetch
	if err := f.fetchAllFeeds(ctx); err != nil {
		log.Printf("Error during initial fetch: %v", err)
	}

	// Then start the ticker
	for {
		select {
		case <-ticker.C:
			if err := f.fetchAllFeeds(ctx); err != nil {
				log.Printf("Error fetching feeds: %v", err)
			}
		case <-ctx.Done():
			log.Println("Feed fetcher service stopped")
			return ctx.Err()
		}
	}
}

// In a real implementation, this would fetch all feeds from the database
// and then fetch the posts for each feed
func (f *FeedFetcher) fetchAllFeeds(ctx context.Context) error {
	// For now, this is just a placeholder
	log.Println("Fetching all feeds")
	return nil
}

// This function would fetch the posts for a feed and store them in the database
func (f *FeedFetcher) fetchFeed(ctx context.Context, feedURL string) error {
	// Fetch the feed
	feed, err := rss.FetchFeed(feedURL)
	if err != nil {
		return err
	}

	// Process each item in the feed
	for _, item := range feed.Channel.Items {
		// In a real implementation, we would parse the date and save the post
		// to the database
		log.Printf("Found post: %s", item.Title)
	}

	return nil
}
