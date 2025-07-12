# Minimal Qt Interface for 2084-bit Numbers

Below are seven whimsical points of design, each followed by a suggested development task.

1. **Randomness Wrangling** – Ensure our number generator is isolated in a single header.
   - *Task:* Provide `big_random.hpp` with `generateRandom2084Bit()`.
2. **Pointer Playground** – Manage history storage via raw pointers just for fun.
   - *Task:* Maintain a `cpp_int history[3][3][3]` buffer and a pointer moving through it.
3. **Copy Convenience** – One click should place the number onto the clipboard.
   - *Task:* Hook a Qt button to `QClipboard`.
4. **Display Discipline** – Prevent edits by using a read‑only text box.
   - *Task:* Configure `QTextEdit` to be read‑only and present the result.
5. **Layout Laziness** – Keep the UI vertical and straightforward.
   - *Task:* Stack widgets with `QVBoxLayout`.
6. **Integration Insight** – The generator should be callable from other modules.
   - *Task:* Separate the GUI (`main_gui.cpp`) from the logic (`big_random.hpp`).
7. **Build Bravery** – Compile everything with Qt5, no magic involved.
   - *Task:* Use `g++ main_gui.cpp -o gui_app $(pkg-config --cflags --libs Qt5Widgets)`.

## Function roles
- `generateRandom2084Bit()` – Returns a freshly minted 2084‑bit integer.
- `main()` – Launches the Qt application, handles UI events, and stores history.

## Libraries
- **Boost.Multiprecision** – Manipulates integers beyond 64 bits.
- **Qt5 Widgets** – Provides `QApplication`, `QTextEdit`, buttons, layouts and clipboard access.

## Compilation
```bash
cd gui
g++ -std=c++17 main_gui.cpp -o gui_app $(pkg-config --cflags --libs Qt5Widgets)
```
Then run `./gui_app` to open the window.

## Final note
> Bon courage, tu vas en avoir besoin. Au moins le Génie sait où il range ses pointeurs!
