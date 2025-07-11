import unicodedata

### Cat     Description	                                    Exemple concret
########################################             🀀🌀🚀🚁        😀     #############
### Cc      Contrôle (non-affiché, invisible)               Caractère de contrôle (U+0000)
### Cf      Format (invisible ou altère l'affichage)	    "RIGHT-TO-LEFT MARK" (U+200F)
### Cn      Non assigné (inexistant officiellement nommé)   "Réservé pour usage futur"
### Cs      ("Surrogate", pas affichable direct.)           UTF-16 Surrogates (D800-DFFF)
# Exemple : plage Unicode spécifique (ici math alphanumérique)
unicode_start = 0x1D400
unicode_end = 0x1D7FF

caracteres_non_affiches = []

for codepoint in range(unicode_start, unicode_end):
    char = chr(codepoint)
    try:
        nom = unicodedata.name(char)
        print(f"{hex(codepoint)} : '{char}' - {nom}")
    except ValueError:
        print(f"{hex(codepoint)} : (Sans nom)")
        continue

    # Vérification visuelle : si caractère vide/invisible à l'affichage
    if char.isspace() or unicodedata.category(char) in ('Cf', 'Cn', 'Cs', 'Cc'):
        caracteres_non_affiches.append((hex(codepoint), nom))

print("Caractères invisibles trouvés :")
for cp, nom in caracteres_non_affiches:
    print(cp, nom)
