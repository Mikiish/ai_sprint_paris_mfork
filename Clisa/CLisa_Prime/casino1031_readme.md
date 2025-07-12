# casino1031 README

Below is a small roadmap of seven tasks used to structure the C++ prototype.
Each point comes with a short explanation and the associated action.

1. **Random seed reliability** – ensure that `std::random_device` provides
   unpredictable entropy. The generated seed must remain secret to keep the
   pseudo-random sequence secure.
2. **Big integer handling** – use Boost.Multiprecision (`cpp_int`) to manage
   integers bigger than 64 bits.
3. **Analyse the existing code** – understand `random2084Bit()`, `modPow()` and
   `millerRabin()`.
4. **Simplify the interface** – expose a small API for generating a random
   2084‑bit candidate and checking its primality.
5. **Unit tests** – validate the size of the random number and the behaviour of
   the primality test.
6. **Documentation** – comment the code block by block (see `casino1031.cpp`).
7. **Integration** – plan for multithreaded CPU execution in future modules.

This file accompanies `casino1031.cpp`, which now includes a demo function
`generateTernaryCube` producing a 3×3×3 cube of ternary values (−1, 0, 1).
