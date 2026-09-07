*This project has been created as part of the 42 curriculum by mghitta, jpik.*

# Pac-Man

## Description

This project is a Python implementation of the classic 1980 Pac-Man arcade game. It uses an externally provided maze generator (the A-Maze-ing package), a JSON configuration file, object-oriented design, and a graphical interface built with pygame.

The game reproduces the original arcade rules and ghost behaviours as reverse-engineered by Jamey Pittman: four ghosts with distinct AI personalities, the original Chase/Scatter timing table, per-level speed tuning, and a Frightened state triggered by super-pacgums. On top of the core game it adds a full menu flow (title, pause, instruction, cheat, highscore and end screens), a persistent top-10 highscore board, a level timer, and a cheat mode for testing/demo purposes.

## Instructions

### Requirements

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) as package/dependency manager
- pygame >= 2.6.1 (installed automatically by uv)
- The A-Maze-ing wheel vendored at `libs/mazegenerator-2.1.0-py3-none-any.whl`

### Installation

```bash
uv sync
```

### Running the game

The program takes exactly one mandatory argument: the path to a JSON configuration file.

```bash
uv run python pac-man.py config.json
```

Any missing or extra argument is reported with a clear message and a clean exit.

### Controls

| Key            | Action                                   |
|----------------|-------------------------------------------|
| Arrow keys     | Move Pac-Man / navigate menus             |
| Enter          | Validate a menu selection                 |
| Left / Right   | Cycle a value (e.g. the "Add Life" cheat) |
| Escape / P     | Pause the game                            |
| Q              | Quit (title screen or in-game)            |
| Backspace      | Delete a character when entering a name   |

### Note on display

The game launches in fullscreen (`pygame.FULLSCREEN | pygame.SCALED`) at the monitor's native resolution. On Linux desktops using fractional display scaling (e.g. GNOME at 125%), this can cause flickering; setting the display scale to 100% avoids the issue.

## Resources

