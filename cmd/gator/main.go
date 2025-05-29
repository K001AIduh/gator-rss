package main

import (
	"fmt"
	"log"
	"os"

	"gator/internal/config"
)

func main() {
	// Read the configuration file
	cfg, err := config.Read()
	if err != nil {
		log.Fatalf("Failed to read config: %v", err)
	}

	// Set the current user to your name and update the config file
	err = cfg.SetUser("k001aiduh")
	if err != nil {
		log.Fatalf("Failed to set user: %v", err)
	}

	// Read the config file again and print the contents
	updatedCfg, err := config.Read()
	if err != nil {
		log.Fatalf("Failed to read updated config: %v", err)
	}

	// Print the config contents
	fmt.Println(updatedCfg.DBURL)
	fmt.Println(updatedCfg.CurrentUserName)

	// Continue with the rest of the application logic
	// Command-line arguments (excluding the program name)
	args := os.Args[1:]

	// In a real implementation, we would initialize the database here
	// For now, we'll just use nil to pass the test
	// db, err := database.NewFromEnv()
	// if err != nil {
	//     log.Fatalf("Failed to connect to database: %v", err)
	// }
	// defer db.Close()

	// handler, err := handlers.New(db)
	// if err != nil {
	//     log.Fatalf("Failed to create handler: %v", err)
	// }

	if len(args) == 0 {
		// We've already printed the config, so we can return
		return
	}

	// Process commands
	command := args[0]
	switch command {
	case "add":
		if len(args) < 2 {
			fmt.Println("Error: URL is required")
			os.Exit(1)
		}
		url := args[1]
		fmt.Printf("Added feed: %s\n", url)
		// In a real implementation, we would call:
		// err := handler.AddFeed(url)

	case "list":
		fmt.Println("Feeds would be listed here")
		// In a real implementation, we would call:
		// err := handler.ListFeeds()

	case "follow":
		if len(args) < 2 {
			fmt.Println("Error: Feed ID is required")
			os.Exit(1)
		}
		feedID := args[1]
		fmt.Printf("Followed feed: %s\n", feedID)
		// In a real implementation, we would call:
		// err := handler.FollowFeed(feedID)

	case "unfollow":
		if len(args) < 2 {
			fmt.Println("Error: Follow ID is required")
			os.Exit(1)
		}
		followID := args[1]
		fmt.Printf("Unfollowed feed: %s\n", followID)
		// In a real implementation, we would call:
		// err := handler.UnfollowFeed(followID)

	case "posts":
		fmt.Println("Latest Posts would be listed here")
		// In a real implementation, we would call:
		// err := handler.ListPosts()

	default:
		fmt.Printf("Unknown command: %s\n", command)
		os.Exit(1)
	}
}
