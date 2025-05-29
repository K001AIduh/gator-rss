package pokecache

import (
	"sync"
	"time"
)

// Cache represents a thread-safe cache with automatic expiration
type Cache struct {
	data     map[string]cacheEntry
	mutex    sync.Mutex
	interval time.Duration
}

// cacheEntry represents a single cache entry with its creation time
type cacheEntry struct {
	createdAt time.Time
	val       []byte
}

// NewCache creates a new cache with the given reaping interval
func NewCache(interval time.Duration) *Cache {
	cache := &Cache{
		data:     make(map[string]cacheEntry),
		interval: interval,
	}

	go cache.reapLoop()

	return cache
}

// Add adds a new entry to the cache
func (c *Cache) Add(key string, val []byte) {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	c.data[key] = cacheEntry{
		createdAt: time.Now(),
		val:       val,
	}
}

// Get retrieves an entry from the cache if it exists
func (c *Cache) Get(key string) ([]byte, bool) {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	entry, ok := c.data[key]
	if !ok {
		return nil, false
	}

	return entry.val, true
}

// reapLoop periodically removes expired entries from the cache
func (c *Cache) reapLoop() {
	ticker := time.NewTicker(c.interval)
	defer ticker.Stop()

	for range ticker.C {
		c.reap()
	}
}

// reap removes expired entries from the cache
func (c *Cache) reap() {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	now := time.Now()

	for key, entry := range c.data {
		if now.Sub(entry.createdAt) > c.interval {
			delete(c.data, key)
		}
	}
}
