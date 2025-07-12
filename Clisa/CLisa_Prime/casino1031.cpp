#include <boost/multiprecision/cpp_int.hpp>
#include <random>
#include <iostream>
#include <array>

// Utility using directive for the big integer type.
using boost::multiprecision::cpp_int;

// Forward declarations for the main helpers.
bool millerRabin(const cpp_int &n, int iterations = 25);
cpp_int modPow(cpp_int base, cpp_int exp, const cpp_int &mod);
cpp_int random2084Bit();

// Helper structures for the ternary 3x3x3 cube example.
struct TernaryCube {
    bool* cells[3][3][3];  // nullptr means 0, otherwise true => 1, false => -1
};

TernaryCube generateTernaryCube(std::mt19937_64 &gen);
void freeTernaryCube(TernaryCube &cube);

// -----------------------------------------------------------------------------
// Entry point demonstrating the usage of the helpers above.
// -----------------------------------------------------------------------------
int main() {
    cpp_int candidate = random2084Bit();
    std::cout << "Random 2084-bit candidate:" << std::endl << candidate << std::endl;

    // Generate a demo ternary cube using the same RNG.
    std::mt19937_64 gen(std::random_device{}());
    TernaryCube cube = generateTernaryCube(gen);

    std::cout << "\nTernary cube values:" << std::endl;
    for (int x = 0; x < 3; ++x) {
        for (int y = 0; y < 3; ++y) {
            for (int z = 0; z < 3; ++z) {
                bool *ptr = cube.cells[x][y][z];
                int val = ptr ? (*ptr ? 1 : -1) : 0;
                std::cout << val << ' ';
            }
            std::cout << " | ";
        }
        std::cout << std::endl;
    }

    freeTernaryCube(cube);

    if (millerRabin(candidate)) {
        std::cout << "Candidate is probably prime." << std::endl;
    } else {
        std::cout << "Candidate is composite." << std::endl;
    }
    return 0;
}

// -----------------------------------------------------------------------------
// Generate a random 2084-bit integer.
// This mimics Python's os.urandom by using std::random_device as entropy source.
// -----------------------------------------------------------------------------
cpp_int random2084Bit() {
    // Use hardware entropy if available. Keeping the seed secret makes the
    // pseudo-random sequence unpredictable, which is desirable for crypto.
    std::random_device rd;              // Non-deterministic seed source.
    std::mt19937_64 gen(rd());          // 64-bit Mersenne Twister engine.
    cpp_int result = 0;
    int bits = 2084;

    // Build the number in 64-bit blocks. Each chunk can be reused as a
    // building block for other structures (e.g. 3x3x3 cubes).
    for (int produced = 0; produced < bits; produced += 64) {
        result <<= 64;                  // Make room for the next chunk.
        result |= static_cast<uint64_t>(gen());
    }

    // Ensure the highest bit is set so the number is exactly 2084 bits.
    result |= cpp_int(1) << (bits - 1);
    return result;
}

// -----------------------------------------------------------------------------
// Modular exponentiation (base^exp mod mod).
// Works for big integers thanks to Boost.Multiprecision.
// -----------------------------------------------------------------------------
cpp_int modPow(cpp_int base, cpp_int exp, const cpp_int &mod) {
    cpp_int result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1)
            result = (result * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return result;
}

// -----------------------------------------------------------------------------
// Miller-Rabin primality test for big integers.
// Returns true if n is probably prime.
// -----------------------------------------------------------------------------
bool millerRabin(const cpp_int &n, int iterations) {
    if (n < 2)
        return false;
    if (n == 2 || n == 3)
        return true;
    if (n % 2 == 0)
        return false;

    // Write n-1 as 2^r * d with d odd.
    cpp_int d = n - 1;
    unsigned int r = 0;
    while ((d & 1) == 0) {
        d >>= 1;
        ++r;
    }

    std::mt19937_64 gen(std::random_device{}());
    std::uniform_int_distribution<uint64_t> dist(2, std::numeric_limits<uint64_t>::max());

    for (int i = 0; i < iterations; ++i) {
        // Generate a random base a in [2, n-2]. We construct it from 64-bit parts.
        cpp_int a = 2 + (cpp_int(dist(gen)) % (n - 3));
        cpp_int x = modPow(a, d, n);
        if (x == 1 || x == n - 1)
            continue;

        bool witness = true;
        for (unsigned int j = 1; j < r; ++j) {
            x = modPow(x, 2, n);
            if (x == n - 1) {
                witness = false;
                break;
            }
        }
        if (witness)
            return false;               // Composite number.
    }
    return true;                        // Probably prime.
}

// -----------------------------------------------------------------------------
// Create a 3x3x3 cube where each cell is a pointer to bool.
// nullptr -> 0, true -> 1, false -> -1.
// -----------------------------------------------------------------------------
TernaryCube generateTernaryCube(std::mt19937_64 &gen) {
    std::uniform_int_distribution<int> dist(0, 2); // 0:nil, 1:true, 2:false
    TernaryCube cube{};
    for (int x = 0; x < 3; ++x)
        for (int y = 0; y < 3; ++y)
            for (int z = 0; z < 3; ++z) {
                int sel = dist(gen);
                if (sel == 0) {
                    cube.cells[x][y][z] = nullptr;
                } else {
                    cube.cells[x][y][z] = new bool(sel == 1);
                }
            }
    return cube;
}

// Release the dynamically allocated booleans within the cube.
void freeTernaryCube(TernaryCube &cube) {
    for (int x = 0; x < 3; ++x)
        for (int y = 0; y < 3; ++y)
            for (int z = 0; z < 3; ++z)
                delete cube.cells[x][y][z];
}
