# Ternary Tensor Example

This mini-program demonstrates how to represent a 3&times;3&times;3 tensor of ternary values and encode it as a large integer. It also serves as a playground for Boost.Multiprecision.

## 7 stray thoughts (and matching tasks)

1. **Pick a multiprecision library wisely.**  
   *Task:* Here we use `boost::multiprecision::cpp_int` because it's header-only and easy to drop in.
2. **Keep tensors small but conceptually expandable.**  
   *Task:* Implement `TernaryTensor` as an array, so swapping in a bigger shape later is trivial.
3. **Randomness matters.**  
   *Task:* Seed an `std::mt19937` with `std::random_device` for repeatable runs that still look random.
4. **Conversion logic reveals structure.**  
   *Task:* Provide `tensorToBigInt` to show how base‑3 digits map to a giant integer.
5. **Readable output beats raw data.**  
   *Task:* `printTensor` formats the tensor layer by layer—no more peering at hex dumps.
6. **Short example, long reach.**  
   *Task:* Put everything in one file so it compiles anywhere without a build system.
7. **Leave room for sarcasm.**  
   *Task:* End with a note reminding the reader that bigger projects await.

## Code walkthrough

- **`struct TernaryTensor`** – stores 27 integers and provides `(x,y,z)` indexing.
- **`randomTensor()`** – fills a tensor with random values in {-1,0,1}.
- **`tensorToBigInt()`** – encodes the tensor in base&nbsp;3 using Boost.Multiprecision.
- **`printTensor()`** – prints each 3&times;3 layer for clarity.
- **`main()`** – glues everything together and dumps the final integer.

## Libraries

- `<array>` and `<random>` from the STL
- `<boost/multiprecision/cpp_int.hpp>` for arbitrary-size integers

## Building

```bash
g++ -std=c++17 ternary_tensor.cpp -o ternary_tensor
./ternary_tensor
```

No special linker flags are required because `cpp_int` is header-only.

## Final note

Good luck scaling this up to something useful—you might need it.
