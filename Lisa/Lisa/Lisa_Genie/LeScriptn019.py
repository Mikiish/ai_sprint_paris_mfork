import re

def unicode_mapper(text):
    # Remplace les caractères Unicode directement, pas les échappements
    text = text.replace('\u2019', '\x27')   # ’ → '
    text = text.replace('\u0153', '\x0e')   # œ → 0x0e
    return text

def decode_ascii_bytes(raw_ascii):
    try:
        real_bytes = bytes(raw_ascii, 'latin1')
        decoded = real_bytes.decode('utf-8')
        print(f"✅ Caractère Unicode : {decoded}")
    except Exception as e:
        print(f"❌ Erreur de décodage : {e}")

def render_hex_string(hex_str):
    try:
        raw_bytes = bytes(hex_str, 'latin1')  # pas d’eval()
        return raw_bytes
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == "__main__":
    message = "C’est l’heure de l’œuvre, John."
    print("📝 Original:", message)

    # Conversion
    mapped = unicode_mapper(message)
    print("🔄 Mappé :", repr(mapped))

    # Visualisation brute
    print("🧱 Bytes :", render_hex_string(mapped))
