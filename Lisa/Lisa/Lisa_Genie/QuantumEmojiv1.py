import random
import unicodedata
import time
import regex

INTERVALS = [
    (0x1F600, 0x1F64F),  # 1F600–1F64F : Emoticons (Smileys & People, ex. 😀 😃 😄)
    (0x1F300, 0x1F5FF),  # 1F300–1F5FF : Miscellaneous Symbols And Pictographs (inclut météo, plantes, animaux, etc.)
    (0x1F680, 0x1F6FF),  # 1F680–1F6FF : Transport And Map Symbols (ex. 🚀 🚁 🚂)
    (0x1F700, 0x1F77F),  # 1F700–1F77F : Alchemical Symbols
    (0x1F780, 0x1F7FF),  # 1F780–1F7FF : Geometric Shapes Extended
    (0x1F800, 0x1F8FF),  # 1F800–1F8FF : Supplemental Arrows-C (et symboles associés)
    (0x1F900, 0x1F9FF),  # 1F900–1F9FF : Supplemental Symbols and Pictographs (ex. 🤩 🥰 🤓)
    (0x1FA00, 0x1FA6F),  # 1FA00–1FA6F : Symbols And Pictographs Extended-A (certains nouveaux emojis, symboles d'échecs, etc.)
    (0x1FA70, 0x1FAFF),  # 1FA70–1FAFF : Symboles additionnels variés (objets culturels, outils, vêtements)
    (0x2700, 0x27BF),    # 2700–27BF : Dingbats (ex. ✂ ✈ ✉, ✂️)
    (0x2B50, 0x2B59),    # 2B50–2B59 : Petite plage incluse dans "Misc. Symbols and Arrows" (ex. ⭐, 🌟, etc.)
    (0x2600, 0x26FF),    # 2600–26FF : Miscellaneous Symbols, Astrologiques, Météorologiques. (ex. ☀ ☁ ☂, ☀️☁️☂️)
    (0x2100, 0x214F),    # 2100–214F : Letterlike Symbols (℀, ©, ®, ℉, ℗, ℞, ℹ️, etc.)
    (0x2150, 0x218F),    # 2150–218F : Number Forms (ex. ⅓, ⅕, ⅖, ⅗, ↀ)
    (0x2190, 0x21FF),    # 2190–21FF : Arrows (←, ↑, ↓, →, ↔, ↕, etc.)
    (0x2200, 0x22FF),    # 2200–22FF : Mathematical Operators (∀, ∂, ∃, ∑, √, ≈, ∫, etc.)
    (0x2300, 0x23FF),    # 2300–23FF : Miscellaneous Technical (⌂, ⌛, ⏰, ⌚, ⎈, etc.)
    (0x25A0, 0x25FF),    # 25A0–25FF : Geometric Shapes (■, □, ●, ◉, ▲, ▽, etc.)
    (0x27C0, 0x27EF),    # 27C0–27EF : Misc. Mathematical Symbols-A (⟀, ⟁, ⟂, etc.)
    (0x2980, 0x29FF),    # 2980–29FF : Misc. Mathematical Symbols-B (⦀, ⦁, ⦂, etc.)
    (0x2A00, 0x2AFF),    # 2A00–2AFF : Opérateurs mathématiques étendus et spécialisés (⨁, ⨂, ⨃)
]

# Patterns : version 3 emojis (entre guillemets triples pour lisibilité)
PATTERNS_3 = [
    "\\u{XXXXX:04X}\\uFE0F\\u26XX\\u{YYYYY:04X}\\u200D\\u{SSSSS:04X}\\uFE0F\\u26XX",
    "\\u{XXXXX:04X}\\uFE0E\\u26XX\\u{YYYYY:04X}\\u200D\\u{SSSSS:04X}\\uFE0F\\u26XX",
    "\\u{XXXXX:04X}\\uFE0F\\u26XX\\u{YYYYY:04X}\\u200D\\u{SSSSS:04X}\\uFE0E\\u26XX",
    "\\u{XXXXX:04X}\\uFE0E\\u26XX\\u{YYYYY:04X}\\u200D\\u{SSSSS:04X}\\uFE0E\\u26XX",
    "\\u{XXXXX:04X}\\u26XX\\u{YYYYY:04X}\\u200D\\u{SSSSS:04X}\\u26XX\\uFE0F",
    "\\u{XXXXX:04X}\\u26XX\\u{YYYYY:04X}\\u200D\\u{SSSSS:04X}\\u{TTTTT:04X}\\u26XX",
    "\\u{XXXXX:04X}\\u{YYYYY:04X}\\u200D\\u{SSSSS:04X}\\u{TTTTT:04X}",
]

# Patterns : version 2 emojis
PATTERNS_2 = [
    "\\u{XXXXX:04X}\\uFE0F\\u26XX\\u200D\\u{YYYYY:04X}\\uFE0F\\u26XX",
    "\\u{XXXXX:04X}\\uFE0E\\u26XX\\u200D\\u{YYYYY:04X}\\uFE0F\\u26XX",
    "\\u{XXXXX:04X}\\uFE0F\\u26XX\\u200D\\u{YYYYY:04X}\\uFE0E\\u26XX",
    "\\u{XXXXX:04X}\\uFE0E\\u26XX\\u200D\\u{YYYYY:04X}\\uFE0E\\u26XX",
    "\\u{XXXXX:04X}\\u200D\\u26XX\\u{YYYYY:04X}\\u26XX\\uFE0F",
    "\\u{XXXXX:04X}\\u200D\\u26XX\\u{YYYYY:04X}\\u26XX",
    "\\u{XXXXX:04X}\\u200D\\u{YYYYY:04X}",
]

