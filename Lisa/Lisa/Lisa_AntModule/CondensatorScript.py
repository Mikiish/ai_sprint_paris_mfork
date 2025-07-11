import re
import numpy as np
import math


def detect_python_code(message):
    """Détecte si un message contient probablement du code Python."""
    code_patterns = [r"\bclass\b", r"\bdef\b", r"import ", r"return ", r"if __name__ =="]
    special_chars = ["\\", "\n", "_", "(", ")"]

    char_density = sum(message.count(c) for c in special_chars) / max(len(message), 1)
    keyword_density = sum(bool(re.search(pattern, message)) for pattern in code_patterns)

    return char_density > 0.05 or keyword_density > 2  # Seuil empirique


def segment_text_into_acts(lines):
    """Segmente les 20,000 lignes en 3 blocs temporels."""
    total_lines = len(lines)
    split_1 = total_lines // 3
    split_2 = 2 * total_lines // 3

    return lines[:split_1], lines[split_1:split_2], lines[split_2:]


def exponential_segmenter(lines, max_block_size=7):
    """Segmente le texte en blocs selon une courbe exponentielle (1 - exp(-t))."""
    segmented = []
    i = 0

    while i < len(lines):
        block_size = min(max_block_size, int(1 + np.log(1 + i)))  # Courbe log
        segmented.append("\n".join(lines[i:i + block_size]))
        i += block_size

    return segmented


def exponential_condensation(text_lines):
    """ Applique une réduction exponentielle sur les blocs de texte. """
    total_lines = len(text_lines)

    # Définition des blocs
    block1 = text_lines[:7000]  # Récent
    block2 = text_lines[7000:15000]  # Moyen
    block3 = text_lines[15000:]  # Ancien

    def apply_condensation(block, factor):
        """ Condense un bloc de texte selon un facteur spécifique. """
        reduced_size = int(len(block) * factor)
        indices = sorted(math.floor(i * len(block) / reduced_size) for i in range(reduced_size))
        return [block[i] for i in indices]

    # Appliquer la condensation progressive
    block1_condensed = apply_condensation(block1, 0.67)  # Réduction douce
    block2_condensed = apply_condensation(block2, 0.45)  # Réduction moyenne
    block3_condensed = apply_condensation(block3, math.log2(len(block3)) / len(block3))  # Réduction extrême

    # Fusion des blocs
    condensed_text = block1_condensed + block2_condensed + block3_condensed

    return condensed_text

def preprocess_text(file_path):
    """Charge et traite le texte brut en appliquant la segmentation et le filtrage."""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # Filtrer le code Python
    cleaned_lines = ["[Interpretating Python Env]" if detect_python_code(line) else line.strip() for line in raw_lines]

    # Segmenter en 3 actes
    act1, act2, act3 = segment_text_into_acts(cleaned_lines)

    # Appliquer la condensation exponentielle
    condensed_act1 = exponential_segmenter(act1)
    condensed_act2 = exponential_segmenter(act2)
    condensed_act3 = exponential_segmenter(act3)

    # Fusionner et retourner
    return condensed_act1 + condensed_act2 + condensed_act3


if __name__ == "__main__":
    processed_text = preprocess_text("conversation_raw.txt")
    with open("conversation_condensed.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(processed_text))
    print("✅ Texte condensé et filtré enregistré dans conversation_condensed.txt !")
