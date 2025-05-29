package main

import (
	"strings"
)

// cleanInput takes a string and returns a slice of strings
// It splits the input on whitespace, lowercases each word,
// and removes any leading/trailing spaces
func cleanInput(text string) []string {
	// Trim leading and trailing whitespace
	text = strings.TrimSpace(text)

	// If the text is empty after trimming, return an empty slice
	if len(text) == 0 {
		return []string{}
	}

	// Convert to lowercase
	text = strings.ToLower(text)

	// Split on whitespace
	words := strings.Fields(text)

	return words
}
