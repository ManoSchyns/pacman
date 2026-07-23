# Project Management — Pac-Man 42

*Companion document to the [root README](../README.md).*

This directory documents **how** the activity was run: the workflow, the task
split, the timeline and the conventions we agreed on before writing any code.

---

## Team

| Login | GitHub | Role in this activity |
| :--- | :--- | :--- |
| **halexand** | [@Primordial-Devv](https://github.com/Primordial-Devv) | Sprites & animation, ghost behaviour, menu & UI, audio, global refactor |
| **mschyns** | [@ManoSchyns](https://github.com/ManoSchyns) | Maze integration, game & level engine, collectibles, scores, config parsing, packaging |

Repository: [`ManoSchyns/pacman`](https://github.com/ManoSchyns/pacman)

---

## Method

We worked in **short vertical slices**: one branch, one feature, one pull
request, one review. No feature was ever developed on `main`, and pull requests
were merged by the *other* member — with one exception, #14, which its own author
merged.

### Key numbers

| | |
| :--- | :---: |
| Duration | 14 days (09 → 22 July 2026) |
| Commits | 65 |
| Feature branches | 17 |
| Pull requests | 17 — all merged, none abandoned |
| Commits made directly on `main` | 3 — the initial commit, the day-one tooling bootstrap, and the final balancing pass |

### Branch convention

```
feature/<subject>     new functionality          feature/pacgums
Resolve/<subject>     fix on an existing feature Resolve/parsing
main                  always runnable
```

The rule we held to: **`main` must always launch.** Anything half-finished stays
on its branch. This is what let either of us pull `main` at any moment and have a
working base to build the next feature on.

### Pull request workflow

1. Branch off `main`.
2. Develop the feature, committing in French with an explicit description of what
   changed and why.
3. Run `make lint` — `flake8` **and** `mypy` must both be clean. Several commits
   in the history exist purely for this (`mise a la norme`, `flake8 et mypy`).
4. Open a pull request.
5. **The other member merges it.** Reading someone else's PR before merging is
   what kept both of us aware of the whole codebase rather than only our half.

### Communication

Day-to-day coordination happened in person and on Discord. Since the split was
made along module boundaries, merge conflicts stayed rare — the two structural
exceptions were handled explicitly by their own dedicated PRs (#4 packaging
reorganisation, #13 global refactor), each announced before being started.

---

## Task split

The division was not made by "one does the front, one does the back", but by
**game subsystem**, so that each of us owned a coherent domain end to end.

### halexand

| Domain | Delivered |
| :--- | :--- |
| **Sprites & animation** | Sprite-sheet auto-slicing, `Animation` primitive, all Pac-Man animations (4 directions + death), all four ghosts (4 directions, frightened, eaten, revive) |
| **Ghost behaviour** | First ghost integration into the maze, targeting logic, death logic and its link to the game-over screen |
| **Movement tuning** | Rework of Pac-Man's turn logic and speed for arcade feel |
| **Menu & UI** | Animated main menu, logo animation, chase parade, highscore and instruction pages |
| **Audio** | Sound-bank slicing, `AudioMixer`, channel roles, ducking, ambience state machine |
| **Refactor** | Global refactor pass (PR #13) that produced the current package layout |
| **Documentation** | Docstring pass across the whole codebase (PR #16), README |
| **Tooling** | Initial Makefile and `requirements.txt` |

### mschyns

| Domain | Delivered |
| :--- | :--- |
| **Maze** | A-Maze-ing integration, rendering, wall collisions, `is_open` navigation contract, spawn computation, scaling to screen |
| **Game engine** | `Game` / `Level` / `Player`, level chaining, per-level timer, pause, waiting screen, reset on death |
| **Collectibles** | Pac-gums and super pac-gums, spawning, scoring, ghost vulnerability and collisions |
| **Ghost flee** | Flee behaviour, per-level edible cooldown, real random seed for levels after the first |
| **Scores** | Name capture on the end screen, `Scores` persistence, validation, sorting, display |
| **Configuration** | JSON parsing, comment stripping, pydantic validation model, default fallbacks |
| **Packaging** | `package.sh`, PyInstaller build, `.gitignore`, guard against a non-functional maze package |
| **Balancing** | Final tuning pass — movement cooldown, level dimension bounds |

---

## Timeline

| Date | Milestone | PRs |
| :--- | :--- | :--- |
| **09 Jul** | Repository bootstrap, Makefile, dependencies, sprite separation | — |
| **10 Jul** | Maze v0 · Pac-Man animation · ghost animations · package reorganisation | #1 #2 #3 #4 |
| **13 Jul** | Game & level engine, timer, pause, first end screen · ghosts placed in the maze, death logic | #5 |
| **14 Jul** | Reset on life lost · menu interface started | #6 #7 #8 |
| **15 Jul** | Pac-gums, scoring, ghost collisions | #9 |
| **16 Jul** | Ghost flee behaviour, per-level vulnerability window, seeded levels | #10 |
| **17 Jul** | Highscore system and its display · audio | #11 |
| **18–20 Jul** | Audio integration merged · **global refactor** · config parsing | #12 #13 |
| **21 Jul** | Config parsing merged · PyInstaller packaging · non-functional-package guard | #14 #15 |
| **22 Jul** | Docstring pass · parsing fix · final balancing | #16 #17 |

---

## Pull request log

| # | Branch | Title | Author | Merged by |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `feature/animationPacman` | All sprites separated & Pac-Man animation | halexand | mschyns |
| 2 | `feature/maze` | Maze | mschyns | halexand |
| 3 | `feature/animationFantome` | Ghost animations + death / revive | halexand | mschyns |
| 4 | `feature/pacmanPlayer` | Package reorganisation + `PacmanPlayer` | mschyns | halexand |
| 5 | `feature/game` | Game engine | mschyns | halexand |
| 6 | `feature/comportementGhost` | Ghosts in maze, turn logic & speed rework | halexand | mschyns |
| 7 | `feature/level` | Reset ghosts and Pac-Man on life lost | mschyns | halexand |
| 8 | `feature/interface` | Interface — first pass | halexand | mschyns |
| 9 | `feature/pacgums` | Pac-gums | mschyns | halexand |
| 10 | `feature/ghost_fuite` | Ghost flee behaviour | mschyns | halexand |
| 11 | `feature/score` | End screen & highscores | mschyns | halexand |
| 12 | `feature/sound` | Sound, mixer & sound viewer | halexand | mschyns |
| 13 | `feature/refactor` | Global refactor | halexand | mschyns |
| 14 | `feature/parsing` | Configuration parsing | mschyns | mschyns |
| 15 | `feature/packaging` | Packaging | mschyns | halexand |
| 16 | `feature/dosctrings` | Docstrings on every function | halexand | mschyns |
| 17 | `Resolve/parsing` | Parsing fix | mschyns | halexand |

---

## Conventions

### Code

- **English** for identifiers, **French** for docstrings and commit messages.
- 79-column limit, `flake8` clean (`setup.cfg`).
- Fully annotated, `mypy` clean under `--disallow-untyped-defs`,
  `--check-untyped-defs`, `--warn-return-any`.
- A docstring on every function, class and module.
- **No inline comments in the code**: if a block needs explaining, it becomes a
  named function with a docstring. The few remaining comments mark section
  boundaries or credit external sources.
- One class per file, one domain per package, public surface declared in
  `__init__.py` via `__all__`.

### Repository hygiene

`pacman_env/`, `__pycache__/` and `.mypy_cache/` are git-ignored. Assets, the
arcade fonts and the vendored A-Maze-ing wheel are committed so that `make
install && make run` works on a fresh clone with no external download.

---

## Retrospective

### What worked

- **Splitting by subsystem, not by layer.** Each of us owned a domain end to end,
  which meant almost no blocking dependency on the other's work in progress.
- **Cross-merging pull requests.** Reading the other's code before merging kept
  both of us able to work anywhere in the codebase by the end.
- **Lint as a merge gate.** Enforcing `flake8` + `mypy` on every branch meant the
  final "norm pass" — usually a painful end-of-project chore — simply did not
  exist.
- **Seeded mazes.** Being able to reproduce an exact layout turned "the ghost
  sometimes gets stuck" into a bug we could actually sit down and fix.

### What we would do differently

- **Refactor earlier.** PR #13 came late; the module layout it produced should
  have been designed at the start rather than extracted afterwards.
- **Automated tests.** The project was validated by playing it. A test suite on
  `GridMovement`, the config validators and `Scores` would have caught
  regressions faster than replaying a level.
- **Write docstrings as we go.** Doing them in a single sweeping pass (PR #16)
  cost more than writing them alongside each function would have.
- **CI.** A GitHub Action running `make lint` on every pull request would have
  removed the manual step entirely.