- [Pygame documentation](https://www.pygame.org/docs/)
- [Pygame tutorials](http://pygametutorials.wikidot.com/tutorials-basic)
- [Pac-Man (reference implementation)](https://freepacman.org)
- [Pac-Man — Wikipedia (FR)](https://fr.wikipedia.org/wiki/Pac-Man)
- [The Pac-Man Dossier](https://pacman.holenet.info/)

### AI usage

An AI assistant (Claude, ChatGPT) was used throughout the project as a support tool, under the same rule for every session: it could propose but never decide or write production code unilaterally — all changes were reviewed and validated by the author before being applied.

- **Code review**: recurring passes over the codebase to spot bugs, inconsistencies, and deviations from the intended arcade behaviour (ghost AI, timing, cheat logic, rendering). Findings were proposed as fixes, validated, then implemented and logged.
- **Docstrings**: generating module/class/method docstrings for several files, following the project's own conventions (Google-style Args/Returns, lines under 80 characters).
- **Discussion**: sounding board for architecture and design trade-offs (e.g. tile-based vs. continuous movement, Manhattan vs. Euclidean ghost targeting) — the final decision and implementation remained the author's.

No game logic, ghost AI, or rendering code was generated wholesale by AI; implementation work was written and understood by the author.

## Features

- JSON configuration with `#`/`//` comment support.
- Robust configuration parsing: invalid or missing values fall back to safe defaults, unknown keys are ignored, no crash on a malformed file.
- Integration of the external A-Maze-ing maze generator via a dedicated adapter, keeping the game logic independent from its implementation.
- A fixed-seed maze for level 1, randomly generated mazes for every subsequent level.
- Four autonomous ghosts (Blinky, Pinky, Inky, Clyde) with distinct targeting logic, faithful to the original 1980 arcade AI, including the historical Chase/Scatter phase sequence and per-level speed tables.
- Pacgum and Super Pacgum system, with a Frightened state and a ghost-eating combo score multiplier (200 → 400 → 800 → 1600 points).
- Multi-level progression with a per-level countdown timer.
- Score capped at the original arcade maximum (3,333,360 points).
- Smooth rendering: continuous floating-point movement for Pac-Man and frame interpolation for ghosts, decoupled from the tile-based simulation.
- Animated pixel-art sprites: Pac-Man's mouth animation and death sequence, ghost Frightened/Flicker/eyes-only (Respawn) variants.
- Full screen flow: title screen, in-game HUD, pause menu, end screen (Game Over / Victory) with player name entry, and a highscore screen.
- Cheat mode (toggleable from the title and pause menus): invincibility, ghost freeze, speed boost, infinite time, infinite lives, extra lives, level skip, instant win, instant lose — intended for testing and demos.
- Persistent top-10 highscore system.
- Dynamic, resolution-independent fullscreen rendering.
- Modular, object-oriented architecture.

## Configuration

The game is configured through a single JSON file, passed as a command-line argument.

Supported keys:

| Key                       | Default        | Notes                                              |
|---------------------------|----------------|-----------------------------------------------------|
| `highscore_filename`      | `highscores.json` | Path to the persistent highscore file           |
| `levels`                  | *(required)*   | Array of `{width, height}` objects, one per level  |
| `max_levels`              | `10`           | Total number of levels played (10–99)              |
| `lives`                   | `3`            | Starting lives (1–99)                              |
| `pacgum`                  | `0`            | Number of pacgums to place; `0` fills all available walkable cells |
| `points_per_pacgum`       | `10`           | Points per pacgum (0–100)                          |
| `points_per_super_pacgum` | `50`           | Points per super-pacgum (0–500)                    |
| `points_per_ghost`        | `200`          | Base points per ghost eaten, before the combo multiplier (0–2000) |
| `seed`                    | `42`           | RNG seed used for level 1's maze only               |
| `level_max_time`          | `90`           | Seconds allowed per level before a life is lost (10–90) |

Each entry in `levels` provides its own `width`/`height` (3–101); if more levels are requested (`max_levels`) than entries are provided, the last entry is reused for the remaining levels.

Comments starting with `#` or `//` are stripped before parsing. Invalid types or out-of-range values print a warning and fall back to the default shown above; unknown keys are silently ignored; a completely missing or unparsable file produces a clear error message instead of a crash.

## Highscore

The highscore system is a simple, persistent top-10 leaderboard stored as a JSON file (path set by `highscore_filename`).

- Scores are loaded once at startup and re-saved after every completed game (win or lose).
- Player names are validated separately from scores (`PlayerScore`): 3–10 characters, alphanumeric and spaces only. Scores must be non-negative integers.
- On save, the new entry is appended, the list is sorted by score (descending), and truncated to the top 10. If the new score makes the cut, its rank is used to highlight (blink) it on the Highscore screen.
- The system is robust to a missing file (created fresh), a corrupted file, and permission errors — none of these crash the game.

## Maze Generation

The project does not implement its own maze generator. Instead, it integrates the external **A-Maze-ing** package (vendored as a wheel under `libs/`), used as-is and never modified, as required by the project subject.

- `MazeFactory` (`src/maze/generator.py`) wraps the library call (`perfect=False`, so the maze includes loops rather than a strict tree — required for Pac-Man-style corridors), passing the requested width, height and seed.
- `MazeAdapter` (`src/maze/adapter.py`) converts the library's raw integer matrix (a wall bitmask per cell) into the project's own `Maze`/`Cell` models, so the rest of the codebase never depends on the external library's data format directly.

## Implementation

The game runs on a single continuous update loop (`Engine.update()`), called once per frame:

1. Apply active cheat flags (invincibility, infinite lives, etc.).
2. Advance the pre-level countdown, or the death-animation freeze, if either is active (both pause the simulation).
3. Update the per-level countdown timer; a level timeout costs a life.
4. Advance the global ghost Chase/Scatter phase (the original 8-phase timed sequence, indexed by level bracket).
5. Move Pac-Man continuously toward the next tile (floating-point position), handling direction changes, corridor collisions, pacgum/super-pacgum collection, and level completion.
6. Move each ghost on its own tile-based tick, at a delay that depends on its state (Scatter/Chase/Frightened/Respawn) and the current level bracket, using arcade-accurate targeting for each ghost type.
7. Check player/ghost collisions (skipped while the "ghost freeze" cheat is active) and resolve eating a ghost or losing a life.
8. Hand off to the renderer.

Ghost targeting follows the original 1980 arcade logic: Blinky targets Pac-Man directly, Pinky targets 4 tiles ahead of Pac-Man (including its well-known overflow bug on an upward heading), Inky computes a vector from Blinky through a pivot point 2 tiles ahead of Pac-Man and doubles it, and Clyde switches between chasing Pac-Man and retreating to its corner based on a distance threshold. Ghosts choose the best available direction toward their target using Manhattan distance (Euclidean distance is used only for Clyde's distance threshold, matching the reference dossier); this deviates slightly from the strictly Euclidean pathfinding described in the dossier, a deliberate trade-off to avoid ghosts looping indefinitely on procedurally generated mazes.

Rendering interpolates ghost positions between ticks for smooth motion, while Pac-Man moves at a genuinely continuous (sub-tile) speed, so movement feels responsive regardless of the underlying tile-based simulation.

## General Software Architecture

The project follows a modular, object-oriented architecture:

```
pac-man.py                     → entry point (CLI argument, error handling)
src/
    app.py                     → App: pygame lifecycle, screen state machine
    config/
        loader.py               → ConfigLoader: JSON parsing & validation
        models.py                → Config, LevelConfig
    game/
        cheat.py                 → Cheat: shared cheat-mode flags
        engine.py                 → Engine: game loop, rules, scoring, timing
        player.py                → Player: position, direction, movement state
        ghost.py                  → Ghost: AI targeting, movement, state
        level.py                  → Level: maze content, spawn placement
        cell_content.py           → CellContent enum
    maze/
        generator.py              → MazeFactory: wraps the external library
        adapter.py                → MazeAdapter: external format → internal models
        models.py                 → Maze, Cell
    renderer/
        renderer.py               → Renderer: draws maze, entities, HUD
        sprite.py                 → Sprite (ABC), PacmanSprite, GhostSprite, SuperPacgumSprite
    ui/
        highscore.py              → Highscore, persistent top-10 storage
        models.py                 → PlayerScore: name/score validation
        screens/
            screen.py               → Screen (ABC): shared menu/drawing helpers
            title_screen.py         → Main menu
            game_screen.py          → In-game screen, delegates to Engine/Renderer
            pause_screen.py         → Pause menu
            instruction_screen.py   → Instruction screen
            cheat_screen.py         → CheatScreen, PauseCheatScreen
            end_screen.py           → Game Over / Victory screen, name entry
            highscore_screen.py     → Top-10 leaderboard display
    utils/
        color.py                  → Color: shared color palette
        screen_state.py           → ScreenState enum (screen state machine)
        sprite_enums.py            → Direction, GhostType, GhostState, PacmanState
exploration/mazegenerator/      → external A-Maze-ing package — never modified
```

`App` owns the top-level pygame loop and a `dict[ScreenState, Screen]` mapping; each frame, it delegates event handling, update and drawing to the active `Screen` and reacts to the `next_screen` transition it emits.
`GameScreen` is the only screen that talks to `Engine` (game rules) and `Renderer` (drawing) — every other screen only touches its own UI state and the shared `Cheat` object.

## Project Management

The project was developed following a GitHub Flow workflow: one short-lived branch per feature or fix, opened as a pull request into `main`, reviewed before merge, and deleted afterward. Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) format (`feat:`, `fix:`, `refactor:`, `chore:`, ...).
