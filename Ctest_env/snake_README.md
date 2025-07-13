# Minimal Snake Game in C++

## 7 Semi-Improbable Structural Thoughts
1. **Grid as Universe** - Treat the 20x20 grid like a self-contained cosmos.
   - *Task:* Ensure coordinates wrap or end at borders. Here we chose border collision for simplicity.
2. **Deque for Body Dynamics** - Using `std::deque` lets the snake grow at the head and shrink at the tail.
   - *Task:* Push front for movement, pop back unless food eaten.
3. **Ncurses for Terminal Life** - `ncurses` gives us real-time keyboard and drawing without manual ANSI escapes.
   - *Task:* Initialize ncurses, enable non-blocking input, and refresh screen each tick.
4. **Random Food Placement** - Food appears at random positions using `std::rand()` seeded by `std::time`.
   - *Task:* Regenerate food location whenever eaten.
5. **Direction Control** - Arrow keys map to an enum; switching prevents direct reverse moves.
   - *Task:* Guard against immediate 180° turns to avoid self-collision glitches.
6. **Frame Timing** - `napms(100)` acts as a crude game loop delay.
   - *Task:* Adjust delay for difficulty or smoothness.
7. **Simple Collision Detection** - Check borders and self-intersection each tick.
   - *Task:* End the game when collision occurs, display score.

## File Summary
- `snake.cpp` — Implements the entire game using ncurses.
- `snake_README.md` — You are reading it: design notes, build instructions, and a snarky farewell.

## Function Roles
- `init()` — Sets up the ncurses environment.
- `draw()` — Renders the grid, snake, food, and score on each frame.
- `end()` — Restores the terminal to normal upon quitting.
- `main()` — Runs the game loop and manages state.

## Libraries
- **`<ncurses.h>`** — Terminal graphics and keyboard handling.
- **`<deque>`** — Manages the snake body.
- **`<cstdlib>` / `<ctime>`** — Randomness and seeding for food placement.

## Compile & Run
```bash
# From the repository root
cd Ctest_env
g++ snake.cpp -lncurses -o snake
./snake
```

## Brief Walkthrough of Code Blocks
1. **Includes & constants** — bring in libraries and define board size.
2. **Structs & enums** — represent points and movement directions.
3. **Game initialization** — seed RNG, set up snake and food, start ncurses.
4. **Input handling** — arrow keys modify direction; 'q' exits.
5. **Movement and collision** — compute new head, test boundaries and self-hit.
6. **Food logic** — check if the snake eats; grow or move accordingly.
7. **Rendering** — clear screen, draw each cell, show score.

## Sarcastic Advice
*Bonne chance,* you’re about to discover that a tiny snake in C++ can swallow hours of your time. But hey, at least your terminal has never looked so retro.
