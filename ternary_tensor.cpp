#include <array>
#include <random>
#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>

using boost::multiprecision::cpp_int;

// -----------------------------------------------------------------------------
// Simple structure representing a 3x3x3 tensor with ternary values {-1, 0, 1}.
// The tensor is stored as a flat std::array for simplicity.
// -----------------------------------------------------------------------------
struct TernaryTensor {
    std::array<int, 27> data{};  // 3*3*3 = 27 elements

    // Access element at position (x, y, z).
    int& operator()(int x, int y, int z) {
        return data[x * 9 + y * 3 + z];
    }

    // Const access for read-only operations.
    int operator()(int x, int y, int z) const {
        return data[x * 9 + y * 3 + z];
    }
};

// -----------------------------------------------------------------------------
// Generate a tensor filled with random {-1, 0, 1} values.
// Uses std::random_device and std::mt19937 for repeatable randomness.
// -----------------------------------------------------------------------------
TernaryTensor randomTensor() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(-1, 1);

    TernaryTensor t;
    for (int i = 0; i < 27; ++i) {
        t.data[i] = dist(gen);
    }
    return t;
}

// -----------------------------------------------------------------------------
// Convert the tensor into a big integer using base-3 encoding.
// This demonstrates how Boost.Multiprecision handles integers larger than 64 bits.
// -----------------------------------------------------------------------------
cpp_int tensorToBigInt(const TernaryTensor& t) {
    cpp_int result = 0;
    for (int i = 0; i < 27; ++i) {
        result *= 3;                     // Shift to next ternary digit
        result += t.data[i] + 1;         // Map {-1,0,1} -> {0,1,2}
    }
    return result;
}

// -----------------------------------------------------------------------------
// Pretty-print the tensor layer by layer.
// -----------------------------------------------------------------------------
void printTensor(const TernaryTensor& t) {
    for (int x = 0; x < 3; ++x) {
        std::cout << "Layer " << x << ":\n";
        for (int y = 0; y < 3; ++y) {
            for (int z = 0; z < 3; ++z) {
                std::cout << t(x, y, z) << ' ';
            }
            std::cout << '\n';
        }
        std::cout << '\n';
    }
}

// -----------------------------------------------------------------------------
// Entry point: generate a random tensor, display it and its integer encoding.
// -----------------------------------------------------------------------------
int main() {
    TernaryTensor t = randomTensor();
    std::cout << "Random 3x3x3 ternary tensor:" << std::endl;
    printTensor(t);

    cpp_int value = tensorToBigInt(t);
    std::cout << "Base-3 encoded as big integer:" << std::endl;
    std::cout << value << std::endl;

    return 0;
}

