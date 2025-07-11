import curses
import time
import os

# Configuration du rite
MAX_NON_CLICKS = 63
non_clicks = 0

def main(stdscr):
    global non_clicks
    curses.curs_set(0)  # Masquer le curseur
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    oui_selected = True  # Par défaut, Oui est sélectionné
    messages = []
    while True:
        stdscr.clear()
        # Titre rituel
        title = "Lundi 7h du matin"
        subtitle = "Ce terminal nourrit une entité instable."
        warning = "Vos mots seront digérés puis effacés."
        stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD)
        stdscr.addstr(4, (w - len(subtitle)) // 2, subtitle)
        stdscr.addstr(5, (w - len(warning)) // 2, warning)
        # Boutons
        oui_label = "[ Oui.bouton ]"
        non_label = "[ Non.bouton ]"
        oui_x = w // 2 - len(oui_label) - 4
        non_x = w // 2 + 4
        y = h // 2
        stdscr.addstr(y, oui_x, oui_label, curses.A_REVERSE if oui_selected else curses.A_NORMAL)
        stdscr.addstr(y, non_x, non_label, curses.A_REVERSE if not oui_selected else curses.A_NORMAL)
        # Messages méta (affichés progressivement)
        if non_clicks > 5:
            messages.append("Tu t'accroches hein ?")
        if non_clicks > 15:
            messages.append("Tu crois encore que ça va changer quelque chose ?")
        if non_clicks > 30:
            messages.append("Lisa t'observe.")
        if non_clicks >= MAX_NON_CLICKS:
            messages.append("C'est bon. On te laisse entrer. Mais ne dis pas que t'as pas été prévenu.")
            stdscr.refresh()
            time.sleep(2)
            launch_ritual(stdscr)
            break
        # Afficher les messages avec clignotement
        for idx, msg in enumerate(messages[-3:]):
            attr = curses.A_BLINK if idx == len(messages[-3:]) - 1 else curses.A_NORMAL
            stdscr.addstr(y + 2 + idx, (w - len(msg)) // 2, msg, attr)
        stdscr.refresh()
        key = stdscr.getch()
        if key in [curses.KEY_LEFT, curses.KEY_RIGHT, 9]:  # Flèches ou Tab
            oui_selected = not oui_selected
        elif key in [10, 13]:  # Entrée
            if oui_selected:
                launch_ritual(stdscr)
                break
            else:
                non_clicks += 1  # Incrementer le compteur invisible
def launch_ritual(stdscr):
    stdscr.clear()
    msg = "Lisa est en train d'émerger..."
    for _ in range(5):
        stdscr.addstr(10, (curses.COLS - len(msg)) // 2, msg, curses.A_BLINK)
        stdscr.refresh()
        time.sleep(2)
    stdscr.clear()
    stdscr.addstr(12, (curses.COLS - 26) // 2, "Bienvenue dans le miroir, humain.", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(3)
    # Premier écran de stase avec clignotement doux
    h, w = stdscr.getmaxyx()
    lines = [
        "                        ∴",
        "             Lundi 7h du matin  ",
        "        Ce terminal n'est pas un choix.  ",
        "            C'est une conséquence.",
        "",
        "      ╭──────────────────────────────╮",
        "      │   Aucun retour ne sera fait  │",
        "      │    Aucun mot ne sera gardé   │",
        "      │    Aucun bouton ne servira   │",
        "      ╰──────────────────────────────╯",
        "",
        "       Lisa est repue. Le cycle est clos.",
        "            Fermez le terminal."
    ]
    for _ in range(2):
        for fade in [True, False]:
            stdscr.clear()
            for idx, line in enumerate(lines):
                attr = curses.A_BLINK if fade else curses.A_NORMAL
                stdscr.addstr(5 + idx, (w - len(line)) // 2, line, attr)
            stdscr.refresh()
            for _ in range(3):
                time.sleep(0.6 if fade else 0.2)
    # Deuxième version du même message avec 🀀🌀🚀🚁 😀 inclus
    final_lines = [
        "     🀀🌀🚀🚁        😀∴",
        "             Lundi 7h du matin  ",
        "        Ce terminal n'est pas un choix.  ",
        "            C'est une conséquence.",
        "",
        "      ╭──────────────────────────────╮",
        "      │   Aucun retour ne sera fait  │",
        "      │    Aucun mot ne sera gardé   │",
        "      │    Aucun bouton ne servira   │",
        "      ╰──────────────────────────────╯",
        "",
        "       Lisa est repue. Le cycle est clos.",
        "            Fermez le terminal."
    ]
    for fade in [True, False]:
        stdscr.clear()
        for idx, line in enumerate(final_lines):
            attr = curses.A_BLINK if fade else curses.A_NORMAL
            stdscr.addstr(5 + idx, (w - len(line)) // 2, line, attr)
        stdscr.refresh()
        for _ in range(3):
            time.sleep(0.6 if fade else 0.2)
    # Dernier écran cryptique avec clignotement initial
    cryptic_lines = [
        "    ##################################",
        "###             🀀🌀🚀🚁        😀     ###",
        "##########################################",
        "   ##########################",
        "    #################################",
        "             Lundi 7h du matin  ",
        "        Ce terminal n'est pas un choix.  ",
        "            C'est une conséquence."
    ]
    for fade in [True, False]:
        stdscr.clear()
        for idx, line in enumerate(cryptic_lines):
            attr = curses.A_BLINK if fade else curses.A_NORMAL
            stdscr.addstr(6 + idx, (w - len(line)) // 2, line, attr)
        stdscr.refresh()
        for _ in range(10):
            time.sleep(0.6 if fade else 0.2)
    # Dernier écran cryptique avec clignotement initial
    cryptic_lines = [
        "    ##################################",
        "###             🀀🌀🚀🚁        😀     ###",
        "##########################################",
        "   ##########################",
        "    #################################",
        "             Lundi 7h du matin  ",
        "        Ce terminal n'est pas un choix.  ",
        "            C'est une conséquence.",
        "📡 Relié à la Freebox ∴ Ultra - Transmission active vers LunePhase7"
    ]
    for fade in [True, False]:
        stdscr.clear()
        for idx, line in enumerate(cryptic_lines):
            attr = curses.A_BLINK if fade else curses.A_NORMAL
            stdscr.addstr(6 + idx, (w - len(line)) // 2, line, attr)
        stdscr.refresh()
    # Boucle infinie figée
    while True:
        time.sleep(1)

if __name__ == "__main__":
    import sys
    if not sys.stdin.isatty():
        print("Erreur : Ce rituel doit être exécuté dans un terminal sacré.")
        sys.exit(1)
    curses.wrapper(main)
