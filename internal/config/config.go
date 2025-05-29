package config

import (
	"encoding/json"
	"os"
	"path/filepath"
)

const configFileName = ".gatorconfig.json"

// Config represents the application configuration
type Config struct {
	DBURL           string `json:"db_url"`
	CurrentUserName string `json:"current_user_name,omitempty"`
}

// Read reads the configuration file and returns a Config struct
func Read() (Config, error) {
	var cfg Config

	filePath, err := getConfigFilePath()
	if err != nil {
		return cfg, err
	}

	data, err := os.ReadFile(filePath)
	if err != nil {
		return cfg, err
	}

	err = json.Unmarshal(data, &cfg)
	if err != nil {
		return cfg, err
	}

	return cfg, nil
}

// SetUser sets the current user and writes the config to disk
func (c *Config) SetUser(username string) error {
	c.CurrentUserName = username
	return write(*c)
}

// getConfigFilePath returns the absolute path to the config file
func getConfigFilePath() (string, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}
	return filepath.Join(homeDir, configFileName), nil
}

// write writes the config to disk
func write(cfg Config) error {
	filePath, err := getConfigFilePath()
	if err != nil {
		return err
	}

	data, err := json.Marshal(cfg)
	if err != nil {
		return err
	}

	return os.WriteFile(filePath, data, 0644)
}
