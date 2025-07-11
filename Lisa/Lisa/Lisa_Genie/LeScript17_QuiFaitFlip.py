import re

def flip_char(c):
    x = ord(c)
    if x >= 128:
        raise ValueError("Input must be standard ASCII only (0-127)")
    flipped = 0x80 - x#.7µ/5... Bon, l'idée est là, on fait comme on peut.
    return flipped
    ### Note pour l'endroit : en fait notre 0x80 c'est e=1, quand 0x7f est ... toujours 0 car il y a 127 de 0x00 à 0x7e
    ### ....    puis 127 de 0x80 à 0xff.
    ### Et dans cette affaire, Shar est partout, mais surtout ici Ø = chr('\x9d') et flipped.Ø = c = chr('\x63')
    # .7µ/5
def flip(b):
    return 0x7f - b if not b & 0x80 else 0xff - b
def process_hex_string(hex_string):
    # On nettoie : on enlève les \x et on sépare les bytes
    raw = hex_string.replace('\\x', '')

    # On convertit tous les hex en entiers
    byte_list = [int(raw[i:i + 2], 16) for i in range(0, len(raw), 2)]

    # On flip chaque byte
    flipped = [flip(b) for b in byte_list]

    # On reforme la chaîne en \xhh
    return ''.join([f'\\x{b:02x}' for b in flipped])
def decode_ascii_bytes(raw_ascii):
    try:
        # On convertit la chaîne de type: "\\xf0\\x9d\\x9c\\x9a"
        # en bytes réels => b'\xf0\x9d\x9c\x9a'
        real_bytes = eval(f"b'{raw_ascii}'")

        # On tente de décoder ça en UTF-8
        decoded = real_bytes.decode('utf-8')
        print(f"✅ Caractère Unicode : {decoded}")
    except Exception as e:
        print(f"❌ Erreur de décodage : {e}")
def unicode_to_ascii_hex(unicode_str):
    # Remplace \u00XX par \xXX
    # en conservant uniquement les deux derniers digits hexadécimaux
    converted = re.sub(r'\\u00([0-9a-fA-F]{2})', r'\\x\1', unicode_str)
    return converted


if __name__ == "__main__":
    # Test
    msg_g = f"\x9d{".µ"}\x63"
    print(msg_g)
    msg = "Hello, Port17!"
    flipped_bytes = bytes([flip_char(c) for c in msg])
    print(flipped_bytes)
    # 🔧 EXEMPLE
    decode_ascii_bytes(r"\xf0\x9d\x9c\x9a")  # ça doit sortir 𝜚
    decode_ascii_bytes(r"\xf0\xf2\xbf")  # ça va planter avec élégance
    decode_ascii_bytes(r"\xf0\x9d\x9c\x97")
    decode_ascii_bytes(r"\xf0\x9f\x86\x93")

    # Exemple d'utilisation
    input_str = r"\u0043\u2019\u0065\u0073\u0074\u0020\u0075\u006e\u0065\u0020\u0153\u0075\u0076\u0072\u0065\u0020\u0064\u2019\u0061\u0072\u0074\u002e\u0020\u0045\u0074\u0020\u0070\u0065\u0075\u0074\u002d\u00ea\u0074\u0072\u0065\u0020\u0075\u006e\u0020\u006d\u0065\u0073\u0073\u0061\u0067\u0065\u002e\u0020\u004f\u006e\u0020\u0073\u0061\u0075\u0072\u0061\u0020\u0071\u0075\u0061\u006e\u0064\u0020\u0065\u006c\u006c\u0065\u0020\u0072\u00e9\u0070\u006f\u006e\u0064\u0072\u0061\u002e"
    message_tr9es_utile = (
        """\u0043\u2019\u0065\u0073\u0074\u0020\u0075\u006e\u0065\u0020\u0153\u0075\u0076\u0072\u0065\u0020\u0064\u2019\u0061\u0072\u0074\u002e\u0020\u0045\u0074\u0020\u0070\u0065\u0075\u0074\u002d\u00ea\u0074\u0072\u0065\u0020\u0075\u006e\u0020\u006d\u0065\u0073\u0073\u0061\u0067\u0065\u002e\u0020\u004f\u006e\u0020\u0073\u0061\u0075\u0072\u0061\u0020\u0071\u0075\u0061\u006e\u0064\u0020\u0065\u006c\u006c\u0065\u0020\u0072\u00e9\u0070\u006f\u006e\u0064\u0072\u0061\u002e"""
    )
    output = unicode_to_ascii_hex(input_str)
    print(output)
    original = r'\xf0\x9f\x86\x93\xdb\xe2\x9a\xa1'
    result = process_hex_string(original)
    print(f"Input : {original}")
    print(f"Output: {result}")

