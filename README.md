# Pokedex CLI

A command-line REPL Pokedex application that uses the PokéAPI to fetch and display Pokemon data.

## Features

- Browse location areas where Pokemon can be found
- Explore specific locations to see available Pokemon
- Catch Pokemon with a simulated probability
- Inspect details of caught Pokemon
- View your Pokedex with all caught Pokemon
- Caching system to improve performance and reduce API calls

## Commands

- `help` - Display help message with available commands
- `exit` - Exit the application
- `map` - Display the next 20 location areas
- `mapb` - Display the previous 20 location areas
- `explore [location]` - Explore a location area for Pokemon
- `catch [pokemon]` - Attempt to catch a Pokemon
- `inspect [pokemon]` - View details about a caught Pokemon
- `pokedex` - List all caught Pokemon

## How to Run

Make sure you have Go installed, then run:

```
go run main.go
```

## Dependencies

- Standard Go libraries only
  - `bufio` - For reading user input
  - `encoding/json` - For parsing JSON responses
  - `net/http` - For making HTTP requests to the PokéAPI
  - `time` - For caching

No external dependencies required.

## Data Source

This application uses the [PokéAPI](https://pokeapi.co/), a free RESTful Pokemon API.
