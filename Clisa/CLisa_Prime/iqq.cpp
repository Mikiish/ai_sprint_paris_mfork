#include <cstdint>
#include <cstddef>
#include <algorithm>
#ifdef _OPENMP
#include <omp.h>
#endif

// --- quantize_fp128_to_u8 ---------------------------------
// Convert an array of 128-bit floats (long double) to 8-bit integers.
// Steps:
//  1. Cast each long double to float.
//  2. Multiply by a scaling factor.
//  3. Clamp to [0, 255] and store as uint8_t.
// The pragma hints the compiler to vectorize the loop.
void quantize_fp128_to_u8(const long double* __restrict input,
                          uint8_t* __restrict output,
                          std::size_t n,
                          float scale)
{
    #pragma omp simd
    for(std::size_t i = 0; i < n; ++i) {
        float fp32 = static_cast<float>(input[i]);
        int q = static_cast<int>(fp32 * scale + 0.5f);
        q = std::clamp(q, 0, 255);
        output[i] = static_cast<uint8_t>(q);
    }
}

// --- main --------------------------------------------------
// Tiny demo that feeds random values to the quantization
// routine and prints the resulting bytes. Purely illustrative
// for benchmarking on a rainy Monday morning.
#ifdef TEST_QUANTIZE_MAIN
#include <iostream>
#include <vector>
#include <random>

int main() {
    const std::size_t N = 16;
    std::vector<long double> src(N);
    std::vector<uint8_t> dst(N);
    std::mt19937_64 rng(1234);
    std::uniform_real_distribution<long double> dist(0.0, 1.0);
    for (std::size_t i = 0; i < N; ++i)
        src[i] = dist(rng);

    quantize_fp128_to_u8(src.data(), dst.data(), N, 255.0f);

    for (std::size_t i = 0; i < N; ++i)
        std::cout << static_cast<int>(dst[i]) << ' ';
    std::cout << '\n';
    return 0;
}
#endif
