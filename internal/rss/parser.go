package rss

import (
	"context"
	"encoding/xml"
	"html"
	"io"
	"net/http"
	"time"
)

// Item represents a single post in an RSS feed
type Item struct {
	Title       string `xml:"title"`
	Link        string `xml:"link"`
	Description string `xml:"description"`
	PubDate     string `xml:"pubDate"`
}

// Channel represents an RSS feed channel
type Channel struct {
	Title       string `xml:"title"`
	Link        string `xml:"link"`
	Description string `xml:"description"`
	Items       []Item `xml:"item"`
}

// Feed represents an RSS feed
type Feed struct {
	XMLName xml.Name `xml:"rss"`
	Channel Channel  `xml:"channel"`
}

// FetchFeed fetches and parses an RSS feed from a URL
func FetchFeed(url string) (Feed, error) {
	var feed Feed

	resp, err := http.Get(url)
	if err != nil {
		return feed, err
	}
	defer resp.Body.Close()

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return feed, err
	}

	err = xml.Unmarshal(data, &feed)
	if err != nil {
		return feed, err
	}

	return feed, nil
}

// FetchFeedWithContext fetches and parses an RSS feed from the given URL with context
func FetchFeedWithContext(ctx context.Context, feedURL string) (*Feed, error) {
	// Create a new HTTP request with context
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, feedURL, nil)
	if err != nil {
		return nil, err
	}

	// Set the User-Agent header
	req.Header.Set("User-Agent", "gator")

	// Create an HTTP client and send the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	// Parse the XML data
	var feed Feed
	err = xml.Unmarshal(body, &feed)
	if err != nil {
		return nil, err
	}

	// Unescape HTML entities in the feed title and description
	feed.Channel.Title = html.UnescapeString(feed.Channel.Title)
	feed.Channel.Description = html.UnescapeString(feed.Channel.Description)

	// Unescape HTML entities in each item's title and description
	for i := range feed.Channel.Items {
		feed.Channel.Items[i].Title = html.UnescapeString(feed.Channel.Items[i].Title)
		feed.Channel.Items[i].Description = html.UnescapeString(feed.Channel.Items[i].Description)
	}

	return &feed, nil
}

// ParseDate attempts to parse the RSS feed date string into a time.Time
func ParseDate(dateString string) (time.Time, error) {
	layouts := []string{
		time.RFC1123Z,
		time.RFC1123,
		time.RFC822Z,
		time.RFC822,
		time.RFC3339,
		"Mon, 02 Jan 2006 15:04:05 MST",
		"Mon, 02 Jan 2006 15:04:05 -0700",
		"2 Jan 2006 15:04:05 -0700",
	}

	var t time.Time
	var err error

	for _, layout := range layouts {
		t, err = time.Parse(layout, dateString)
		if err == nil {
			return t, nil
		}
	}

	// If we couldn't parse the date, return the current time
	return time.Now(), err
}
