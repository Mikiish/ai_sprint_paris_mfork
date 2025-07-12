#include <QApplication>
#include <QClipboard>
#include <QPushButton>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QWidget>

#include "big_random.hpp"

using boost::multiprecision::cpp_int;

// -----------------------------------------------------------------------------
// Minimal Qt interface to generate and copy a 2084-bit number.
// It also stores the last 27 numbers in a 3x3x3 array.
// -----------------------------------------------------------------------------
int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QWidget window;                 // Main window widget
    QVBoxLayout layout(&window);    // Vertical stack layout

    QTextEdit display;              // Text box to show the number
    display.setReadOnly(true);

    QPushButton generateBtn("Generate");
    QPushButton copyBtn("Copy");

    layout.addWidget(&display);
    layout.addWidget(&generateBtn);
    layout.addWidget(&copyBtn);

    // ------------------------------------------------------------------
    // History buffer: stores 27 numbers (3x3x3). We manipulate it via a
    // pointer to demonstrate array pointer usage.
    // ------------------------------------------------------------------
    static cpp_int history[3][3][3];
    static int historyIndex = 0;          // Tracks next slot (0..26)
    cpp_int *historyPtr = &history[0][0][0];

    QObject::connect(&generateBtn, &QPushButton::clicked, [&]() {
        // Generate a new big number and display it
        cpp_int number = generateRandom2084Bit();
        display.setPlainText(QString::fromStdString(number.str()));

        // Store in history via the pointer
        historyPtr[historyIndex] = number;
        historyIndex = (historyIndex + 1) % 27;
    });

    QObject::connect(&copyBtn, &QPushButton::clicked, [&]() {
        // Copy current text to the clipboard
        QClipboard *clip = QApplication::clipboard();
        clip->setText(display.toPlainText());
    });

    window.setWindowTitle("2084-bit Random Generator");
    window.show();

    return app.exec();
}
