package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"

	"github.com/k001aiduh/pokedexcli/internal/pokeapi"
)

type cliCommand struct {
	name        string
	description string
	callback    func(*config, ...string) error
}

type config struct {
	pokeapiClient       pokeapi.Client
	nextLocationAreaURL *string
	prevLocationAreaURL *string
	caughtPokemon       map[string]pokeapi.Pokemon
}

func getCommands() map[string]cliCommand {
	return map[string]cliCommand{
		"help": {
			name:        "help",
			description: "Displays a help message",
			callback:    commandHelp,
		},
		"exit": {
			name:        "exit",
			description: "Exit the Pokedex",
			callback:    commandExit,
		},
		"map": {
			name:        "map",
			description: "Display the next 20 location areas",
			callback:    commandMap,
		},
		"mapb": {
			name:        "mapb",
			description: "Display the previous 20 location areas",
			callback:    commandMapBack,
		},
		"explore": {
			name:        "explore",
			description: "Explore a location area to see available Pokemon",
			callback:    commandExplore,
		},
		"catch": {
			name:        "catch",
			description: "Attempt to catch a Pokemon",
			callback:    commandCatch,
		},
		"inspect": {
			name:        "inspect",
			description: "View details about a caught Pokemon",
			callback:    commandInspect,
		},
		"pokedex": {
			name:        "pokedex",
			description: "List all caught Pokemon",
			callback:    commandPokedex,
		},
	}
}

func main() {
	cfg := config{
		pokeapiClient: pokeapi.NewClient(),
		caughtPokemon: make(map[string]pokeapi.Pokemon),
	}

	cmdMap := getCommands()

	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("Pokedex > ")
		if !scanner.Scan() {
			break
		}

		input := scanner.Text()
		cleaned := cleanInput(input)

		if len(cleaned) == 0 {
			continue
		}

		commandName := cleaned[0]
		command, exists := cmdMap[commandName]

		if exists {
			args := []string{}
			if len(cleaned) > 1 {
				args = cleaned[1:]
			}

			err := command.callback(&cfg, args...)
			if err != nil {
				fmt.Println(err)
			}
		} else {
			fmt.Printf("Unknown command: %s\n", commandName)
		}
	}
}

func commandHelp(cfg *config, args ...string) error {
	fmt.Println("Welcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println()

	commands := getCommands()

	// Print command descriptions
	for _, cmd := range commands {
		fmt.Printf("%s: %s\n", cmd.name, cmd.description)
	}

	return nil
}

func commandExit(cfg *config, args ...string) error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

func commandMap(cfg *config, args ...string) error {
	// Get the location areas
	resp, err := cfg.pokeapiClient.GetLocationAreas(cfg.nextLocationAreaURL)
	if err != nil {
		return err
	}

	// Update the next and previous URLs
	cfg.nextLocationAreaURL = resp.Next
	cfg.prevLocationAreaURL = resp.Previous

	// Print the location areas
	for _, area := range resp.Results {
		fmt.Println(area.Name)
	}

	return nil
}

func commandMapBack(cfg *config, args ...string) error {
	if cfg.prevLocationAreaURL == nil {
		fmt.Println("You're on the first page")
		return nil
	}

	// Get the previous location areas
	resp, err := cfg.pokeapiClient.GetLocationAreas(cfg.prevLocationAreaURL)
	if err != nil {
		return err
	}

	// Update the next and previous URLs
	cfg.nextLocationAreaURL = resp.Next
	cfg.prevLocationAreaURL = resp.Previous

	// Print the location areas
	for _, area := range resp.Results {
		fmt.Println(area.Name)
	}

	return nil
}

func commandExplore(cfg *config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("Please provide a location area name")
	}

	areaName := args[0]
	fmt.Printf("Exploring %s...\n", areaName)

	locationResp, err := cfg.pokeapiClient.GetLocationArea(areaName)
	if err != nil {
		return err
	}

	fmt.Println("Found Pokemon:")
	for _, encounter := range locationResp.PokemonEncounters {
		fmt.Printf(" - %s\n", encounter.Pokemon.Name)
	}

	return nil
}

func commandCatch(cfg *config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("Please provide a Pokemon name")
	}

	pokemonName := args[0]

	// Check if already caught
	if _, ok := cfg.caughtPokemon[pokemonName]; ok {
		return fmt.Errorf("You've already caught %s!", pokemonName)
	}

	fmt.Printf("Throwing a Pokeball at %s...\n", pokemonName)

	// Get Pokemon data
	pokemon, err := cfg.pokeapiClient.GetPokemon(pokemonName)
	if err != nil {
		return err
	}

	// Calculate catch probability based on base experience
	// The higher the base experience, the lower the catch probability
	catchProbability := calculateCatchProbability(pokemon.BaseExperience)

	// Generate random number to determine if Pokemon is caught
	randNum := rand.Float64()

	if randNum <= catchProbability {
		fmt.Printf("%s was caught!\n", pokemonName)
		cfg.caughtPokemon[pokemonName] = pokemon
		fmt.Println("You may now inspect it with the inspect command.")
	} else {
		fmt.Printf("%s escaped!\n", pokemonName)
	}

	return nil
}

func commandInspect(cfg *config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("Please provide a Pokemon name")
	}

	pokemonName := args[0]

	// Check if the Pokemon has been caught
	pokemon, ok := cfg.caughtPokemon[pokemonName]
	if !ok {
		return fmt.Errorf("You have not caught that pokemon")
	}

	// Display Pokemon information
	fmt.Printf("Name: %s\n", pokemon.Name)
	fmt.Printf("Height: %d\n", pokemon.Height)
	fmt.Printf("Weight: %d\n", pokemon.Weight)

	// Display stats
	fmt.Println("Stats:")
	for _, stat := range pokemon.Stats {
		fmt.Printf("  -%s: %d\n", stat.Stat.Name, stat.BaseStat)
	}

	// Display types
	fmt.Println("Types:")
	for _, typeInfo := range pokemon.Types {
		fmt.Printf("  - %s\n", typeInfo.Type.Name)
	}

	return nil
}

func commandPokedex(cfg *config, args ...string) error {
	if len(cfg.caughtPokemon) == 0 {
		fmt.Println("Your Pokedex is empty! Try catching some Pokemon first.")
		return nil
	}

	fmt.Println("Your Pokedex:")
	for name := range cfg.caughtPokemon {
		fmt.Printf(" - %s\n", name)
	}

	return nil
}

// calculateCatchProbability returns a probability (0.0 to 1.0) based on the Pokemon's base experience
func calculateCatchProbability(baseExp int) float64 {
	// Define base probability
	baseProbability := 0.5

	// Adjust based on base experience
	// Higher base experience = lower probability
	// This formula gives a range from about 0.1 (high base exp) to 0.9 (low base exp)
	adjustedProbability := baseProbability - (float64(baseExp) / 1000.0)

	// Ensure probability is between 0.1 and 0.9
	if adjustedProbability < 0.1 {
		return 0.1
	}
	if adjustedProbability > 0.9 {
		return 0.9
	}

	return adjustedProbability
}
