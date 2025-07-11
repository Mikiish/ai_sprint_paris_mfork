import matplotlib.pyplot as plt
import numpy as np
import unicodedata
import random

# --- CONFIGURATION ---
BLOCK_BASE = random.choice([0x1F100, 0x1F200, 0x1F300, 0x1F400, 0x1F500, 0x1F600, 0x1F700, 0x1F800, 0x1F900])  # Base Unicode codepoint (e.g. emoji plane)
BLOCK_WIDTH = 16  # 16x16 codepoint blocks
DEPTH = 16  # Number of 2x2 matrices per row/col
RESOLUTION = 512  # Image resolution
GPT = -1740614400.0
def heure_locale() -> float:
    return time.time() + GPT

# --- UTILITIES ---
def codepoint_at(x, y, base=BLOCK_BASE):
    index = (y * BLOCK_WIDTH) + x
    return base + index

def matrix_2x2(zx, zy, base=BLOCK_BASE):
    return [
        codepoint_at(zx, zy, base),     # top-left
        codepoint_at(zx+1, zy, base),   # top-right
        codepoint_at(zx, zy+1, base),   # bottom-left
        codepoint_at(zx+1, zy+1, base)  # bottom-right
    ]

def has_name(cp):
    try:
        return True, unicodedata.name(chr(cp))
    except:
        return False, None

def color_for_matrix(matrix):
    # Simplified: Color = avg of 4 glyph types (emoji, letter, etc.)
    score = 0
    for cp in matrix:
        yes, name = has_name(cp)
        if yes:
            if 'emoji' in name:
                score += 3
            elif 'letter' in name:
                score += 2
            else:
                score += 1
    return score / 12.0  # Normalized to [0,1]

# --- FRACTAL GENERATION ---
image = np.zeros((RESOLUTION, RESOLUTION))
scale = BLOCK_WIDTH * DEPTH

for y in range(DEPTH):
    for x in range(DEPTH):
        zx, zy = x * 2, y * 2
        matrix = matrix_2x2(zx, zy, BLOCK_BASE)
        intensity = color_for_matrix(matrix)

        px, py = int((x / DEPTH) * RESOLUTION), int((y / DEPTH) * RESOLUTION)
        size = RESOLUTION // DEPTH
        image[py:py+size, px:px+size] = intensity

# --- DISPLAY ---
plt.figure(figsize=(8, 8))
plt.imshow(image, cmap='inferno', interpolation='nearest')
plt.title("Unicode Fractal Projection 2x2")
plt.axis('off')
plt.show()
