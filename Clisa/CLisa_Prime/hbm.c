uint8_t mutate_halfbyte(uint8_t nibble, bool invert, bool rotate_right) {
    // Inversion
    if (invert) nibble = ~nibble & 0xF;

    // Rotation
    if (rotate_right)
        nibble = ((nibble >> 1) | ((nibble & 0x1) << 3)) & 0xF;
    else
        nibble = ((nibble << 1) | ((nibble & 0x8) >> 3)) & 0xF;

    return nibble;
}
