# PAC-MAN

A Pac-Man game made with Python and Pygame.

## Installation

### Requirements

* Python 3.10 or newer
* `uv`
* `make`

### Install

Extract the downloaded archive, open a terminal in the `Pac-Man` folder, then run:

```bash
make install
```

This installs the required dependencies and creates the project environment.

## Launch

To start the game:

```bash
make run
```

The game opens in fullscreen mode.

## Controls

* **Arrow keys** — Move Pac-Man
* **P** — Pause / Resume
* **Enter** — Confirm / Select
* **Escape** — Pause / Return
* **Q** — Quit

## Gameplay

* Eat Pac-Gums to earn points.
* Super Pac-Gums temporarily make ghosts vulnerable.
* Avoid the ghosts.
* Clear the maze to progress through the levels.
* Try to achieve the highest score possible!

## Configuration

The game can be configured through the included `config.json` file.

Available options include:

* Number of lives
* Number of levels
* Level time limit
* Pac-Gum points
* Super Pac-Gum points
* Ghost points
* Maze generation seed
* High-score file

The default configuration is ready to play and does not need to be modified.

Have fun! 👾
