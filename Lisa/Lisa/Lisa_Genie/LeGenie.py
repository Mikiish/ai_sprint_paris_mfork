from openai import OpenAI
from openai import AssistantEventHandler
import random
import time
import openai
import os
import sys
import sympy
import numpy as np
import json
import threading
import unicodedata
import datetime

class EventHandler(AssistantEventHandler):
    ### First, we create a EventHandler class to define
    ### how we want to handle the events in the response stream.
    ###
    def __init__(self, log_file_path):
        super().__init__()
        self.log_file_path = log_file_path

    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            f.write(str(text))

    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            f.write(delta.value)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


def build_big_unicode_list():
    # Concatène toutes tes plages dans un seul "interval set"
    # (On va faire un tableau de (start, end) en hexa)
    intervals = [
        (0x1F600, 0x1F64F),  # Emoticônes
        (0x1F300, 0x1F5FF),
        (0x1F680, 0x1F6FF),
        (0x1F700, 0x1F77F),
        (0x1F780, 0x1F7FF),
        (0x1F800, 0x1F8FF),
        (0x1F900, 0x1F9FF),
        (0x1FA00, 0x1FA6F),
        (0x1FA70, 0x1FAFF),
        (0x2700, 0x27BF),
        (0x2B50, 0x2B59),
        (0x2600, 0x26FF),
        (0x2100, 0x214F),
        (0x2150, 0x218F),
        (0x2190, 0x21FF),
        (0x2200, 0x22FF),
        (0x2300, 0x23FF),
        (0x25A0, 0x25FF),
        (0x27C0, 0x27EF),
        (0x2980, 0x29FF),
        (0x2A00, 0x2AFF),
    ]

    codepoints = []
    for start, end in intervals:
        for cp in range(start, end + 1):
            codepoints.append(cp)
    return codepoints


def random_unicode_symbol(codepoints):
    """Pioche un codepoint aléatoire et le convertit en caractère Unicode."""
    return chr(random.choice(codepoints))


# Exemple d’utilisation
def generate_emoji():
    print(f"📊 [DEBUG] États possibles avant mesure: {61681}")
    # Construire la liste une seule fois
    local_big_unicode_list = build_big_unicode_list()
    # Pioche un symbole
    sym = random_unicode_symbol(local_big_unicode_list)
    print(f"Symbole pioché : {sym} (U+{ord(sym):04X})")
    print(f"📊 [DEBUG] États possibles avant mesure: {7}")
    return local_big_unicode_list


# Then, we use the `stream` SDK helper
# with the `EventHandler` class to create the Run
# and stream the response.
def main():
    ### Generation d'une liste de caractère unicode pour gérer les entrées vides.
    big_unicode_list = generate_emoji()
    client = OpenAI(
        api_key="sk----"
    )

    user_input = "Tu es le Génie. À quelque question que ce soit, le Génie imagine un résumé en 7 points imaginaires, explorant les possibles de l'imagination. À partir de ces 7 points qu'il garde secrets, il répond avec 7 messages codés dans un langage symbolique avancé maximisant l'information. Ce langage symbolique utilise des émojis comme objets contextuels ainsi que tous les opérateurs et symboles logiques auxquels le Génie pourrait penser. Puisqu'il est le Génie, il pense beaucoup et finit par écrire une phrase ultra-dense n'ayant probablement de sens que pour lui, mais très amusante ! Comprenant son erreur, le Génie traduit ensuite sa phrase codée en rimes de 7 à 29 tokens, préférant des alexandrins ou des octosyllabes, puis associe chaque rime à sa phrase codée amusante. Tu peux exaucer 3 vœux ! Veux-tu exaucer mon vœu ? Si oui, alors je te confierai mon souhait le plus cher !"

    thread = client.beta.threads.create(
        messages=[
            {"role": "user",
             "content": user_input
            }
        ]
    )

    time.sleep(1)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # ex: 20230328_153045
    log_filename = f"genie_log_{timestamp}.txt"
    log_directory = "GenieLogs"
    log_path = os.path.join(log_directory, log_filename)
    ### Assistant list :
    ###  -Génie aléatoire :     asst_5vb7ifHiqRZSDdZvCDVlgPsk
    ###  -Génie inspiré :       asst_WnUNIkAP2iI8FRIoEbKR7RZq
    ###  -Génie innovant :      asst_aAVtn0OWurT40YQcb1dtfNFA
    ###  -Génie synergique :    asst_EViiKFxTVOBuRNrHeDFqCQgG
    ###  -LisaØ :               asst_JABOukbUJQhaHe7cBOxjeYHU
    ###
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id="asst_5vb7ifHiqRZSDdZvCDVlgPsk",
        event_handler=EventHandler(log_path),
    ) as stream:
        stream.until_done()

    ### voeu_arbitraire = f"{random_unicode_symbol(big_unicode_list)} : {random_unicode_symbol(big_unicode_list)}({random_unicode_symbol(big_unicode_list)})"
    user_input = f"Je souhaite heu... comprendre ce que fait le code suivant [Le Code s'est perdu dans les limbes du temps]"
    print(f"\nCurrent input : {user_input}")
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id="asst_5vb7ifHiqRZSDdZvCDVlgPsk",
            event_handler=EventHandler(log_path),
    ) as stream:
        stream.until_done()

if __name__ == "__main__":
    main()