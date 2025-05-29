package main

import (
	"reflect"
	"testing"
)

func TestCleanInput(t *testing.T) {
	cases := []struct {
		input    string
		expected []string
	}{
		{
			input:    "hello world",
			expected: []string{"hello", "world"},
		},
		{
			input:    "  hello  world  ",
			expected: []string{"hello", "world"},
		},
		{
			input:    "Charmander Bulbasaur PIKACHU",
			expected: []string{"charmander", "bulbasaur", "pikachu"},
		},
		{
			input:    "",
			expected: []string{},
		},
		{
			input:    "   ",
			expected: []string{},
		},
		{
			input:    "catch pikachu",
			expected: []string{"catch", "pikachu"},
		},
	}

	for _, c := range cases {
		actual := cleanInput(c.input)

		// Check the length of the actual slice against the expected slice
		if len(actual) != len(c.expected) {
			t.Errorf("cleanInput(%q) returned %d words, expected %d",
				c.input, len(actual), len(c.expected))
			continue
		}

		// Check each word in the slice
		for i := range actual {
			word := actual[i]
			expectedWord := c.expected[i]
			if word != expectedWord {
				t.Errorf("cleanInput(%q)[%d] == %q, expected %q",
					c.input, i, word, expectedWord)
			}
		}

		// Alternative approach using reflect.DeepEqual
		if !reflect.DeepEqual(actual, c.expected) {
			t.Errorf("cleanInput(%q) == %v, expected %v",
				c.input, actual, c.expected)
		}
	}
}
