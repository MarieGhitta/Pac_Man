*This project has been created as part of the 42 curriculum by mghitta, jpik.*

# Pac-Man

## Description
<!-- A “Description” section that clearly presents the project, including its goal and a brief overview. -->
This project is a Python implementation of the classic Pac-Man arcade game.
The game uses an external maze generator, a JSON configuration file, object-oriented programming and a graphical interface built with pygame.
The project was designed with a modular architecture separating configuration loading, maze generation, game logic and rendering.

## Instructions
<!-- An “Instructions” section containing any relevant information about compilation, installation, and/or execution. -->

## Resources
<!-- A “Resources” section listing classic references related to the topic (documentation, articles, tutorials, etc.), as well as a description of how AI was used — specifying for which tasks and which parts of the project. -->
- Pygame documentation: https://www.pygame.org/docs/
- Pygame tutorials: http://pygametutorials.wikidot.com/tutorials-basic
- Pac-Man game: https://freepacman.org
- infos Pac-Man: https://fr.wikipedia.org/wiki/Pac-Man



## Features
- JSON configuration with comments support.
- Robust configuration parsing with safe default values.
- Integration of an external maze generator.
- Randomly generated playable mazes.
- Autonomous ghosts with multiple behaviours.
- Pacgum and Super Pacgum system.
- Multi-level progression.
- Score management.
- Collision handling.
- Modular object-oriented architecture.

### Configuration
<!-- A Configuration section explaining the config file structure and default values. -->
The game is configured through a JSON file.

Supported parameters include:

- highscore_filename
- levels
- width
- height
- lives
- pacgum
- points_per_pacgum
- points_per_super_pacgum
- points_per_ghost
- seed
- level_max_time

The configuration loader:

- ignores comment lines beginning with `#` or `//`;
- validates value types;
- replaces invalid values with safe defaults;
- ignores unknown keys;
- reports configuration problems without crashing.

### Highscore
<!-- A Highscore section explaining how the highscore system works and why you decided to implement it this way. -->

### Maze Generation
<!-- A Maze Generation section explaining how the assigned A-Maze-ing package is used to generate mazes. -->
The project does not implement its own maze generator.
Instead, it integrates the external A-Maze-ing package provided during the project.
An adapter converts the generated maze into the project's internal representation while keeping the game independent from the external library implementation.

### Implementation
<!-- An Implementation section with a technical summary of your implementation. -->
The game engine is based on a continuous update loop.

Each iteration:

1. updates the global ghost state;
2. updates the player;
3. updates all ghosts;
4. checks collisions;
5. redraws the game.

The player:

- moves inside maze corridors only;
- collects pacgums and super pacgums;
- progresses to the next level when all pacgums have been collected.

Ghosts implement several behaviours:

- Chase
- Scatter
- Frightened
- Respawn

Super pacgums temporarily switch every ghost to the frightened state.

When a frightened ghost is eaten, it returns to its spawn position before becoming active again.

### General Software Architecture
<!-- A General Software Architecture section, with high-level overview of the software architecture (modules, classes, and their relationships). -->
The project follows a modular object-oriented architecture.

The main modules are:

- `config`
  - configuration loading and validation

- `maze`
  - maze generation adapter
  - maze models

- `game`
  - game loop
  - player
  - ghosts
  - level management
  - scoring
  - collision handling

- `renderer`
  - graphical rendering

### Project Management
<!-- A Project Management section, with a brief overview of how you managed the project and a link to the dedicated project management directory. -->
