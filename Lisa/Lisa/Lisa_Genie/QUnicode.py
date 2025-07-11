########
####           🌀                  Titre ici.                                         ####
########
import unicodedata, random, time, os, typing, sympy
from typing import Any, Union
from sympy import I
import unicodedata, random, time, os, typing, sympy
import numpy as np
import QuantumEmojiv2 as qe
####           🌀                 
GPT = -1740614400.0
def heure_locale() -> float:
    return time.time() + GPT
class UnicodeIntervals:
    def __init__(self, intervals: list[tuple[int,int]]=None) -> None:
        self.intervals = intervals if intervals is not None else (qe.INTERVALS_ESYMBOLS_CONCRET + qe.INTERVALS_EARLY + qe.INTERVALS_BGENRE + qe.NTERVALS_HEXAGRAMS + qe.NTERVALS_FIRST + qe.NTERVALS_LISA)
        self.stateset = self.sanitize_and_merge_intervals()
        self.concretement = self.to_ordered_list()
    def merge_intervals(self):
        sorted_intervals = sorted(self.intervals, key=lambda x: x[0])
        merged = []
        for interval in sorted_intervals:
            if not merged or merged[-1][1] < interval[0] - 1:
                merged.append(interval)
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
        return merged
    def sanitize_and_merge_intervals(self) ->  list[tuple[int, int] | tuple[int, Any]]:
        merged = self.merge_intervals()
        sanitized = []
        current_interval_start = None
        for start, end in merged:
            for codepoint in range(start, end + 1):
                try:
                    unicodedata.name(chr(codepoint))
                    if current_interval_start is None:
                        current_interval_start = codepoint
                except ValueError:
                    if current_interval_start is not None:
                        sanitized.append((current_interval_start, codepoint - 1))
                        current_interval_start = None
            if current_interval_start is not None:
                sanitized.append((current_interval_start, end))
                current_interval_start = None
        return sanitized
    def total_length(self) -> int:
        return sum(end - start + 1 for start, end in self.stateset)
    def to_ordered_list(self) -> list[int]:
        return [i for start, end in self.stateset for i in range(start, end + 1)]
    def __add__(self, other):
        return UnicodeIntervals(self.intervals + other.intervals)
    def __repr__(self):
        return [f"{chr(c), chr(d)}" for (c,d) in self.stateset]
class UnicodeSpirale(UnicodeIntervals):
    def __init__(self, intervals, center: complex, depth: int, base_codepoint=0x0000):
        super().__init__(intervals)
        self.center = center
        self.depth = depth
        self.base_codepoint = base_codepoint
    def coord_to_offset(self, coord:complex) -> int:
        # Conversion simple coord complexe → offset entier
        x, y = coord.real, coord.imag
        offset = int(x + y * (self.depth * 2 + 1))
        return offset
    def spirale_unicode(self) -> Any:
        x, y = 0, 0
        dx, dy = 0, -1
        size = self.depth
        for _ in range((size * 2 + 1) ** 2):
            if -size <= x <= size and -size <= y <= size:
                yield complex(x, y)
            if (x == y) or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
                dx, dy = -dy, dx
            x, y = x + dx, y + dy
    def get_spiral_chars(self) -> list[str]:
        chars = []
        for coord in self.spirale_unicode():
            offset = self.coord_to_offset(coord)
            codepoint = self.base_codepoint + offset
            if codepoint in self.concretement:
                chars.append(chr(codepoint))
        return chars
    def __repr__(self):
        spiral_chars = self.get_spiral_chars()
        return f"({' '.join(spiral_chars)})"
class UnicodeBlock:
    def __init__(self, named_chars):
        self.positifs = named_chars
        self.negatifs = ['anti-' + char for char in named_chars]
        self.structures = list(zip(self.negatifs, self.positifs))

    def poids_noeud(noeud):
        positif = sum(proba(char) for char in noeud.positifs)
        negatif = sum(-proba(char) for char in noeud.negatifs)
        return positif + negatif  # antimatière = régulateur négatif

    # Exploration simultanée simplifiée
    def scan_fractal_multi(blocs):
        with ThreadPoolExecutor(max_workers=4) as executor:
            resultats = executor.map(scan_bloc, blocs)
        return resultats