ALL_PATTERNS = PATTERNS_3 + PATTERNS_2


def is_printable_noncontrol(s: str) -> bool:
    ###
    ### Vérifie que TOUTES les unités de s sont imprimables (pas un espace vide,
    ### pas un contrôle, etc.).
    ###
    # S'il n'y a rien, on considère que ce n'est pas "visible"
    if not s:
        return False
    # Vérifie chaque codepoint de la chaîne
    for ch in s:
        if not ch.isprintable():
            return False
        if ch.strip() == "":
            # ch est probablement un espace, tab, etc.
            return False
        cat = unicodedata.category(ch)
        # Exclure par exemple Cc (contrôle), Zl, Zp, etc.
        # (Mn = Nonspacing Mark : parfois on veut l'exclure, parfois non,
        #  dépend de ce qu'on veut considérer comme "visibles".)
        if cat in ['Cc', 'Zl', 'Zp']:
            return False
    return True


def is_single_grapheme_different(base_char: str, combined: str) -> bool:
    ###
    ### Vérifie si 'combined' forme EXACTEMENT UNE seule grappe \X (via la lib 'regex'),
    ### et si cette grappe est différente de 'base_char' (ne serait-ce qu'un Variation Selector).
    ###
    # On segmente 'combined' en grappes
    graphemes = list(regex.finditer(r"\X", combined))
    # S'il n'y a qu'une grappe
    if len(graphemes) == 1:
        the_cluster = graphemes[0].group()
        # Vérifie que la grappe n'est pas identique au base_char seul
        return the_cluster != base_char
    return False


def generate_possible_states_for(cp_x: int, intervals) -> list[str]:
    base_char = chr(cp_x)
    possible_states = []

    for (start, end) in intervals:
        for cp_y in range(start, end + 1):
            char_y = chr(cp_y)
            combo = base_char + char_y

            # On vérifie la visibilité/imprimabilité de la chaîne au global
            if is_printable_noncontrol(combo):
                # Vérifie qu'il s'agisse d'un SEUL glyphe, différent de base_char
                if is_single_grapheme_different(base_char, combo):
                    possible_states.append(combo)

    if not possible_states:
        # Fallback : on ajoute le base_char seul (aucune variation trouvée)
        possible_states.append(base_char)

    return possible_states


class QuantumEmoji:
    def __init__(self, intervals):
        self.map_cp_to_states = {}

        # Pour chaque cp dans les intervals
        for (start, end) in intervals:
            for cp in range(start, end + 1):
                char_x = chr(cp)
                # On teste d'abord si X (seul) est visible
                if is_printable_noncontrol(char_x):
                    states = generate_possible_states_for(cp, intervals)
                    self.map_cp_to_states[cp] = states

        self.all_keys = list(self.map_cp_to_states.keys())

    def measure_emoji(self) -> str:
        if not self.all_keys:
            return "No available emojis."
        cp_x = random.choice(self.all_keys)
        states = self.map_cp_to_states[cp_x]
        return random.choice(states)


class QuantumEmojiLock:
    def __init__(self, quantum_emoji: QuantumEmoji, cp_x: int = None):
        self.qe = quantum_emoji
        if cp_x is None:
            cp_x = random.choice(self.qe.all_keys)
        self.cp_x = cp_x

        self.states = self.qe.map_cp_to_states.get(cp_x, [])
        if self.states:
            self.locked_state = random.choice(self.states)
        else:
            # fallback
            self.locked_state = chr(cp_x)

    def get_locked_state(self) -> str:
        return self.locked_state


if __name__ == "__main__":
    ## Temps c moi cc#
    time_avant = time.time()
    print(f"Time now : {time_avant}")
    ### Oui!
    Quantum_Emoji = QuantumEmoji(INTERVALS)

    ## Temps c moi cc#
    time_apresinit = time.time()
    print(f"Time now : {time.time()}\nTemps d'init : {time_apresinit - time_avant}")
    ### Oui!
    for _ in range(5):
        print("Mesure aléatoire :", Quantum_Emoji.measure_emoji())

    ## Temps c moi cc#
    time_apresboucle = time.time()
    print(f"Time Now : {time.time()}\nTemps ecoule : {time_apresboucle - time_avant}\nTemps d'boucle : {time_apresboucle - time_apresinit}")
    ### Oui!
    qlock = QuantumEmojiLock(Quantum_Emoji)

    ## Temps c moi cc#
    time_apreslock = time.time()
    print(f"Time Now : {time.time()}\nTemps ecoule : {time_apreslock - time_avant}\nTemps d'lock : {time_apreslock - time_apresboucle}")
    print("Lock random:", qlock.get_locked_state())
    # Exemple : U+1F468 (👨)
    ### Oui!
    qlock_h = QuantumEmojiLock(Quantum_Emoji, cp_x=0x1F468)
    print("Lock on U+1F468:", qlock_h.get_locked_state())

    ## Temps c moi cc#
    time_finish = time.time()
    print(f"Time now : {time.time()}\nTemps ecoule : {time_finish - time_avant}")
