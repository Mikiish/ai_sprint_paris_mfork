#include <ncurses.h>
#include <deque>
#include <cstdlib>
#include <ctime>

// Size of the playfield
const int WIDTH = 20;
const int HEIGHT = 20;

// Directions the snake can move
enum Direction { UP, DOWN, LEFT, RIGHT };

struct Point {
    int x, y;
};

// Function prototypes
void init();
void draw(const std::deque<Point>& snake, const Point& food, int score);
void end();

int main() {
    std::deque<Point> snake;
    snake.push_back({WIDTH/2, HEIGHT/2});
    Direction dir = RIGHT;

    std::srand(std::time(nullptr));
    Point food{ std::rand() % WIDTH, std::rand() % HEIGHT };
    int score = 0;

    init();
    nodelay(stdscr, TRUE); // Non-blocking input
    keypad(stdscr, TRUE);  // Enable arrow keys

    bool running = true;
    while (running) {
        int ch = getch();
        switch (ch) {
            case KEY_UP:    if (dir != DOWN) dir = UP; break;
            case KEY_DOWN:  if (dir != UP) dir = DOWN; break;
            case KEY_LEFT:  if (dir != RIGHT) dir = LEFT; break;
            case KEY_RIGHT: if (dir != LEFT) dir = RIGHT; break;
            case 'q': running = false; break;
            default: break;
        }

        // Move snake
        Point head = snake.front();
        switch (dir) {
            case UP:    head.y--; break;
            case DOWN:  head.y++; break;
            case LEFT:  head.x--; break;
            case RIGHT: head.x++; break;
        }

        // Check collisions
        if (head.x < 0 || head.x >= WIDTH || head.y < 0 || head.y >= HEIGHT) {
            running = false;
        } else {
            for (const auto& p : snake) {
                if (p.x == head.x && p.y == head.y) {
                    running = false;
                    break;
                }
            }
        }
        if (!running) break;

        snake.push_front(head);
        if (head.x == food.x && head.y == food.y) {
            score++;
            food = { std::rand() % WIDTH, std::rand() % HEIGHT };
        } else {
            snake.pop_back();
        }

        draw(snake, food, score);
        napms(100); // Delay 100ms
    }

    end();
    return 0;
}

// Initialize ncurses
void init() {
    initscr();
    cbreak();
    noecho();
    curs_set(0);
}

// Draw the game state
void draw(const std::deque<Point>& snake, const Point& food, int score) {
    clear();
    for (int y = 0; y < HEIGHT; ++y) {
        for (int x = 0; x < WIDTH; ++x) {
            bool printed = false;
            if (food.x == x && food.y == y) {
                mvaddch(y, x, 'F');
                printed = true;
            }
            for (const auto& p : snake) {
                if (p.x == x && p.y == y) {
                    mvaddch(y, x, 'O');
                    printed = true;
                    break;
                }
            }
            if (!printed) mvaddch(y, x, '.');
        }
    }
    mvprintw(HEIGHT, 0, "Score: %d (q to quit)", score);
    refresh();
}

// End ncurses
void end() {
    nodelay(stdscr, FALSE);
    getch();
    endwin();
}