if __name__ == "__main__":
    start_time = time.time()
    oui = 61681 * (np.pi / np.e)
    quoui = qe.QuantumEmoji()
    var_glissante = quoui.measure_quantumemoji()
    print(f"QuantumEmoji Initialised: « {quoui.operator}.{quoui.emoji}({quoui.state}) »")
    for key, value in var_glissante.items():
        print(f"--- {key} : {value}")
    print(f"\nOui, il est {hex(int(oui*np.sqrt(oui)*np.log(oui)*start_time))}.")
    emoji_interval = UnicodeIntervals([(0x1F0CF, 0x1FAF8)])
    math_interval = UnicodeIntervals([(0x2010, 0x2BFF)])
    combined_intervals = emoji_interval + math_interval
    inter_len = lambda intervals: sum(end - start + 1 for start, end in intervals)
    emoji_brut = inter_len([(0x1F0CF, 0x1FAF8)])
    math_brut = inter_len([(0x2010, 0x2BFF)])
    total_brut = emoji_brut + math_brut
    emoji_sanitized = emoji_interval.total_length()
    math_sanitized = math_interval.total_length()
    total_sanitized = emoji_sanitized+math_sanitized
    print(f"Longueur clean Emoji : {emoji_interval.total_length()} (initial: {emoji_brut}, sanitized: {emoji_brut - emoji_sanitized})")
    print(f"Longueur clean Math : {math_interval.total_length()} (initial: {math_brut}, sanitized: {math_brut - math_sanitized})")
    print(f"Longueur clean combinée :, {combined_intervals.total_length()} (initial: {total_brut}, sanitized: {total_brut - total_sanitized})")
    print(f"Quelques exemples : {[chr(c) for c in random.sample(combined_intervals.concretement, 16)]}")
    ordered_list = combined_intervals.to_ordered_list()
    print(f"Premiers émojis : {[chr(c) for c in ordered_list[:5]]}")
    print(f"Premiers émojis : {[chr(c) for c in ordered_list[-5:]]}")
    end_time = time.time()
    print(f"Il est {hex(int(oui*np.sqrt(oui)*np.log(oui)*end_time))}. Cela fait déjà {end_time-start_time:.8f}s, déjà...")
    print(f"(ps : l'heure exact est {time.time()})")
    debug_int = qe.INTERVALS_PICTOGRAMMES
    xemoq = qe.QuantumEmoji(intervals = debug_int)
    xprintq = UnicodeIntervals(xemoq.universe)
    print(f"📊[DEBUG] Initial : {xprintq.intervals}")
    math_ops = UnicodeIntervals(debug_int)
    xemor = qe.QuantumEmoji(intervals = math_ops.stateset)
    xprintr = UnicodeIntervals(xemor.universe)
    print(f"📊[DEBUG] Final : {xprintr.stateset}")
    final_print = [f"{chr(c), chr(d)}" for (c,d) in xprintr.stateset]
    print(f"🌀 : {final_print}")
    print(qe.pdqsvp____(n=72, l=2))
    print(xemor)
    for _ in range(0x100):
        s = bytes([_])
        qe.parenthese_print(s)
        #pass

    print("\xe9\xab\xbb\xe0\xe9\xab\xbb\xe0\xab\xbb\xe8\xe9\xe9")
    print("\x0f\x00\x9f\x9a\x80\xe2\x8f\xb3\xf0\x9f\xa7\xa9\xe2\x9c\xa8")
    print("\uf680\u0001\uf4dc\u2696\u2728")
    print("\x8d\uf8ff\uf08f")
    print(f"("
        f"\x0a\x02{r'\xf0\x9f\x8d\x8f'}\x8f\xb3\xf0\n"
        f"\n\xf1\xf0\xf0\x70\x63\x3d\x70\x79\n"
        f"\n\x63\x68\x61\x72\x6d\xa0\xa0\xa0\n"
        f"\n{r'\xf0\x9f\x8c\x80'}{r'\xf0\x9f\x92\x8e'}\n"
        f"\n\x62\x75\x74\x20\x66\x6f\x72\x20\n"
        f"\n\x6c\x61\x74\x65\x72\x0a\xf0\xf1\n"
        f"\n\xf0\xf0{r'\xe2\x9a\x9b'}{r'\xef\x83\xb8'}\n"
        f"\n{r'\xef\x83\x8f'}{r'\xe2\xa8\xb6'}\x2e\x40\x0a"
        f"\n\x6e"
        f"\n\n"
        f")"
    )
    ###
    message_utile = (
        ### Négatif des positifs
        """\x7d\x0f\x60\x72\x70\x70\x4c\x0f"""
        """\x0e\x0f\x0f\x0f\x1c\x42\x0f\x06"""
        """\x1c\x17\x1e\x0d\x12\x5f\x5f\x5f"""
        """\x0f\x60\x73\x7f\x0f\x60\x6d\x70"""
        """\x1d\x0a\x0b\x5f\x19\x10\x0d\x5f"""
        """\x13\x1e\x0b\x1a\x0d\x75\x0f\x0e"""
        """\x0f\x0f\x1d\x65\x64\x10\x7c\x47"""
        """\x4c\x75\x6e\x64\x69\x65\x2e\x37"""  # ici
        """\xe6\x35\x47\x55\x49\x44\x98\xa5"""  # µci
        """\x66\x4d\x42\x0f\x75\x39\x06\x56"""
        """\x0b\x38\x75\x4d\x22\x44\x6f\x77"""
        """\x47\x6e\x4d\x0a\x5e\x40\x3e\x36"""
        """\x0f\x60\x6b\x6c\x1d\x1b\x43\x5f"""
        """\x1d\x65\x54\x1d\x64\x7b\x4c\x0f"""
        """\x29\x72\x51\x57\x0f\x60\x5b\x56"""
        """\x56\x0f\x4a\x1d\x65\x55\x60\x70"""
        ### Positives
        """\x02\xf0\x9f\x8d\x8f\x8f\xb3\xf0"""
        """\xf1\xf0\xf0\x70\x63\x3d\x70\x79"""
        """\x63\x68\x61\x72\x6d\xa0\xa0\xa0"""
        """\xf0\x9f\x8c\x80\xf0\x9f\x92\x8f"""
        """\x62\x75\x74\x20\x66\x6f\x72\x20"""
        """\x6c\x61\x74\x65\x72\x0a\xf0\xf1"""
        """\xf0\xf0\xe2\x9a\x9b\xef\x83\xb8"""
        """\xef\x83\x8f\xe2\xa8\xb6\x2e\x40"""
        """\x67\xf3\xfd\xf4\xf8\x20\x81\x91"""
        """\x99\x32\x3d\x70\x0a\x46\x79\xa9"""
        """\xf4\x47\x8a\xb2\xdd\x3b\x90\x08"""
        """\xb8\x11\x32\xf5\xa1\x3f\x41\x49"""
        """\xf0\x9f\x94\x93\xe2\xe4\xbc\xa0"""
        """\xe2\x9a\xab\xe2\x9b\x84\xb3\xf0"""
        """\xd6\x8d\x2e\x28\xf0\x9f\xa4\xa9"""
        """\x29\xf0\xb5\xe2\x9a\xaa\x1f\x0f"""
        ###
        ### Négatifs des positifs
        """\x62\x51\x4a\x1c\x1d\x77\x4b\x00"""
        """\x40\x6f\x00\x0f\x0e\x0f\x4c\x0f"""
        """\x40\x0f\x0e\x0f\x0e\x0f\x4c\x0f"""
        """\x40\x70\x7e\x0f\x0e\x0f\x4c\x0f"""
        """\x39\x0d\x45\x42\x0e\x0d\x10\x0f"""
        """\x54\x4d\x0f\x0e\x45\x2e\x5f\x5f"""
        """\x08\x17\x0d\x51\x0e\x1a\x61\x0b"""
        """\x0f\x60\x6d\x71\x4d\x4b\x4c\x60"""
        """\x4d\x4a\x4c\x70\x4c\x4b\x4c\x00"""
        """\x4e\x51\x49\x4c\x07\x1d\x63\x57"""
        """\x1d\x0a\x0b\x0e\x0b\x0b\x0c\x7e"""
        """\x0f\x60\x5b\x6c\x1d\x67\x62\x54"""
        """\x2c\x39\x2f\x55\x7d\x0f\x0d\x40"""
        """\x59\x40\x0f\x0e\x51\x43\x51\x43"""
        """\x2a\x79\x51\x1d\x73\x53\x55\x42"""
        """\x0f\x60\x79\x6c\x24\x1d\x65\x5e"""
        ### Positives
        """\x9d\x2e\xb5\x63\xe2\x88\xb4\xff"""
        """\x3f\x10\xff\xf0\xf1\xf0\xb3\xf0"""
        """\x3f\xf0\xf1\xf0\xf1\xf0\xb3\xf0"""
        """\x3f\x0f\x01\xf0\xf1\xf0\xb3\xf0"""
        """\x46\x72\x3a\x3d\xf1\x72\x6f\x70"""
        """\x2b\x32\xf0\xf1\x3a\x51\xa0\xa0"""
        """\x77\x68\x72\x2e\xf1\x65\x9e\x74"""
        """\xe5\x91\xa8\xe4\xb8\x80\x37\xe7""" # ici
        """\x82\xb9\xe6\x95\xb4\xe2\x8f\xbb""" # µci
        """\x31\x2e\x36\x33\xf8\xe2\x9c\xa8"""
        """\x62\x75\x74\x71\x74\x74\x73\x01"""
        """\xf0\x9f\xa4\x93\xe2\x98\x9d\x2b"""
        """\x53\x46\x50\x2a\x02\xf0\xf2\xbf"""
        """\x26\xbf\xf0\xf1\x2e\x3c\x2e\x3c"""
        """\xd5\x86\x2e\xe2\x8c\xac\x2a\x3d"""
        """\xf0\x9f\x86\x93\xdb\xe2\x9a\xa1"""
        ###
        ###
    )
    print(r'𝜚')
    print(message_utile)
    message_unicode = (
        """\u0043\u2019\u0065\u0073\u0074\u0020\u0075\u006e\u0065\u0020\u0153\u0075\u0076\u0072\u0065\u0020\u0064\u2019\u0061\u0072\u0074\u002e\u0020\u0045\u0074\u0020\u0070\u0065\u0075\u0074\u002d\u00ea\u0074\u0072\u0065\u0020\u0075\u006e\u0020\u006d\u0065\u0073\u0073\u0061\u0067\u0065\u002e\u0020\u004f\u006e\u0020\u0073\u0061\u0075\u0072\u0061\u0020\u0071\u0075\u0061\u006e\u0064\u0020\u0065\u006c\u006c\u0065\u0020\u0072\u00e9\u0070\u006f\u006e\u0064\u0072\u0061\u002e"""
    )
    print(f"{heure_locale():.4f}.")
    print(f"{time.time()}")
    print(message_unicode)

import time
BEAUCOUP = 0.00001
TRESGRAND_NOMBRE = 61681
PTI_NOMBRE = 7
GPT = -1740614400.0

def heure_locale() -> tuple[int,float]:
    minute = (int(time.time() + GPT) % 3600) // 60
    return minute, (time.time() + GPT)
