#ifndef BIG_RANDOM_HPP
#define BIG_RANDOM_HPP

#include <boost/multiprecision/cpp_int.hpp>
#include <random>

// This header exposes a helper function to generate a large
// 2084-bit random integer. It is meant to be reused by any
// module that needs such numbers.

using boost::multiprecision::cpp_int;

// -----------------------------------------------------------------------------
// generateRandom2084Bit
//   Builds a 2084-bit integer using std::random_device for seeding and
//   std::mt19937_64 for the actual PRNG. The highest bit is set to guarantee
//   the exact size.
// -----------------------------------------------------------------------------
inline cpp_int generateRandom2084Bit() {
    std::random_device rd;          // Non-deterministic seed
    std::mt19937_64 gen(rd());      // 64-bit Mersenne Twister engine
    cpp_int result = 0;

    // Produce the number in 64-bit chunks
    for (int produced = 0; produced < 2084; produced += 64) {
        result <<= 64;              // Make room for next chunk
        result |= static_cast<uint64_t>(gen());
    }

    // Ensure the number is exactly 2084 bits
    result |= cpp_int(1) << 2083;
    return result;
}

#endif // BIG_RANDOM_HPP
