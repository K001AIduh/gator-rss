package utils

import (
	"time"

	"github.com/google/uuid"
)

// GenerateUUID generates a new UUID
func GenerateUUID() uuid.UUID {
	return uuid.New()
}

// TimeNow returns the current time
func TimeNow() time.Time {
	return time.Now().UTC()
}

// FormatTime formats a time.Time into a string
func FormatTime(t time.Time) string {
	return t.Format(time.RFC3339)
}
