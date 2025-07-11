import re
import unicodedata
from Lisa_Tokenizer import bijective_tokenize


class LisaCompressor:
    def __init__(self, text):
        self.text = text
        self.compression_steps = []
        self.current_text = text

    def reduce_text(self):
        """Réduit progressivement le texte en supprimant les détails secondaires."""
        self.current_text = re.sub(r'\b(the|a|an|is|was|were|of|in|on|at|by)\b', '', self.current_text)
        self.current_text = re.sub(r'\s+', ' ', self.current_text).strip()
        self.compression_steps.append(self.current_text)

    def condense_text(self):
        """Condense les phrases en raccourcissant chaque mot à un maximum de 5 lettres sauf les noms propres."""
        words = self.current_text.split()
        truncated_words = [word if word.istitle() else word[:5] for word in words]  # Ne tronque pas les noms propres
        self.current_text = ' '.join(truncated_words)
        self.compression_steps.append(self.current_text)

    def introduce_symbols(self):
        """Remplace toute sous-chaîne clé par des emojis, peu importe sa position dans le mot."""
        symbol_map = {
            'presi': '👔', 'war': '⚔️', 'ukrai': '🇺🇦', 'comed': '🎭',
            'scien': '🔬', 'resea': '📖', 'histo': '📜', 'polit': '🏛️'
        }
        for word, symbol in symbol_map.items():
            self.current_text = re.sub(fr'{word}', symbol, self.current_text)
        self.compression_steps.append(self.current_text)

    def merge_symbols(self):
        """Transforme la chaîne en tokens bijectifs et conserve leur structure avec la taille."""
        tokenized = bijective_tokenize(self.current_text)
        self.current_text = ' - '.join([f'[{token["word"]}]({token["size"]})' for token in tokenized])
        self.compression_steps.append(self.current_text)

    def to_unicode_hex(self):
        """Convertit les tokens en Unicode Hexadécimal en conservant leur structure."""
        self.current_text = re.sub(r'\[(.*?)\]\((\d+)\)',
                                   lambda m: f'[{"".join(f"\\u{ord(c):04X}" for c in m.group(1))}]({m.group(2)})',
                                   self.current_text)
        self.compression_steps.append(self.current_text)

    def to_hexadecimal(self):
        """Convertit la représentation Unicode en Hexadécimal tout en conservant la structure."""
        self.current_text = re.sub(r'\[(.*?)\]\((\d+)\)',
                                   lambda m: f'[{m.group(1).encode("utf-8").hex().upper()}]({m.group(2)})',
                                   self.current_text)
        self.compression_steps.append(self.current_text)

    def to_base4(self):
        """Convertit chaque élément de la structure hexadécimale en base 4 tout en conservant la structure."""

        def hex_to_base4(hex_str):
            num = int(hex_str, 16)
            base4_repr = ''
            while num:
                base4_repr = str(num % 4) + base4_repr
                num //= 4
            return base4_repr if base4_repr else '3'

        self.current_text = re.sub(r'\[(.*?)\]\((\d+)\)',
                                   lambda m: f'[{hex_to_base4(m.group(1))}]({m.group(2)})',
                                   self.current_text)
        self.compression_steps.append(self.current_text)

    def concat_base4(self):
        """Concatène les tokens en base 4 en insérant un séparateur spécifique."""
        separator = f'{format(ord(" "), "b")}61681'
        tokens = re.findall(r'\[(.*?)\]\((\d+)\)', self.current_text)
        self.current_text = separator.join(f"{token[0]}{token[1]}" for token in tokens)
        self.compression_steps.append(self.current_text)

    def compress(self):
        """Applique les différentes étapes de compression."""
        self.reduce_text()
        self.condense_text()
        self.introduce_symbols()
        self.merge_symbols()
        self.to_unicode_hex()
        self.to_hexadecimal()
        self.to_base4()
        self.concat_base4()
        return self.compression_steps


# Exemple d'utilisation
text = "Volodymyr Zelenskyy, former comedian, became Ukraine's president in 2019 and led during the 2022 war."
compressor = LisaCompressor(text)
steps = compressor.compress()

for i, step in enumerate(steps, 1):
    print(f"Étape {i}: {step}")
