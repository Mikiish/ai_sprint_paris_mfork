import typing, random, math, sympy, unicodedata, regex, json, time, os, re
import sympy.plotting, sympy.combinatorics, sympy.polys
from typing import Any, Union
from sympy import Symbol, Rational, I
import QUnicode as quc
import numpy as np

###    
###    
# — Intervalles de ton code, commentés :
BEAUCOUP = 0.00001
TRESGRAND_NOMBRE = 61681
PTI_NOMBRE = 7
GPT = -1740614400.0
def heure_locale() -> float:
    return time.time() + GPT
INTERVALS = [
    (0x1F300, 0x1F5FF),  # Misc Symbols & Pictographs
    (0x1F600, 0x1F67F),  # Emoticons (Smileys)
    (0x1F680, 0x1F6FF),  # Transport & Map
    (0x1F700, 0x1F77F),  # Alchemical
    (0x1F780, 0x1F7FF),  # Geometric Shapes Extended
    (0x1F800, 0x1F8FF),  # Supplemental Arrows-C
    (0x1F900, 0x1F9FF),  # Supplemental Symbols & Pictographs
    (0x1FA00, 0x1FA6F),  # Symbols & Pictographs Extended-A
    (0x1FA70, 0x1FAFF),  # Autres extensions d’emojis
    (0x20D0, 0x20F0),  # Combining Diacritical Marks for Symbols block
    (0x2100, 0x214F),  # Letterlike
    (0x2150, 0x218F),  # Number Forms
    (0x2190, 0x21FF),  # Arrows
    (0x2200, 0x22FF),  # Mathematical Operators
    (0x2300, 0x23FF),  # Misc. Technical
    (0x25A0, 0x25FF),  # Geometric Shapes
    (0x2600, 0x26FF),  # Genres
    (0x2700, 0x27BF),  # Dingbats
    (0x27C0, 0x27EF),  # Misc. Mathematical Symbols-A
    (0x27F0, 0x27FF),  # Supplemental Arrows-A block
    (0x2900, 0x297F),  # Supplemental Arrows-B block
    (0x2980, 0x29FF),  # Misc. Mathematical Symbols-B
    (0x2A00, 0x2AFF),  # Supplemental Mathematical Operators
    (0x2B00, 0x2BFF),  # Miscellaneous Symbols and Arrows block
]
##########################################
### 0x1F000 < Nous < 0x1FBFF
##########################################
INTERVALS_EMOJI = [
    (0x1F300, 0x1F5FF),
    (0x1F600, 0x1F64F),
    (0x1F680, 0x1F6FF),
    (0x1F7E0, 0x1F7F0),
    (0x1F900, 0x1F9FF),
    (0x1FA00, 0x1FA6F),
    (0x1FA70, 0x1FAF8)
]
INTERVALS_EMOJI_ADD = [
    (0x1F000, 0x1F1AD),
    (0x1F1E6, 0x1F265),
    (0x1F650, 0x1F67F),
    (0x1FB00, 0x1FBFF),
]
INTERVALS_VARIOUS = [
    (0x1F650, 0x1F67F),  # 🙿 🚀 🚁 <- 0xF1681
    (0x1F700, 0x1F7FF)
]
INTERVALS_ADD_ARROWS = [
    (0x1F800, 0x1F8C1)
]
INTERVALS_QRCODE = [
    (0x1FB00, 0x1FB3B), # QR-Code
    (0x1FB3C, 0x1FB8B), # Polygon.QR-Code
    (0x1FB8C, 0x1FBFF) # All.QR-Code
]
##########################################
### These are < 0xFFFF
##########################################
INTERVALS_MATH = [
    (0x20D0, 0x20F0),  # Combining Diacritical Marks for Symbols block
    (0x2100, 0x214F),  # Letterlike
    (0x2150, 0x218F),  # Number Forms
    (0x2190, 0x21FF),  # Arrows
    (0x2200, 0x22FF),  # Mathematical Operators
    (0x2300, 0x23FF),  # Misc. Technical
    (0x25A0, 0x25FF),  # Geometric Shapes
    (0x2600, 0x26FF),  # Genres
    (0x2700, 0x27BF),  # Dingbats
    (0x27C0, 0x27EF),  # Misc. Mathematical Symbols-A
    (0x27F0, 0x27FF),  # Supplemental Arrows-A block
    (0x2900, 0x297F),  # Supplemental Arrows-B block
    (0x2980, 0x29FF),  # Misc. Mathematical Symbols-B
    (0x2A00, 0x2AFF),  # Supplemental Mathematical Operators
    (0x2B00, 0x2BFF),  # Miscellaneous Symbols and Arrows block
]
INTERVALS_LETTERLIKE = [
    (0x2100, 0x214F),  # Letterlike
    (0x2150, 0x218F),  # Number Forms
]
INTERVALS_MATH_LOGIC = [
    (0x20D0, 0x20F0),  # Combining Diacritical Marks for Symbols block
    (0x2100, 0x214F),  # Letterlike
    (0x2150, 0x218F),  # Number Forms
    (0x2190, 0x21FF),  # Arrows
    (0x27F0, 0x27FF),  # Supplemental Arrows-A block
    (0x2900, 0x297F),  # Supplemental Arrows-B block
    (0x2B00, 0x2BFF)  # Miscellaneous Symbols and Arrows block
]
INTERVALS_MATH_OPERATORS = [
    (0x2100, 0x214F),  # Letterlike
    (0x2190, 0x21FF),  # Arrows
    (0x2200, 0x22FF),  # Mathematical Operators
    (0x2A00, 0x2AFF),  # Supplemental Mathematical Operators
]
INTERVALS_MATH_EXTRA = [
    (0x27C0, 0x27EF),  # Misc. Mathematical Symbols-A
    (0x2980, 0x29FF),  # Misc. Mathematical Symbols-B
    (0x2A00, 0x2AFF)  # Supplemental Mathematical Operators
]
INTERVALS_MATH_SYMBOLS = [
    (0x25A0, 0x25FF),  # Geometric Shapes
    (0x2700, 0x27BF),  # Dingbats
    (0x27C0, 0x27EF),  # Misc. Mathematical Symbols-A
    (0x2980, 0x29FF),  # Misc. Mathematical Symbols-B
    (0x2B50, 0x2B59),  # Misc. Symbols
]
INTERVALS_MATH_ARROWS = [
    (0x2190, 0x21FF),  # Extended Arrows
    (0x27F0, 0x27FF),
    (0x2900, 0x297F),
    (0x2B00, 0x2BFF),
]
INTERVALS_EARLY = [
    (0x0021, 0x007E),  # Init Letters
    (0x00A1, 0x0FFF),  # Latin & Arabic, Tibetan, Various...
    (0x1000, 0x1FFF),  # Myanmar, and many more xdd
    (0x2000, 0x200F),  # Start of Symbolic, Spaces.
    (0x2010, 0x205F),  # Punctuation, more Spaces.
    (0x2070, 0x209F),  # Subscripts. Just avoiding some Cc.
    (0x20A0, 0x20CF),  # Currency Symbols.
]
INTERVALS_EARLY_LETTERS = [
    (0x0021, 0x007E),  # Init Letters
    (0x00A1, 0x0FFF),  # Latin & Arabic, Tibetan, Various...
    (0x1000, 0x1FFF),  # Myanmar, and many more xdd
]
INTERVALS_EARLY_EXT = INTERVALS_EARLY + [
    (0x2C00, 0x2CFF),
]
INTERVALS_PICTOGRAMMES = [
    (0x2C00, 0x2CFF),  # Varied Latin, Greek, Cyrillic
    (0x2D00, 0x2DFF),  # Georgian, etc...
    (0x2E00, 0x2E7F),  # Various punctuation.
    (0x2E80, 0x4DBF),  # Unified CJK (Chinese, Japan, Korean) symbols and ideographs.
    (0x4DC0, 0x4DFF),  # Special mention for Hexagrams. There are 64.
    (0x4E00, 0x4E00),  # First.
    (0x4E01, 0x9FFF),  # Unified CJK remains.
    (0xA000, 0xA4CF),  # Yi.
    (0xA4D0, 0xA4FF),  # Lisa. Latin based with symetry. <BPrPDTrTGKrKJCrCZFrFMNLSRrRrVVHrGrJWXYrB-ArAErEIOUrUrLrD>
    (0xA500, 0xABBF),  # Various.
    (0xABC0, 0xABFF),  # Meetei ?
    (0xAC00, 0xD7FF),  # Hangul.
    (0xF900, 0xFAD9),  # Additionnal CJK symbols.
    (0xFB00, 0xFDFF),  # Various Arabic.
    (0xFE00, 0xFE0F),  # Junctions, Variations. These are non-spaces.
    (0xFE10, 0xFFEF),  # Vertical separators. Various letters (Arabic, Latin, CJK...), numbers and separators.
    (0xFFF0, 0xFFFF),  # Specials.
]
INTERVALS_PRIVATE = [
    (0xD800, 0xDB7F),  # High Surrogates.
    (0xDB80, 0xDBFF),  # Private.
    (0xDC00, 0xDFFF),  # Low Surrogates.
    (0xE000, 0xF8FF),  # Private Area. <-  se trouve ici.
]
##########################################
### 0x10000 < Nous < 0x1EFFF
##########################################
INTERVALS_VARIOUS_EARLY = [
    (0x10000, 0x1254F),  # Various.
    (0x12F90, 0x1345F),  # Giga Various. Hieroglyphs
    (0x14400, 0x14646),  # Some named Hieroglyphs.
    (0x16800, 0x16A38),  # Le fameux Bamum.
    (0x16A40, 0x16B8F),  # Divers... (Tangsa, Pahawh Hmong)
    (0x16E40, 0x16E9A),  # Divers... (Medefaidrin)
    (0x16F00, 0x16F9F),  # Divers... (Miao)
    (0x16FE0, 0x16FE4),  # ???
    (0x1B000, 0x1B001),  # C'est un gars une fille xdxd
    (0x1B170, 0x1B2FB),  # Divers... (Nushu)
    (0x1BC00, 0x1BC9F),  # Divers... (Duployan)
    (0x1CD00, 0x1CEAF),  # Divers... (Musical)
    (0x1D000, 0x1D3FF),  # Divers...
    (0x1D400, 0x1D7FF),  # Divers... (Bold letters, and various number/letters for LaTeX ?)
    (0x1DF00, 0x1DF1E),  # Divers... ("Extended Latin")
    (0x1E100, 0x1E14F),  # Divers... (Nyiakeng)
    (0x1E290, 0x1E2AE),  # Divers... (Toto)
    (0x1E2C0, 0x1E2FF),  # Divers... (Wancho)
    (0x1E4D0, 0x1E4F9),  # Divers... (Ethiopic)
    (0x1E7E0, 0x1E7FF),  # Divers... (Ethiopic Ext.)
    (0x1E800, 0x1E8D6),  # Divers... (Mende Kikakui)
    (0x1E900, 0x1E95F),  # Divers... (Adlam)
    (0x1EC71, 0x1ECB4),  # Divers... (Siyaq Numbers)
    (0x1ED00, 0x1ED3D),  # Divers... (Ottoman Siyaq Numbers)
]
INTERVALS_PRIVATE_EXT = [
    (0x13460, 0x143FF),  # Unamed Hieroglyphs.
    (0x14647, 0x167FF),  # Unamed Bamum.
    (0x16FE5, 0x16FFF),  # Unamed random.
    (0x17000, 0x187FF),  # Unamed Tangut.
    (0x18800, 0x18AFF),  # Tangut numéro 768.
    (0x18B00, 0x18CD5),  # Khitan numéro 18B00.
    (0x18CD6, 0x18CFE),  # Unamed Khitans.
    (0x18CFF, 0x18CFF),  # 18CFF lui-même !
    (0x18D00, 0x18D7F),  # More unamed Tanguts.
    (0x18D80, 0x1AFFF),  # Unamed Kanas.
    (0x1B002, 0x1B16F),  # More named Kanas.
    (0x1B300, 0x1BBFF),  # Unamed Duployan.
    (0x1BCB0, 0x1CBFF),  # Unamed Musical.
    (0x1CC00, 0x1CCF9),  # Musical.
    (0x1CD00, 0x1CEB3),  # Add Musical (QR-Code).
    (0x1ED50, 0x1EEFF),  # Unamed Arabic Maths.
    (0x1EF00, 0x1EFFF),  # Unamed Majong Tiles.
    ###
    ### 0x1F000 < 🀀🀀🀀 ENFIN HOURA GGWP.🀀🀀🀀
    ### 0x1F300 < 🀀🌀🌀
    ### 0x1F600 < 😀😀😀
    ### 0x1F680 < 🚀🚀🚀
    ### 0x1F681 < 🚁🚁🀀
]
##########################################
### 0x20000 < Nous
##########################################
INTERVALS_HIGHER = [
    (0x20000, 0x2EE5D),  # "Some" ...
    (0x2F80F, 0x2F9F4),  # "Various" ...
    (0x30000, 0x323AF),  # "Tags" ...
]
INTERVALS_END = [
    (0x323B0, 0x323FF),  # Nothing here.
    (0x32400, 0x32FFF),  # Nothing here neither.
    (0x33000, 0x3FFFF),  # Nothing here, I've checked.
    (0x40000, 0xFFFFF)   # Nothing but numbers. We have 0x61681 in there.
]
##########################################
### Et Nous, il peut tout regrouper :
##########################################
INTERVALS_EMOJI_CONCRET: list[tuple[int, int]]          = INTERVALS_EMOJI + INTERVALS_EMOJI_ADD
INTERVALS_ESYMBOLS_CONCRET: list[tuple[int, int]]       = INTERVALS_EMOJI_CONCRET + INTERVALS_VARIOUS + INTERVALS_ADD_ARROWS + INTERVALS_QRCODE
INTERVALS_MATH_2: list[tuple[int, int]]                 = INTERVALS_LETTERLIKE + INTERVALS_MATH_OPERATORS + INTERVALS_MATH_EXTRA
INTERVALS_MATH_OPERATORS_2: list[tuple[int, int]]       = INTERVALS_MATH_OPERATORS + INTERVALS_MATH_SYMBOLS
INTERVALS_OPERATORS_EXT: list[tuple[int, int]]          = INTERVALS_ESYMBOLS_CONCRET + INTERVALS_MATH_OPERATORS_2 + INTERVALS_MATH_ARROWS + INTERVALS_MATH_EXTRA
INTERVALS_LOGIC_EXT: list[tuple[int, int]]              = INTERVALS_ADD_ARROWS + INTERVALS_MATH_ARROWS + INTERVALS_MATH_LOGIC + INTERVALS_MATH_SYMBOLS
INTERVALS_HEXAGRAMS: list[tuple[int, int]]              = [(0x4DC0, 0x4DFF)]  # [Hexagrams
INTERVALS_FIRST: list[tuple[int, int]]                  = [(0x4E00, 0x4E00),]  # First.]
INTERVALS_LISA: list[tuple[int, int]]                   = [(0xA4D0, 0xA4FF)]  # Lisa.]]
INTERVALS_GENRE: list[tuple[int, int]]                  = [(0x1F6B9, 0x1F6BA)]  # Coloured Man/Woman
INTERVALS_BGENRE: list[tuple[int, int]]                 = [(0x1B000, 0x1B001)]  # C'est un gars une fille xd]]]
INTERVALS_XGENRE: list[tuple[int, int]]                 = [(0x2600, 0x26FF)]  # X-Genre]]
INTERVALS_ZGENRE: list[tuple[int, int]]                 = [(0x1F650, 0x1F6B8), (0x1F6BB,0x1F7F0)]
INTERVALS_EXTGENRE: list[tuple[int, int]]               = INTERVALS_XGENRE + INTERVALS_ZGENRE  # Extended Genre.]
##########################################
###         😀    🀀🌀🚀🚁             ###
##########################################
# Patterns : version 3 emojis (entre guillemets triples pour lisibilité)
PATTERNS_E: list[str] = [
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}",
    "\\U{XXXXX:08X}\\U{SPECIAL2:08X}",
    "\\U{SPECIAL1:08X}\\U0000FE0F\\U0000200D\\U{XXXXX:08X}",
    "\\U{SPECIAL1:08X}\\U0000200D\\U{XXXXX:08X}",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}",
    "\\U{SPECIAL2:08X}\\U0000FE0F\\U0000200D\\U{XXXXX:08X}",
    "\\U{SPECIAL2:08X}\\U0000200D\\U{XXXXX:08X}",
    "\\U{SPECIAL2:08X}\\U{XXXXX:08X}",
    "\\U{XXXXX:08X}"
]
PATTERNS_3: list[str] = [
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL1:08X}\\U0000FE0F\\U{YYYYY:08X}\\U0000200D\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U0000FE0E\\U{YYYYY:08X}\\U0000200D\\U{SSSSS:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U0000FE0F\\U{YYYYY:08X}\\U0000200D\\U{SSSSS:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U0000FE0E\\U{YYYYY:08X}\\U0000200D\\U{SSSSS:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U0000200D\\U{SSSSS:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U{SSSSS:08X}\\U{TTTTT:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U0000200D\\U{SSSSS:08X}\\U{TTTTT:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U0000200D\\U{SSSSS:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}\\U{SSSSS:08X}",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U{SSSSS:08X}",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SSSSS:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SSSSS:08X}\\U{SPECIAL1:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SSSSS:08X}\\U{SPECIAL2:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SSSSS:08X}",
]
PATTERNS_3b: list[str] = []

# Patterns : version 2 emojis
PATTERNS_2: list[str] = [
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL1:08X}\\U0000FE0F\\U{YYYYY:08X}\\U0000200D\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL2:08X}\\U0000FE0F\\U{YYYYY:08X}\\U0000200D\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL2:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U0000200D\\U{SPECIAL2:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}",
    "\\U{XXXXX:08X}\\U0000FE0F\\U{YYYYY:08X}\\U0000200D\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U0000FE0F\\U{YYYYY:08X}\\U0000200D\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U0000200D\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U0000200D\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U{YYYYY:08X}",
    "\\U{XXXXX:08X}\\U{SPECIAL2:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL2:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{XXXXX:08X}\\U{SPECIAL2:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{XXXXX:08X}\\U{SPECIAL2:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{XXXXX:08X}\\U{SPECIAL2:08X}\\U{YYYYY:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{XXXXX:08X}\\U{YYYYY:08X}",
    "\\U{SPECIAL2:08X}\\U{XXXXX:08X}\\U{YYYYY:08X}",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}\\U{YYYYY:08X}",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{SPECIAL2:08X}\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{SPECIAL2:08X}\\U{XXXXX:08X}\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{SPECIAL2:08X}\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}\\U{SPECIAL1:08X}",
    "\\U{SPECIAL2:08X}\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}\\U{SPECIAL2:08X}",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{SPECIAL1:08X}\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{SPECIAL2:08X}\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{SPECIAL2:08X}\\U{XXXXX:08X}\\U0000200D\\U{YYYYY:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{SPECIAL1:08X}\\U0000FE0F\\U0000200D\\U{XXXXX:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{SPECIAL1:08X}\\U0000FE0F\\U0000200D\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U0000FE0F",
    "\\U{SPECIAL2:08X}\\U0000FE0F\\U0000200D\\U{XXXXX:08X}\\U{SPECIAL2:08X}\\U0000FE0F",
    "\\U{SPECIAL2:08X}\\U0000FE0F\\U0000200D\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U0000FE0F"
]
ALL_PATTERNS: list[str] = PATTERNS_3 + PATTERNS_2 + PATTERNS_E
ALL_PATTERNS_GENREAL: list[str] = [
    "\\U{XXXXX:08X}\\U{SPECIAL1:08X}\\U0000FE0F\\U{YYYYY:08X}\\U{SSSSS:08X}\\U0000200D\\U{SPECIAL1:08X}\\U0000FE0F",
    # ... etc. (les 7 patterns)
]

    ##################################
###             🀀🌀🚀🚁        😀     ###
##########################################
   ####################################
    ### Pick random bools
def pdqsvp____(n=345, l=20) -> str:
    ### Pas De Question Svp
    fprint, tools = "", pick_random_septool()
    for _ in range(n):
        markerq = "\n" if _% (n//l) == 0 else ""
        if not tools:
            fprint += f"{markerq}"
        else:
            tools -= 1
            fprint += (f"{markerq}" if not tools else f"{markerq}")  # 
        tools = pick_random_septool()
    return fprint
def pick_random_bool() -> bool:
    return bool(os.urandom(1)[0] % 2)
def pick_random_tool() -> Union[complex, bool]:
    tool = os.urandom(1)[0] % 3
    return I if not tool else (not tool % 2)
def pick_random_tool_concret() -> bool:
    tool = os.urandom(1)[0] % 3
    return True if not tool else (not tool % 2)
def pick_random_tool_inside() -> tuple[bool,bool]:
    tool = os.urandom(1)[0] % 3
    return (False, True) if tool else (True, not tool % 2)
def pick_random_septool() -> Union[complex, bool]:
    ool = os.urandom(1)
    septool = os.urandom(1)[0] % 7
    #print(ool)
    parenthese_print(ool)
    ### 'ð', 'ñ', 'ÿ', ' '
    ### 'f0', 'f1', 'ff' ,'00'
    return I if not septool else (not septool % 2)
def parenthese_print(ool: bytes=bytes(0xF1)) -> bool:
    def affiche_clairement(byte_char):
        intv = int.from_bytes(byte_char)
        raw = force_affichage_hex(byte_char)
        try:
            if intv == 0x08:
                print(f"[{raw}]: {''}")
                return True
            elif intv == 0x09:
                print(f"[{raw}]: {''}")
                return True
            elif intv == 0x0a:
                print(f"[{raw}]: {''}")
                return True
            elif intv == 0x0b:
                print(f"[{raw}]: {''}")
                return True
            elif intv == 0x0c:
                print(f"[{raw}]: {''}")
                return True
            elif intv == 0x0d:
                print(f"[{raw}]: {''}")
                return True
            elif intv == 0x20:
                print(f"[{raw}]: {''}")
                return True
            elif intv == 0x7f:
                print(f"[{raw}]: {''}")
                return True
            elif intv < 0x20:
                print(f"[{raw}]: {''}")
                return True
            else:
                # Tente de décoder le byte en UTF-8 puis d'afficher
                char = byte_char.decode('utf-8')
                print(f"[{raw}]: {char}")
            return True
        except UnicodeDecodeError:
            # Ne peut pas afficher directement
            print(f"[{raw}] : ⚫")
            return False
    return affiche_clairement(ool)
def force_affichage_hex(byte_char : bytes) -> str:
    # Affiche toujours en notation hex explicite b'\x??'
    return "b'" + ''.join(f'\\x{b:02x}' for b in byte_char) + "'"
def pick_random_pool(n=23) -> Union[complex, bool]:
    p = n if sympy.isprime(n) else sympy.nextprime(n)
    pool = int.from_bytes(os.urandom(2), 'big') % p
    return I if not pool else (not pool % 2)
def pick_random_oddnool_big(n=42) -> Union[complex, bool]:
    nool = int.from_bytes(os.urandom(2), 'big') % (2*n + 1)
    return I if not nool else (not nool % 2)
def pick_random_oddnool_lite(n=42) -> Union[complex, bool]:
    if not n%2:
        return pick_random_oddnool_big((n-1)//2)
    odd = v2(n)[1]  # Odd piece of code...
    return pick_random_oddnool_big((odd-1)//2)
def pick_random_nool(n=0x10) -> Union[complex, bool]:
    nool = int.from_bytes(os.urandom(2), 'big') % n
    return I if not nool else (not nool % 2)
def v2(n=42) -> tuple[int,int,Union[int,bool]]:
    ### Return (i,q,v) with
    ### 🟠 i = valuation 2adique of n, and n = q*2^i
    ### 🟡 q = odd remain
    ### 🟤 v = absolute value or not isFinite()
    ###
    def v2abs(l):
        return 1 / (2 ** l) if l else True
    i = 0
    while not(n % 2 or not n):
        i+=1
        n //= 2
    return i, n, v2abs(n)
def vp(n=42, p=3) -> tuple[int,int,Union[int,bool]]:
    ### Return (i,q,v) with n = q*p^i
    ### 🟠 i = valuation p-adique of n
    ### 🟡 q = non-p remain e.g gcd(p,q) = 1
    ### 🟤 v = absolute value or not isFinite()
    ###
    def vpabs(l):
        return 1 / (p ** l) if l else True
    i = 0
    while not(n % p or not n):
        i+=1
        n //= p
    return i, n, vpabs(n)

    ##################################
###             🀀🌀🚀🚁        😀     ###
##########################################
   ##########################🃏
    #################################
    ### Pick random symbols
def pick_random_emoji_interval(intervals_emoji: list[tuple[int, int]] = None, coulour = None) -> tuple[int, int]:
    ### Pioche un intervalle aléatoire dans la liste des intervalles d'émojis.
    ###     1) INTERVALS, INTERVALS_EMOJI, INTERVALS_EMOJI_ADD, INTERVALS_VARIOUS, INTERVALS_ADD_ARROWS, INTERVALS_QRCODE
    ###     2) INTERVALS_MATH, INTERVALS_LETTERLIKE, INTERVALS_MATH_LOGIC, INTERVALS_MATH_OPERATORS, INTERVALS_MATH_EXTRA, INTERVALS_MATH_SYMBOLS, INTERVALS_MATH_ARROWS
    ###     3) INTERVALS_EMOJI_CONCRET, INTERVALS_ESYMBOLS_CONCRET, INTERVALS_MATH_2, INTERVALS_MATH_OPERATORS_2, INTERVALS_OPERATORS_EXT, INTERVALS_LOGIC_EXT
    ###     4) INTERVALS_EARLY, INTERVALS_EARLY_LETTERS, INTERVALS_EARLY_EXT, INTERVALS_PICTOGRAMMES
    ###     5) INTERVALS_VARIOUS_EARLY, INTERVALS_HIGHER
    ###     6) ?
    ###     7) INTERVALS_PRIVATE, INTERVALS_PRIVATE_EXT, INTERVALS_END
    local_constint = INTERVALS_EMOJI_CONCRET if not coulour and not (os.urandom(1)[0]%2) else random.choice((INTERVALS_EMOJI_CONCRET,INTERVALS_ESYMBOLS_CONCRET))
    local_inputkek = intervals_emoji if intervals_emoji else local_constint
    tool = int.from_bytes(os.urandom(2), 'big') % len(local_inputkek)
    return local_inputkek[tool]
def pick_random_emoji(intervals_emoji: list[tuple[int,int]] = None) -> int:
    fresult = pick_random_emoji_interval(intervals_emoji)
    tool = int.from_bytes(os.urandom(2), 'big') % len(fresult)
    return fresult[tool]
def pick_random_genre() -> str:
    male=f"\u2642\ufe0f"
    female=f"\u2640\ufe0f"
    return male if not pick_random_pool() else female
def pick_random_xgenre(intervals_genre: list[tuple[int,int]] = None) -> int:
    ### Pioche un genre aléatoire dans l'intervalle de genre.
    ### - ♀ = 0x2640,
    ### - ♂ = 0x2642.
    ### - etc.
    local_inputkek = intervals_genre if intervals_genre else [(0x2600, 0x26FF), (0x1F650, 0x1F6B8), (0x1F6BB,0x1F7F0)]
    local_interval = quc.UnicodeIntervals(local_inputkek)
    fresult = local_interval.to_ordered_list()
    tool = int.from_bytes(os.urandom(2), 'big') % len(fresult)
    return fresult[tool]
def pick_random_arrow(intervals_arrow: list[tuple[int,int]] = None) -> int:
    local_inputkek = intervals_arrow if intervals_arrow else [(0x2190, 0x21FF), (0x1F800, 0x1F8C1)]
    local_interval = quc.UnicodeIntervals(local_inputkek)
    fresult = local_interval.to_ordered_list()
    tool = int.from_bytes(os.urandom(2), 'big') % len(fresult)
    return fresult[tool]
def pick_random_math(intervals_math = (0x2A00, 0x2AFF)) -> int:
    ### Pioche un intervalle aléatoire dans la liste des intervalles d'émojis.
    return random.randint(intervals_math[0], intervals_math[1])
def pick_random_math_2(intervals_math: list[tuple[int, int]] = None) -> int:
    if intervals_math is None:
        intervals_math = INTERVALS_MATH_2
    return pick_random_cp_2(intervals_math)
def pick_random_math_3(intervals_math: list[tuple[int, int]] = None) -> int:
    if intervals_math is None:
        intervals_math = INTERVALS_MATH_OPERATORS_2
    return pick_random_cp_2(intervals_math)
def pick_random_logic(intervals_logic: list[tuple[int, int]] = None) -> int:
    if intervals_logic is None:
        intervals_logic = INTERVALS_MATH_LOGIC
    return pick_random_cp_2(intervals_logic)
def pick_random_operator(intervals_operator: list[tuple[int, int]] = None) -> int:
    if intervals_operator is None:
        intervals_operator = INTERVALS_MATH_OPERATORS_2
    return pick_random_cp_2(intervals_operator)
def pick_random_cp(intervals: list[tuple[int, int]] = None) -> int:
    ### Pioche un codepoint aléatoire dans la liste d'intervalles.
    if intervals is None:
        intervals = INTERVALS_EMOJI_CONCRET

    (start, end) = random.choice(intervals)
    return random.randint(start, end)
def pick_random_cp_2(intervals: list[tuple[int, int]] = None) -> int:
    if intervals is None:
        intervals = INTERVALS
    ###
    ### intervals : liste de tuples (start, end)
    ### Renvoie un entier choisi uniformément dans l'union de tous ces intervalles.
    ###
    # 1) Taille totale
    total_size = 0
    sizes = []
    for (start, end) in intervals:
        size = (end - start + 1)
        sizes.append(size)
        total_size += size
    ###
    # 2) On génère un nombre aléatoire "quantique" (ou pseudo) dans [0, total_size-1].
    #    Par exemple en convertissant os.urandom(...) si tu veux du 100% système.
    random_bytes = os.urandom(4)  # 4 octets = 32 bits
    rand_int = int.from_bytes(random_bytes, 'big') % total_size

    # 3) On détermine dans quel intervalle 'rand_int' tombe
    cumulative = 0
    i: int
    for i, (start, end) in enumerate(intervals):
        size = sizes[i]
        if rand_int < cumulative + size:
            # Il est dans cet intervalle
            offset = rand_int - cumulative
            return start + offset
        cumulative += size
    ###
    # En théorie, on ne devrait jamais arriver ici
    raise RuntimeError("Logic error in pick_random_cp.2")
########################
####################
####
######.
    #######
    ### Some interesting bool functions.
def is_single_grapheme(s: str) -> bool:
    ### Vérifie si la chaîne s est UNE seule grappe via regex \X.
    graphemes = list(regex.finditer(r"\X", s))
    return len(graphemes) == 1
def is_double_grapheme(s: str) -> bool:
    graphemes = list(regex.finditer(r"\X", s))
    return len(graphemes) == 2
def is_triple_grapheme(s: str) -> bool:
    # ^ et $ ancrent le match au début et à la fin de la chaîne
    # \X{2} signifie “exactement deux grappes de caractères Unicode”
    return bool(regex.fullmatch(r"\X{3}", s))
def is_printable_noncontrol(s: str) -> bool:
    ###
    ### Vérifie que chaque codepoint de 's' est imprimable, non-vide
    ### et qu'il n'appartient pas aux catégories de contrôle / séparateurs.
    ###
    if not s:
        return False
    for ch in s:
        if not ch.isprintable():
            return False
        if ch.strip() == "":
            return False
        cat = unicodedata.category(ch)
        if cat in ['Cc', 'Zl', 'Zp']:  # Contrôle, etc.
            return False
    return True
def is_single_grapheme_different(base_char: str, combined: str) -> bool:
    ###
    ### Vérifie que 'combined' forme exactement UNE grappe (\X via la lib 'regex')
    ### et que cette grappe est différente de base_char seul.
    ###
    graphemes = list(regex.finditer(r"\X", combined))
    if len(graphemes) == 1:
        return graphemes[0].group() != base_char
    return False
    ### Getters and specific to QUnicode.py
def get_interval_length(interval: list[tuple[int, int]]) -> int:
    quint = quc.UnicodeIntervals(interval)
    return quint.total_length()
def getlength_grapheme(s: str) -> int:
    graphemes = list(regex.finditer(r"\X", s))
    return len(graphemes)
def get_grapheme_codepoints_sizes(s: str) -> list[int]:
    ###
    ### Retourne une liste où chaque élément est la 'taille en codepoints'
    ### du grapheme correspondant.
    ###
    sizes = []
    for match in regex.finditer(r"\X", s):
        grapheme_str = match.group()  # la sous-chaîne correspondant à cette grappe
        sizes.append(len(grapheme_str))  # combien de codepoints dans cette grappe
    return sizes
def get_gendered_emoji() -> int:
    random_pick = (lambda x: 0 if x < 37 else (1 if x < 146 else 2))(os.urandom(1)[0])
    return get_xgendered_emoji() if not random_pick else (0x2640 if not (random_pick % 2) else 0x2642)
def get_xgendered_emoji() -> int:
    random_byte = os.urandom(1)[0]  # entre 0 et 255
    genre_cp = 0x2600 + random_byte
    return genre_cp
    ### Old builders
def build_random_sequence(patterns: list[str]=None) -> str:
    if patterns is None:
        patterns = ALL_PATTERNS
    ### Construit une séquence Unicode 'cryptique' en choisissant :
    ###   - un pattern au hasard
    ###   - remplace {XXXXX}, {YYYYY}, {SSSSS}, {TTTTT} par des cp random
    ###     issus de tes intervals
    ###   - {26XX} sera un codepoint dans la plage 0x2600-0x26FF
    ###

    pattern = random.choice(patterns)
    # Remarque : le placeholder "26XX" on peut le forcer à être
    # un codepoint entre 0x2600 et 0x26FF :
    cp_26xx = random.randint(0x2600, 0x26FF)
    cp_27xx = random.randint(0x2700, 0x27FF)
    ###
    # On va récupérer différents codepoints potentiels
    cp_x = pick_random_cp(INTERVALS)  # XXXXX
    cp_y = pick_random_cp(INTERVALS)  # YYYYY
    cp_s = pick_random_cp(INTERVALS)  # SSSSS
    cp_t = pick_random_cp(INTERVALS)  # TTTTT
    ###
    # On remplace dans le pattern
    # :04X → hex sur 4 chiffres (si > U+FFFF, faudrait :08X, etc.)
    out = pattern.format(
        XXXXX=cp_x,
        YYYYY=cp_y,
        SSSSS=cp_s,
        TTTTT=cp_t,
        # On force 2 hex digits après 26 ?
        # Non, on intègre carrément la valeur "cp_26xx" en 4 hex
        # comme on fait pour les placeholders.
        SPECIAL1=cp_26xx,
        SPECIAL2=cp_27xx
    )
    ###
    # 'out' est une chaîne littérale, ex: "\u1F60A\uFE0F\u26C4..."
    # On veut l'évaluer en tant que véritables séquences Unicode
    # → on peut faire un "encode puis decode" ou utiliser "unicode_escape"
    # OU on peut faire "eval" si on est prudent (mais c'est risqué).
    # Il vaut mieux faire :
    real_str = out.encode("utf-8").decode("unicode_escape")
    return real_str
def build_random_logic_expression() -> str:
    ###
    ### Construit une expression aléatoire.
    ### - Dans 1/3 des cas (form=0), on fait : \U000XXXXX\U000YYYYY
    ### - Dans 2/3 des cas, on choisit form = 1, 2, ou 3 uniformément
    ###   (les trois cas existants).
    ###
    ### Les 3 cas existants (1,2,3) sont décrits auparavant :
    ###   1)  \U000XXXXX\u<logic>\s\u<operateur>\(\U000YYYYY\)
    ###   2)  \U000XXXXX<build_random_sequence()>\u<logic>\s\u<operateur>\(\U000YYYYY\)
    ###   3)  \U000XXXXX<build_random_sequence()>\u<logic>\s\u<operateur>\(<build_random_sequence()>\)
    ###
    ### On renvoie une chaîne Python finale (grappes non garanties !).
    ###
    ### Choisir form=0 avec proba 1/3, sinon form=1,2,3 (au hasard).
    ###
    # 1) Choisir aléatoirement l'une des 3 formes
    p = random.random()
    if p < 1/3:
        form = 0
    else:
        form = random.choice([1, 2, 3])
    ###
    # 2) Récupérer un codepoint X + un codepoint Y
    cp_x = pick_random_cp_2(INTERVALS_EMOJI)  # un codepoint émoji dans [1F300..1FAFF]
    cp_y = pick_random_cp_2(INTERVALS_EMOJI)
    ###
    # On génère leurs chaînes littérales "\U000XXXXX" (8 hex digits)
    # {cp_x:08X} => ex. "0001F623"
    base_emoji_x = f"\\U{cp_x:08X}"  # ex: "\U0001F600"
    base_emoji_y = f"\\U{cp_y:08X}"
    ###
    ### Si form=0, on se contente de concaténer X + Y
    if form == 0:
        pattern = "{X}{Y}"
        out = pattern.format(X=base_emoji_x, Y=base_emoji_y)
        final_str = out.encode("utf-8").decode("unicode_escape")
        return final_str
    ###
    ### Sinon, on gère form=1,2,3 comme avant
    # 3)a) On génère un symbole logique (opérateurs logiques, flèches, etc.)
    # 3)b) On génère un opérateur math (par exemple dans INTERVALS_MATH_OPERATORS)
    logic_cp = pick_random_cp_2(INTERVALS_MATH_LOGIC)  # ex. => \u2192 (→)
    oper_cp = pick_random_cp_2(INTERVALS_MATH_OPERATORS) # ex. => \u2249 (≉)
    logic_str = f"\\U{logic_cp:08X}"
    oper_str = f"\\U{oper_cp:08X}"
    ###
    # 4) On décide si on met un "mini-emoji fusions" (build_random_sequence()) à la place de X ou Y
    #    ou s'il s'agit juste du codepoint émoji.
    #    Pour le style, form 2 → X + build_random_sequence()
    #                   form 3 => X + build_random_sequence() ET Y + build_random_sequence()
    ###
    if form == 1:
        # "\U000XXXXX\u<logic>\s\u<operateur>\(\U000YYYYY\)"
        # On insère un espace ou non ? Au choix :
        # Ex :  \U0001F623\U00002192 \U00002295 (\U0001F600)
        pattern = (
            "{BASE_X}{LOGIC_STR}{OPER_STR}"
            "\\u0028{BASE_Y}\\u0029"  # \u0028 => "(" , \u0029 => ")"
        )
        out = pattern.format(
            BASE_X=base_emoji_x,
            LOGIC_STR=logic_str,
            OPER_STR=oper_str,
            BASE_Y=base_emoji_y
        )
    ###
    ### X + build_random_sequence() + logic + oper + ( Y )
    ###
    elif form == 2:
        # "\U000XXXXX<build_random_sequence()>\u<logic>\s\u<operateur>\(\U000YYYYY\)"
        # => On remplace X par (X + build_random_sequence())
        #    Y reste un simple codepoint
        mini_seq = build_random_sequence()  # On aura un truc type "\U0001F600\U0001F3FF" ...
        # mini_seq est déjà “décodé” → on doit le reconvertir en forme littérale si on veut coller au pattern
        # OU plus simple : on l'insère tel quel, et on fera encode/decode à la fin globale.
        ###
        # Pour coller au style "littéral" → on peut s'en passer,
        #   on va juste concaténer la variable `mini_seq` brut,
        #   sachant qu'ensuite on fera .encode().decode("unicode_escape").
        mini_seq_lit = mini_seq.encode('unicode_escape').decode('ascii')
        # => "\U0001F600\U0001F3FF", etc. (des séquences littérales)
        ###
        pattern = (
            "{BASE_X}{MINI_SEQ}{LOGIC_STR}{OPER_STR}"
            "\\u0028{BASE_Y}\\u0029"
        )
        # On concatène mini_seq à la *forme littérale* qu’on prépare,
        # en évitant de tout casser.
        # Astuce : on remplace chaque backslash de mini_seq par un double backslash
        #   pour qu'il soit bien pris en compte dans le "big" out littéral.
        ###
        out = pattern.format(
            BASE_X=base_emoji_x,
            MINI_SEQ=mini_seq_lit,
            LOGIC_STR=logic_str,
            OPER_STR=oper_str,
            BASE_Y=base_emoji_y
        )
    ###
    else:
        # form == 3
        # "\U000XXXXX<build_random_sequence()>\u<logic>\s\u<operateur>\(<build_random_sequence()>\)"
        mini_seq_x = build_random_sequence()
        mini_seq_y = build_random_sequence()
        ###
        mini_seq_x_lit = mini_seq_x.encode('unicode_escape').decode('ascii')
        mini_seq_y_lit = mini_seq_y.encode('unicode_escape').decode('ascii')
        ###
        # => \U000XXXXX + mini_seq_x + \u<logic> + \u<oper> + (mini_seq_y)
        # Y n’est plus un codepoint tout seul, c’est un build_random_sequence() entre parenthèses
        pattern = (
            "{BASE_X}{MINI_SEQ_X}{LOGIC_STR}{OPER_STR}\\u0028{MINI_SEQ_Y}\\u0029"
        )
        out = pattern.format(
            BASE_X=base_emoji_x,
            MINI_SEQ_X=mini_seq_x_lit,
            LOGIC_STR=logic_str,
            OPER_STR=oper_str,
            MINI_SEQ_Y=mini_seq_y_lit
        )
    ###
    # 6) On a un grand littéral “out” → on le convertit en vraies séquences Unicode
    final_str = out.encode("utf-8").decode("unicode_escape")
    ###
    return final_str
def build_gendered_emoji() -> str:
    ###
    ### Exemple : on crée un 'emoji base' + ZWJ + symbole de genre + Variation Selector
    ### ex : U+1F469 \u200D \u2640 \uFE0F  => femme
    ###
    base_cp = pick_random_cp_2(INTERVALS_EMOJI)
    genre_cp = (os.urandom(1)[0] % 3) + 0x2640
    if genre_cp == 0x2641:
        #grapheme = "\U"
        return chr(base_cp)+chr(get_xgendered_emoji())

    ## Variation selector 16 (emoji style):
    vs16_cp = 0xFE0F
    # ZWJ
    zwj_cp = 0x200D

    # On assemble
    candidate = (chr(base_cp)
                 + chr(zwj_cp)
                 + chr(genre_cp)
                 + chr(vs16_cp))
    return candidate
def build_xgendered_emoji(base_cp: int = None) -> str:
    ###
    ### Exemple : on crée un 'emoji base' + ZWJ + symbole de genre + Variation Selector
    ### ex : U+1F469 \u200D \u2640 \uFE0F  => femme
    ###
    base_cp = base_cp if base_cp is not None else pick_random_cp_2(INTERVALS_EMOJI_CONCRET)
    genre_cp = random.choice([0x2600, 0x26FF])  # x
    # Variation selector 16 (emoji style):
    vs16_cp = 0xFE0F
    # ZWJ
    zwj_cp = 0x200D

    # On assemble
    candidate = (chr(base_cp)
                 + chr(zwj_cp)
                 + chr(genre_cp)
                 + chr(vs16_cp))
    return candidate
    ### Old code
def generate_states_for(cp_x: int, intervals: list[tuple[int, int]] = None) -> tuple[list[str], list[str]]:
    if intervals is None:
        intervals = INTERVALS
    ###
    ### Renvoie deux listes :
    ###   - fused_states : Les combinaisons X+Y formant un seul glyph distinct.
    ###   - all_states   : Les fused_states + un fallback (X) si vide.
    ###
    base_char = chr(cp_x)
    fused_states = []

    for (start, end) in intervals:
        for cp_y in range(start, end + 1):
            char_y = chr(cp_y)
            combo = base_char + char_y
            if is_printable_noncontrol(combo) and is_single_grapheme_different(base_char, combo):
                fused_states.append(combo)

    # S'il n'y a aucun fused_state, on crée un fallback = [base_char]
    if not fused_states:
        all_states = [base_char]
    else:
        # On a au moins une fusion, on la liste + éventuellement on rajoute base_char
        # si tu veux l'avoir, mais ici on peut le mettre ou pas.
        # Pour imiter le comportement précédent, on ajoute base_char au final :
        all_states = [base_char] + fused_states

    return fused_states, all_states
def measure_fused_emoji(max_attempts=100) -> str:
    ###     # len(str) = 1
    ### Tente de fabriquer 'max_attempts' séquences aléatoires
    ### et renvoie la première qui est un "single grapheme".
    ### Sinon renvoie un message.
    ###
    for _ in range(max_attempts):
        candidate = build_random_sequence()
        if is_single_grapheme(candidate):
            return candidate
    return "⚫"

# -----------------------------------------------------------------------
#########################################################################################################
#
####################################### LE FAMEUX EMOJI QUANTIQUE ⟩.⟨####################################
#
# -----------------------------------------------------------------------
class QuantumEmoji:
    def __init__(self, emojson_filepath = None, intervals: list[tuple[int, int]] = None):
        ### Shar ->
        ###     ⟩0xD7FF,0xF900⟨,
        ###
        # On charge le JSON
        self.universe = intervals if intervals is not None else INTERVALS
        self.emojson_filepath = "precomputed_emoji_data.json" if not emojson_filepath else emojson_filepath
        with open(self.emojson_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Reconversion des clés str -> int
        fused_str_keys = data["fused"]
        all_states_str_keys = data["all_states"]
        self.map_cp_to_fused_states = {int(k): v for k, v in fused_str_keys.items()}
        self.map_cp_to_all_states   = {int(k): v for k, v in all_states_str_keys.items()}
        # On construit la liste des clés
        self.all_keys = list(self.map_cp_to_all_states.keys())
        self.e = "🚁"
        self.f = 0xF0F1
        self.g = False
        # ... et le reste de ton init (operator, arrow, wave, etc.)
        self.emoji = chr(pick_random_cp_2(INTERVALS_EMOJI)) # self.emoji est maintenant un string “émoji”
        self.state = chr(pick_random_cp_2(INTERVALS_EMOJI))
        self.arrow = chr(pick_random_arrow())
        self.gender = pick_random_genre()
        # Bon → par ex. on prend le premier codepoint de self.emoji
        if self.emoji:
            base_cp = ord(self.emoji[0])  # int codepoint
            self.xgender = build_xgendered_emoji(base_cp)
        else:
            # si self.emoji est vide, on prend un random
            self.xgender = build_xgendered_emoji()
        self.complicated = f"{self.state}{self.gender}"
        self.simple = f"{self.emoji}{self.arrow}{self.state}"
        self.operator = chr(pick_random_operator())
        rand_int = int.from_bytes(os.urandom(2), 'big') % 3
        self.side = (
            f"{self.operator}_{self.emoji}({self.state})" if rand_int % 3 == 0 else
            (f"{self.operator}^{self.emoji}({self.state})" if rand_int % 3 == 2 else f"{self.operator}({self.emoji})={self.state}")
        )
        self.outsde = f"{self.operator}_{self.emoji}({self.state})"
        self.inside = f"{self.operator}^{self.emoji}({self.state})"
        self.wave = f"{self.emoji}{self.arrow} {self.operator}({self.state}).{self.outsde}"
        self.wave_error = f"{self.emoji}({self.arrow}{self.state})∴{self.outsde}"
        self.measure = f"Φ[{self.emoji}, {self.state}, {self.arrow}, {self.gender}, {self.simple}, {self.complicated}, {self.operator}, {self.wave_error}, {self.wave}, {self.side}]"
        ### Concretement...
        ###
        ### Ici, « ⤳ » désigne la convergence d'une série de fonctions.
        ### - « (φ : ℂ(Xi, i=self.lenght) → ℂ) » désigne la limite de cette série de fractions rationelles trigonométriques.
        ###     **Rem : ℂ(Xi, i=self.lenght) est un corps, qui peut être « vraiment bien » si i est un nombre premier.
        ### - C'est une fonction analytique, et la convergence est garantie, disons si tant est qu'on parte d'un truc « bien ».
        ### - C'est self.concretement xdd
        ### - Concretement, self.concretement c'est une suite de tableaux (poids) que représentent les coefficients de chaque monome
        ###     **Rem : Il faut d'abords décomponser φi en éléments "simple". (cf. Décomposition des fractions rationnelles, ici trigonometriques)
        ### - On peut utiliser les corps finis pour les calculs, plutôt que ℂ lui-même, ou choisir une représentation dans ℚ[i] voir dans ℤ[i], ℤp[i].
        ### - L'important est que Φ est une fonction très bizarre, de i variables que l'on approxime par une série de Fourier,
        ###     ou une série de fractions rationnelles judicieusement choisies, et que l'on fait converger vers une fonction limite φ,
        ###     qui existe et qui est analytique. C'est beau la vie dans ℂ.
        ### - φ est une forme i-linéaire.
        ### - On retombe sur Minkowski-Hasse et généralisations.
        self.concretement = {self.g, self.emoji, self.state, self.arrow, self.gender, self.xgender, self.operator}
        self.concretement_2 = {"function" : [
              #  {"key": "1", "value" : 1.0, "rangex" : ([(1, 1)], self.g)},
             #   {"key": "e", "value" : wgt_e, "rangex" : ([(int(self.e), int(self.e))], self.g)},
            #    {"key": "f", "value" : wgt_f, "rangex" : ([(int(self.f), int(self.f))], self.g)},
           #     {"key": "g", "value" : self.g, "rangex" : ([(0, 0)], 1.0)},
          #      {"key": "cX", "value" : wgt_cX, "rangex" : (INTERVALS_EMOJI, self.g)},
         #       {"key": "cY", "value" : wgt_cY, "rangex" : (INTERVALS_EMOJI, float(self.state))},
        #        {"key": "cA", "value" : wgt_cA, "rangex" : (INTERVALS_MATH_ARROWS, math.atan2(float(self.state), float(self.emoji)))},
       #         {"key": "cG", "value" : wgt_cB, "rangex" : ([(1, 1)], 0.0) if (self.xgender != 0x2640 and self.xgender != 0x2642) else ([(0, 0)], 0)},
      #          {"key": "cGx", "value" : wgt_cGx, "rangex" : ([(0, 0)], 0)},
     #           {"key": "cO", "value": wgt_cO, "rangex": ([(0, 0)], 0)},
    #            {"key": "cC", "value" : wgt_cC, "rangex" : ([(0, 0)], 0)},
   #             {"key": "cS", "value" : wgt_cS, "rangex" : ([(0, 0)], 0)},
  #              {"key": "cOsd", "value" : wgt_cOsd, "rangex" : ([(0, 0)], 0)},
 #               {"key": "cWE", "value" : wgt_cWE, "rangex" : ([(0, 0)], 0)},
#                {"key": "cW", "value" : wgt_cW, "rangex" : ([(0, 0)], 0)}
                ]
        }
    def calcul_hinhin(self, lenght_hinhin):
        mid = 0x1F681
        length = 0x1FBFF - 0x1F000  # intervalle original voulu
        half_length = length // 2

        start_cp = mid - half_length
        end_cp = mid + half_length

    def get_universe(self):
        return self.universe
    def get_arrow(self):
        return self.arrow
    def measure_low(self) -> int:
        self.g = pick_random_cp_2(INTERVALS_EMOJI_CONCRET)
        return self.g
    def measure_complicated(self) -> complex:
        c = self.emoji * np.exp(I*self.g)
        return c
    def measure_any_emoji(self) -> str:
        ###
        ### Renvoie un état au hasard, y compris fallback (un seul codepoint).
        ###
        if not self.all_keys:
            self.measure_low()
            return "No available emojis."
        # Choix du codepoint
        cp_x = random.choice(self.all_keys)
        # Choix d'un état au hasard
        states = self.map_cp_to_all_states[cp_x]
        self.measure_low()
        return random.choice(states)
    def measure_fused_emoji(self, max_tries=61681) -> str:
        ###
        ### Ne renvoie qu'une fusion (X+Y) formant un seul glyph distinct.
        ### On boucle jusqu'à trouver un codepoint qui a au moins un fused_state.
        ### (Pour éviter un codepoint qui n'en a pas.)
        ###
        ### max_tries : nombre maximum d'essais pour ne pas tourner en boucle infinie
        ###             s'il y a peu ou pas de fusions dans la table.
        ###
        for _ in range(max_tries):
            cp_x = random.choice(self.all_keys)
            fused_list = self.map_cp_to_fused_states[cp_x]
            if fused_list:
                pick_random_e = random.choice(fused_list)
                if is_single_grapheme(pick_random_e):
                    #print(f"Heuu Random ici : {pick_random_e}")
                    self.measure_low()
                    return pick_random_e
        # Si on n'en trouve vraiment pas...
        self.measure_low()
        return "No fused emoji found."
    def measure_fused_emoji_ex(self, max_attempts=50) -> str:
        ###
        ### Version 'exotique' : fabrique dynamiquement des séquences
        ### pour voir si elles forment une seule grappe.
        ###
        candidate = self.emoji
        cX = self.emoji
        cY = self.state
        cA = self.arrow
        cG = self.gender
        cS = self.simple
        cC = self.complicated
        cO = self.operator
        cW = self.wave
        cWE = self.wave_error
        cOsde = self.outsde

        i_range = range(1, 61681)
        i_tries = random.choices(i_range, k=257)
        for i in range(max_attempts):
            i_prime = sympy.isprime(i)
            # Génération aléatoire...
            which = random.choice(["sequence", "logic", "gendered", "xgendered", "tone", "-> emoji"])
            if which == "sequence":
                candidate = build_random_sequence()
            elif which == "logic":
                candidate = build_random_logic_expression()
            elif which == "gendered":
                candidate = build_gendered_emoji()
            elif which == "xgendered":
                candidate = build_xgendered_emoji()
            elif which == "tone":
                base_cp = pick_random_cp_2(INTERVALS_EMOJI)
                tone_cp = random.randint(0x1F3FB, 0x1F3FF)
                candidate = chr(base_cp) + chr(tone_cp)
            else:
                # "-> emoji"
                arrow_cp = pick_random_arrow()
                base_cp = pick_random_cp_2(INTERVALS_EMOJI)
                candidate = chr(arrow_cp) + chr(base_cp)

            ### On test plusieurs options...
            ###
            if is_single_grapheme(candidate):
                # 1 grappe
                result_delombr = f"{candidate}"
                if i_prime:
                    print(f"Single Candidate :{result_delombr}")
                return result_delombr

            elif is_double_grapheme(candidate):
                # 2 grappes
                result_delombr = f"{candidate[0]}{candidate[1]}"
                if i_prime:
                    print(f"Double Candidate :{result_delombr}")
                return result_delombr

            elif is_triple_grapheme(candidate):
                # 3 grappes
                result_delombr = f"{candidate[0]}{candidate[1]}{candidate[2]}"
                if i_prime:
                    print(f"Triple Candidate :{result_delombr}")
                return result_delombr

            else:
                ### Construit un nouveau candidate pour debug
                ### (ici, c'est un mélange d'int + str)
                ### - On veut un nouveau cX = un codepoint emoji → en string
                ###
                new_cpX = pick_random_cp_2(INTERVALS_EMOJI)     # entier
                cX = chr(new_cpX)                               # string

                arrowX = pick_random_arrow()                    # entier
                cA = chr(arrowX)                                # string

                cpO = pick_random_operator()                    # entier
                cO = chr(cpO)                                   # string

                cpY = pick_random_cp_2(INTERVALS_EMOJI)         # entier
                cY = chr(cpY)                                   # string

                # out → un littéral style "\U0001F600" (si on veut) ou un vrai char
                # si c’est du debug, tu peux faire :
                out = f"\\U{cpY:08X}"  # un string littéral
                # Juste un debug ?
                cC = f"{cX}{cA}{cY}"
                cG = f"{chr(get_gendered_emoji())}"
                cS = f"{cX}{cG}"

                # U Random
                rand_int = int.from_bytes(os.urandom(2), 'big') % 3
                cOsde = (
                    f"{cO}_{cX}({cY})" if rand_int % 3 == 0 else
                    (f"{cO}^{cX}({cY})" if rand_int % 3 == 2 else f"{cO}({cX})={cY}")
                )
                cWE = f"{cX}({cA}{cY}).{cOsde}"
                cW = f"{cX}{cA} {cO}({cY})∴{cOsde}"
                ###
                ### Debug
                ###

                if i in i_tries:
                    print(f"Random.2 --Candidate : {cX}")
                    print(f"Random.2 --Arrow Candidate : {cA}")
                    print(f"Random.2 --Sequence Candidate : {cC}")
                    print(f"Random.2 --Logic Candidate : {cWE}")
                    print(f"Random.2 --Gender : {cG}")
                    print(f"Random.2 --XGender : {cS}")
                    print(f"Random.2 --Gendered : {cC}")
                    print(f"Random.2 --Function Candidate : {candidate}")
                    print(f"Random.2 --Indice, Exposant, Equivalent : {cOsde}")
                    print(f"Random.2 --Operator : {cO}")


                # Puis si tu veux "remplacer" cX par le littéral \U0001F600, tu peux
                cX = out  # cX devient le LITTÉRAL, plus un emoji.
        print(f"Random.2 --Candidate : {cX}")
        print(f"Random.2 --Candidate.2 : {cY}")
        print(f"Random.2 --Arrow Candidate : {cA}")
        print(f"Random.2 --Gender : {cG}")
        print(f"Random.2 --XGender : {cS}")
        print(f"Random.2 --Gendered : {cC}")
        print(f"Random.2 --Operator : {cO}")
        print(f"Random.2 --Logic Candidate : {cWE}")
        print(f"Random.2 --Wave Candidate : {cW}")
        print(f"Random.2 --Indice, Exposant, Equivalent : {cOsde}")
        print(f"Random.2 --Function Candidate : {candidate}")
        print(f"Random.2 --Wave Error Function : {self.wave_error}")
        print(f"Random.2 --Wave Function Candidate : {self.wave}")
        ### Inateignable
        self.emoji = cX
        self.state = cY
        self.arrow = cA
        self.gender = cG
        self.simple = cS
        self.complicated = cC
        self.operator = cO
        self.wave_error = cWE
        self.wave = cW
        self.side = cOsde
        self.measure = f"Φ[{cX}, {cY}, {cA}, {cG}, {cS}, {cC}, {cO}, {cWE}, {cW}, {cOsde}]"
        self.concretement = {"cX": int(cX), "cY": int(cY), "cA": int(cA)}
        print(f"Function Φ of parmaters : [{cX}, {cY}, {cA}, {cG}, {cS}, {cC}, {cO}, {cWE}, {cW}, {cOsde}]")
        self.measure_low()
        return self.measure
    def measure_quantumemoji(self):
        temp_var = f"{self.operator}^{self.emoji}({self.state})"
        self.measure_fused_emoji_ex(max_attempts=500)
        self.inside = temp_var
        result_ici = {
            "emoji" : f"{self.emoji}",
            "side" : f"{self.side}",
            "measure" : f"Φ : [{self.emoji}, {self.state}, {self.arrow}, {self.gender}, {self.xgender}, {self.simple}, {self.complicated}, {self.operator}, {self.wave_error}, {self.wave}, {self.side}] ⤳ ⟨φ : ℂ(Xi, i=self.lenght) → ℂ⟩"
            ### Ici, « ⤳ » désigne la convergence d'une série de fonctions.
            ### - « (φ : ℂ(Xi, i=self.lenght) → ℂ) » désigne la limite de cette série de fractions rationelles trigonométriques.
            ###     **Rem : ℂ(Xi, i=self.lenght) est un corps, qui peut être « vraiment bien » si i est un nombre premier.
            ### - C'est une fonction analytique, et la convergence est garantie, disons si tant est qu'on parte d'un truc « bien ».
            ### - C'est self.concretement xdd
            ### - Concretement, self.concretement c'est une suite de tableaux (poids) que représentent les coefficients de chaque monome
            ###     **Rem : Il faut d'abords décomponser φi en éléments "simple". (cf. Décomposition des fractions rationnelles, ici trigonometriques)
            ### - On peut utiliser les corps finis pour les calculs, plutôt que ℂ lui-même, ou choisir une représentation dans ℚ[i] voir dans ℤ[i], ℤp[i].
            ### - L'important est que Φ est une fonction très bizarre, de i variables que l'on approxime par une série de Fourier,
            ###     ou une série de fractions rationnelles judicieusement choisies, et que l'on fait converger vers une fonction limite φ,
            ###     qui existe et qui est analytique. C'est beau la vie dans ℂ.
            ### - φ est une forme i-linéaire, continue, analytique. Peut-être pas i-linéaire. Mais analytique, oui!
            ### - On retombe sur Minkowski-Hasse et généralisations.
        }
        self.measure_low()
        return result_ici
    def __getattr__(self, item):
        # Ici, on capture le contexte (.)
        return lambda op: f"{self.emoji}.{item}({op})"
    def __mul__(self, other):
        # Produit tensoriel simple, contexte maximal
        return f"{self.emoji}⊗{other.emoji if isinstance(other, QuantumEmoji) else other}"
    def __repr__(self):
        # Retourne un format "tuple" en string, ex. ( '🍂', '⚗️', '→', '🏹', '🙂', ... )
        return (
            f"("
            f"{self.e!r}, "  # '!' 'r' => on inclut la représentation "raw" de la chaîne
            f"{self.emoji!r}, "
            f"{self.state!r}, "
            f"{self.arrow!r}, "
            f"{self.gender!r}, "
            f"{self.xgender!r}, "
            f"{self.complicated!r}, "
            f"{self.simple!r}, "
            f"{self.operator!r}, "
            f"{self.side!r}, "
            f"{self.wave!r}, "
            f"{self.wave_error!r}, "
            f"{self.measure!r}"
            f")"
        )

# -----------------------------------------------------------------------
# EXEMPLE D'UTILISATION
# -----------------------------------------------------------------------

if __name__ == "__main__":
    time_start = time.time()/BEAUCOUP
    print(f"Il est  {time_start:.0f}.\n")

    # 1) On instancie le QuantumEmoji avec un fichier JSON pré-calculé (et les intervals).
    qe = QuantumEmoji("precomputed_emoji_data.json", INTERVALS)
    time_ding1 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding1:.0f}.\nIl s'est écoulé {(time_ding1 - time_start):.2f}.\n")

    # 2) Petit test sur une chaîne fixe (pour illustrer la segmentation graphemes)
    test = "🤛🏼🧕🏿👚"
    print("Test string:", test)
    print("Nombre de grappes :", getlength_grapheme(test))
    print("Codepoints par grappe :", get_grapheme_codepoints_sizes(test))
    print("-" * 40)
    time_ding2 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding2:.0f}.\nIl s'est écoulé {(time_ding2 - time_ding1):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding2 - time_start):.2f} depuis le début. ⌚")

    # 3) Essais sur measure_any_emoji
    print("=== 5 mesures aléatoires (any) ===")
    for _ in range(TRESGRAND_NOMBRE * 2):
        result = qe.measure_any_emoji()
        if (_ % 31) == 0 and is_printable_noncontrol(result):
            print(f"Mesure aléatoire : {result}")
    print("-" * 40)
    time_ding3 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding3:.0f}.\nIl s'est écoulé {(time_ding3 - time_ding2):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding3 - time_start):.2f} depuis le début. ⌚")

    # 4) Essais sur measure_fused_emoji (une seule grappe)
    print("=== 5 mesures aléatoires FUSION (une seule grappe) ===")
    for _ in range(TRESGRAND_NOMBRE * 2):
        fused = qe.measure_fused_emoji()
        if (_ % 31) == 0 and is_printable_noncontrol(fused):
            print(f"Mesure fusionnée : {fused}")
    print("-" * 40)
    time_ding4 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding4:.0f}.\nIl s'est écoulé {(time_ding4 - time_ding3):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding4 - time_start):.2f} depuis le début. ⌚")

    # 5) Quelques candidates issues de build_random_sequence
    print("=== 5 sequences aléatoires ===")
    for _ in range(TRESGRAND_NOMBRE * 2):
        seq = build_random_sequence()
        if (_ % 31) == 0 and is_printable_noncontrol(seq):
            print(f"Candidate: {seq}")
    print("-" * 40)
    time_ding5 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding5:.0f}.\nIl s'est écoulé {(time_ding5 - time_ding4):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding5 - time_start):.2f} depuis le début. ⌚")

    # 6) Quelques expressions logiques
    print("=== 5 expressions logiques aléatoires ===")
    for _ in range(TRESGRAND_NOMBRE * 2):
        expr = build_random_logic_expression()
        if (_ % 31) == 0 and is_printable_noncontrol(expr):
            print(f"Logical Candidate: {expr}")
    print("-" * 40)
    time_ding6 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding6:.0f}.\nIl s'est écoulé {(time_ding6- time_ding5):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding6 - time_start):.2f} depuis le début. ⌚")

    # 7) Vérifier measure_fused_emoji (fonction globale hors classe)
    print("=== 5 mesures globales measure_fused_emoji ===")
    for _ in range(TRESGRAND_NOMBRE * 2):
        fused_global = qe.measure_fused_emoji()
        if (_ % 31) == 0 and is_printable_noncontrol(fused_global):
            print(f"Fused?: {fused_global}")
    print("-" * 40)
    time_ding7 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding7:.0f}.\nIl s'est écoulé {(time_ding7- time_ding6):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding7 - time_start):.2f} depuis le début. ⌚")

    # 8) Tester measure_fused_emoji_ex (version exotique)
    print("=== 5 mesures exotiques via qe.measure_fused_emoji_ex() ===")
    for _ in range(TRESGRAND_NOMBRE * 2):
        exotic = qe.measure_fused_emoji_ex()
        if (_ % 31) == 0 and is_printable_noncontrol(exotic):
            print(f"Fusion Ex: {exotic}")
    print("-" * 40)
    time_ding8 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding8:.0f}.\nIl s'est écoulé {(time_ding8- time_ding7):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding8 - time_start):.2f} depuis le début. ⌚")

    # 9) Appeler measure_quantumemoji() pour voir comment il modifie des champs
    print("=== measure_quantumemoji() test ===")
    quantum_res = qe.measure_quantumemoji()
    print("Résultat measure_quantumemoji:", quantum_res)
    print("Champs internes modifiés :")
    print("  self.emoji         =", qe.emoji)
    print("  self.state         =", qe.state)
    print("  self.arrow         =", qe.arrow)
    print("  self.gender        =", qe.gender)
    print("  self.xgender       =", qe.xgender)
    print("  self.complicated   =", qe.complicated)
    print("  self.simple        =", qe.simple)
    print("  self.operator      =", qe.operator)
    print("  self.wave_error    =", qe.wave_error)
    print("  self.wave          =", qe.wave)
    print("  self.outsde        =", qe.outsde)
    print("  self.inside        =", qe.inside)
    print("  self.side          =", qe.side)
    print("-" * 40)
    time_ding9 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding9:.0f}.\nIl s'est écoulé {(time_ding9- time_ding8):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding9 - time_start):.2f} depuis le début. ⌚")

    # 10) Final debug / ending
    print("=== Fin des tests ===")
    time_ding10 = time.time()/BEAUCOUP
    print(f"Il est  {time_ding10:.0f}.\nIl s'est écoulé {(time_ding10- time_ding9):.2f} depuis la dernière fois 😠.\nIl s'est écoulé {(time_ding10 - time_start):.2f} depuis le début. ⌚")
    print(f"\nProcess time : {1000 * (time.time() - BEAUCOUP*time_start):.2f}ms.")
    print(f"Process time : {(time.time() - BEAUCOUP*time_start):.3f}s.")
    print(f"Random Bool: {pick_random_bool()}\nRandom Tool: {pick_random_tool()}")
    print(qe)
