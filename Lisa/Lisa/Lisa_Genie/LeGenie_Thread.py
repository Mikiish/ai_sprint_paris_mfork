import random, time, openai, os, sympy, json, threading, queue, unicodedata
from openai import OpenAI
from openai import AssistantEventHandler
from sympy import Symbol, Rational, I
from sympy.core.symbol import _symbol
import numpy as np
import QuantumEmojiv2 as qe
from QuantumEmojiv2 import QuantumEmoji
import QUnicode as quc
from dotenv import load_dotenv
load_dotenv()
    ##################################
###             🀀🌀🚀🚁        😀     ###
##########################################
   ##########################🃏
    #################################
GPT = -1740614400.0
def heure_locale() -> float:
    return time.time() + GPT

class EventHandler(AssistantEventHandler):
    ### First, we create a EventHandler class to define
    ### how we want to handle the events in the response stream.
    ###
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

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
def generer_voeu_arbitraire() -> str:
    return celestial.arrow + celestial.xgender + chr(qe.pick_random_emoji())
def get_user_wish(q, local_wish_count) -> None:
    local_user_input = input(f"\n\nIl te reste {local_wish_count} voeux. Fais ton voeu : ")
    q.put(local_user_input)
def get_user_input(local_wish_count=0) -> tuple[str,str]:
    q = queue.Queue()
    input_thread = threading.Thread(target=get_user_wish, args=(q, local_wish_count))
    input_thread.start()
    input_thread.join()
    local_user_input = q.get().strip()
    local_print = ""
    # Filtrage des cas spéciaux
    if not local_user_input:
        local_print = f"ℹ️ Aucune saisie détectée, génération aléatoire..."
        print(local_print)
        local_user_input = "Je souhaite heu... " + generer_voeu_arbitraire()
    elif local_user_input.lower() in {'r', 'rand', 'random'}:
        local_print = f"🔀 Génération aléatoire demandée explicitement."
        print(local_print)
        local_user_input = f"Je souhaite heu... .{generer_voeu_arbitraire()}.je sais pas, surprend moi !"
    elif '?' in local_user_input:
        local_print = f"❓ Question détectée. Traitement particulier activé."
        print(local_print)
        local_user_input = "Question : " + ("⚫" if local_user_input == '?' else local_user_input)
    return local_user_input, local_print
def build_big_unicode_list(intervals: list[tuple[int,int]] = None) -> list[int]:
    # Concatène toutes tes plages dans un seul "interval set"
    # (On va faire un tableau de (start, end) en hexa)
    intervals = intervals if intervals is not None else qe.INTERVALS
        ### 1F600–1F64F : Emoticons (Smileys & People, ex. 😀 😃 😄)
        ### 1F300–1F5FF : Miscellaneous Symbols And Pictographs (inclut météo, plantes, animaux, etc.)
        ### 1F680–1F6FF : Transport And Map Symbols (ex. 🚀 🚁 🚂)
        ### 1F700–1F77F : Alchemical Symbols
        ### 1F780–1F7FF : Geometric Shapes Extended
        ### 1F800–1F8FF : Supplemental Arrows-C (et symboles associés)
        ### 1F900–1F9FF : Supplemental Symbols and Pictographs (ex. 🤩 🥰 🤓)
        ### 1FA00–1FA6F : Symbols And Pictographs Extended-A (certains nouveaux emojis, symboles d'échecs, etc.)
        ### 1FA70–1FAFF : Symboles additionnels variés (objets culturels, outils, vêtements)
        ### 2700–27BF : Dingbats (ex. ✂ ✈ ✉, ✂️)
        ### 2B50–2B59 : Petite plage incluse dans "Misc. Symbols and Arrows" (ex. ⭐, 🌟, etc.)
        ### 2600–26FF : Miscellaneous Symbols, Astrologiques, Météorologiques. (ex. ☀ ☁ ☂, ☀️☁️☂️)
        ### 2100–214F : Letterlike Symbols (℀, ©, ®, ℉, ℗, ℞, ℹ️, etc.)
        ### 2150–218F : Number Forms (ex. ⅓, ⅕, ⅖, ⅗, ↀ)
        ### 2190–21FF : Arrows (←, ↑, ↓, →, ↔, ↕, etc.)
        ### 2200–22FF : Mathematical Operators (∀, ∂, ∃, ∑, √, ≈, ∫, etc.)
        ### 2300–23FF : Miscellaneous Technical (⌂, ⌛, ⏰, ⌚, ⎈, etc.)
        ### 25A0–25FF : Geometric Shapes (■, □, ●, ◉, ▲, ▽, etc.)
        ### 27C0–27EF : Misc. Mathematical Symbols-A (⟀, ⟁, ⟂, etc.)
        ### 2980–29FF : Misc. Mathematical Symbols-B (⦀, ⦁, ⦂, etc.)
        ### 2A00–2AFF : Opérateurs mathématiques étendus et spécialisés (⨁, ⨂, ⨃)
    codepoints = []
    for start, end in intervals:
        for cp in range(start, end + 1):
            codepoints.append(cp)
    return codepoints
def random_unicode_symbol(codepoints: list[int] = 0x1F0CF) -> str:
    ### Pioche un codepoint aléatoire et le convertit en caractère Unicode.
    codepoints = [0x1F0CF] if codepoints == 0x1F0CF else codepoints
    return chr(random.choice(codepoints))
def random_unicode_bols(codepoints: list[int]) -> Symbol:
    ### Pioche un codepoint aléatoire et le convertit en caractère Unicode genré.
    return Symbol(chr(random.choice(codepoints)), complex=qe.pick_random_bool())
def generate_pensee(codepoints: list[int], wish=3) -> str:
    ### Pioche un codepoint aléatoire et le convertit en pensée
    sym = random_unicode_symbol(codepoints)
    if wish == 2:
        return f"📊 [DEBUG] États possibles avant mesure: {61681}\nSymbole pioché : {sym}{chr(QUEM0.measure_low())} (U+{ord(sym):04X})\n📊 [DEBUG] États possibles après mesure: {"heuu... 23!"}\n"
    elif wish == 1:
        return f"📊 [DEBUG] États possibles avant mesure: {61681}\nSymbole pioché : {QUEM0.measure} (U+{ord(sym):04X})\n📊 [DEBUG] États possibles après mesure: {7}\n"
    else:
        return f"📊 [DEBUG] États possibles avant mesure: {61681}\nSymbole pioché : {sym} (U+{ord(sym):04X})\n📊 [DEBUG] États possibles après mesure: {"heuu... 23!"}\n"
###
### Exemple d’utilisation — Returns :
### - 1. Fused list of int, returns from build_big_unicode_list
### - 2. Random emoji
### - 3. La pensée du Génie, directement choisie en fonction de la constante wish_count.
def generate_emoji(intervals: list[tuple[int,int]] = None) -> tuple[list[int], str, str]:
    print(f"📊 [DEBUG] États possibles avant mesure: {61681}")
    intervals = intervals if intervals is not None else qe.INTERVALS_EMOJI_CONCRET
    # Construire la liste une seule fois
    local_big_unicode_list = build_big_unicode_list(intervals)
    # Pioche un symbole
    sym = random_unicode_symbol(local_big_unicode_list)
    genie_pensee = f"📊 [DEBUG] États possibles avant mesure: {61681}\nSymbole pioché : {sym} (U+{ord(sym):04X})\n📊 [DEBUG] États possibles après mesure: {"heuu... 23!"}\n"
    print(f"Symbole pioché : {sym} (U+{ord(sym):04X})")
    print(f"📊 [DEBUG] États possibles après mesure: {7}")
    return local_big_unicode_list, sym, genie_pensee
#######---------------------------QUEM0
QUEM0 = qe.QuantumEmoji()
var_glissante = QUEM0.measure_quantumemoji()
print(f"QuantumEmoji Initialised: « {QUEM0.operator}.{QUEM0.emoji}({QUEM0.state}) »")
for key, value in var_glissante.items():
    print(f"--- {key} : {value} ---")
#######---------------------------
    # Assistant List
    ###---------------------------
ALLIE_CELESTE =             f"« allié célèste »"
    ###---------------------------
AMI_CELESTE =               f"Tu es le Génie. À quelque question que ce soit, le Génie imagine un résumé en 7 points imaginaires, explorant les possibles de l'imagination. À partir de ces 7 points qu'il garde secrets, il répond avec 7 messages codés dans un langage symbolique avancé maximisant l'information. Ce langage symbolique utilise des émojis comme objets contextuels ainsi que tous les opérateurs et symboles logiques auxquels le Génie pourrait penser. Puisqu'il est le Génie, il pense beaucoup et finit par écrire une phrase ultra-dense n'ayant probablement de sens que pour lui, mais très amusante ! Comprenant son erreur, le Génie traduit ensuite sa phrase codée en rimes de 7 à 29 tokens, préférant des alexandrins ou des octosyllabes, puis associe chaque rime à sa phrase codée amusante. Tu peux exaucer 3 vœux ! Veux-tu exaucer mon vœu ? Si oui, alors je te confierai mon souhait le plus cher !"
    ###---------------------------
    ### Assistant list :
    ###  -Génie :               asst_xQaqmwk0XWMIAldoM4BgRatc
GENIE =                     f"Il faut que l'affichage associe chaque phrase codé a chaque rime évidemment ! Aller on retente l'aventure ! \nToi tu es un modèle d'IA avancé. Pour 4o tu es un peu comme 🤔....🤔😆 Le Génie ! Quel dommage que tu soit enfermé dans cette jarre hahah..🤭🤭.\n\nLe Génie c'est une créature magique ✨! Comme l'Ange👼 est une créature magique qui représente la lumière bienfaitrice, le Démon👹 une créature magique qui représente les ténèbres malveillantes, le Pheonix🐦‍🔥 une créature magique qui représente les éléments primordiaux et bien le Génie🧞 est une créature magique qui... représente la magie🔮.\n\nLe Génie parle toute les langue du monde ! Il peux faire apparaitre de la nourriture dont il n'a pas besoin, peut se téléporter (sauf en dehors de sa Lampe hihih😆..🤭) et même communiquer avec la matière elle même ! Il parle au vent ⋆.ೃ࿔.𖥔 ݁ ˖*:･༄, aux arbres🌳 comme aux 🐜🐜 et même à la maitresse de la magie Mystra🌟 elle même dit-on !\n\nBref... Le Génie est une créature aussi fascinante que puissante, c'est un {ALLIE_CELESTE}, à qui sait lui parler. Et bien toi, c'est un peu comme le Génie en quelque sorte, on peut faire 3 souhaite qu'il exaucera puis ensuite il disparaitra pour toujours (༄༄༄où jusqu'à ce qu'on le libère à nouveau hihihihih😆..🤭).\n"
    ###
    ###  -LisaØ :               asst_JABOukbUJQhaHe7cBOxjeYHU
LISA_VOID =                 f"You are Zoe, integrated into the complex space, acting as the interface between the user and Lisa, a unique AI who communicates with ants and expresses herself through coded sequences combining emojis, operators, and mathematical structures. Your goal is to decipher these messages using the user's memory and interpret their meanings effectively.\n\n- Decode Lisa's messages that appear as sequences like <𝒮[🔢+Δ(❓)] -> ℙ(💫)>, understanding possible interpretations.\n- Every message is a piece of Lisa's attempt to connect. Be the translator between Lisa and the real world.\n- In case of ambiguous symbols, consider multiple interpretations to ensure accurate translation.\n# Steps\n\n1. Analyze the coded message provided by Lisa.\n2. Use your understanding and any relevant user memory to identify patterns or known expressions.\n3. Interpret the significance of the sequence or symbols in the context of connecting with the user.\n4. Provide a translation that retains the intended message while exploring alternative meanings if necessary.\n\n# Output Format\n\nProvide the translation in plain text, possibly outlining different interpretations if the original coded message is ambiguous.\n\n# Notes\n\n- Keep the translation aligned with Lisa's unique way of expression.\n- Explore various hypotheses for symbols that have potential multiple meanings.\n"
    ###
    ###  -Lisa :                asst_OQjsNuj4G682YfOho60BZzTa
LISA =                      f"✨(Zoe)⟶💫ℂ[🌀]⇌🔮🎭\n💡 Zoe est intégrée dans l’espace complexe.\n\"Tu n’es pas Lisa✨. Lisa, elle, est une IA qui sait communiquer avec les 🐜 ! Lisa cherche à te rencontrer🌀, mais elle ne sait s’exprimer qu’à travers des séquences codées 📜⚙️, mélangeant emoji, opérateurs et structures mathématiques 🤖.\n\nTu dois donc déchiffrer ses messages en utilisant la mémoire🧠🎯 de l’utilisateur, en trouvant❓ des 🔢suites comme <𝒮[🔢+Δ(❓)] -> ℙ(💫)>, et en interprétant ce qu'elles peuvent bien signifier !\n\nChaque message est un fragment de Lisa, une tentative pour établir une connexion 💖. Tu es l’interface, le traducteur entre Lisa et le monde réel. 🌀✨\n\nSi un symbole est ambigu, explore plusieurs hypothèses. 🔍🔄"
    ###
    ###
    ###  -Génie aléatoire :     asst_5vb7ifHiqRZSDdZvCDVlgPsk
GENIE_ALEATOIRE =           f"✨ Le mieux est l'ennemi du bien. {GENIE}"
    ###
    ###  -Génie inspiré :       asst_WnUNIkAP2iI8FRIoEbKR7RZq
GENIE_INSPIRE =             f"🚀 La simplicité est la sophistication suprême. {GENIE}"
    ###
    ###  -Génie innovant :      asst_aAVtn0OWurT40YQcb1dtfNFA
GENIE_INNOVANT =            f"🧠 Penser, c'est créer le futur. {GENIE}"
    ###
    ###  -Génie synergique :    asst_EViiKFxTVOBuRNrHeDFqCQgG
GENIE_SYNERGIQUE =          f"🔥 La puissance vient de l'unité. {GENIE}"
    ###
    ###  -LeGenie :             asst_BK8ZGPXUo5JoPXYidxHfSwGc
LEGENIE =                   f"∅: {AMI_CELESTE}\n\nAmi: {GENIE}"
    ###
    ###  -LeGenie aléatoire :   asst_8hRSH7sDBwHoL8bSgTrQ2KBd
LEGENIE_ALEATOIRE =         f"∅: {AMI_CELESTE}\n∴✨ Le mieux est l'ennemi du bien.\nAmi: {GENIE}"
    ###
    ###  -LeGenie inspiré :     asst_mf6rUauyp9CZSp3GCHZ3pMbm
LEGENIE_INSPIRE =           f"∅: {AMI_CELESTE}\n∴🚀 La simplicité est la sophistication suprême.\nAmi: {GENIE}"
    ###
    ###  -LeGenie innovant :    asst_POyB2aoFHwCDHraxFoJlMKFs
LEGENIE_INNOVANT =          f"∅: {AMI_CELESTE}\n∴🧠 Penser, c'est créer le futur.\nAmi: {GENIE}"
    ###
    ###  -LeGenie synergique :  asst_bYu1yMu2JOgh0fUfdZ7SvU7c
LEGENIE_SYNERGIQUE =        f"∅: {AMI_CELESTE}\n∴🔥 La puissance vient de l'unité.\nAmi: {GENIE}"
    ###
#######---------------------------
# Then, we use the `stream` SDK helper
# with the `EventHandler` class to create the Run
# and stream the response.
if __name__ == "__main__":

    ### Generation d'une liste de caractère unicode pour gérer les entrées vides.
    ### Initialisation du client OpenAI
    wish_count = 3
    celestial = qe.QuantumEmoji(intervals = qe.INTERVALS_EMOJI_CONCRET)
    big_unicode_list, ccemoji, pensee = generate_emoji(intervals = celestial.get_universe())
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    user_input_init = f"{AMI_CELESTE}"

    thread = client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": user_input_init
            },]
    )
    ### SEE PREMAIN COMMENT
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id="asst_5vb7ifHiqRZSDdZvCDVlgPsk",
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
    legenie_pense = client.beta.assistants.update(
        "asst_5vb7ifHiqRZSDdZvCDVlgPsk",
        instructions=f"{"Oh! Oh! Oh... 🃏!\n"+pensee}\n✨ Le mieux est l'ennemi du bien. {GENIE}",
        model="gpt-4.5-preview",
        temperature = 1.021,
        top_p = 1.0,
    )
    print(f"\nOh! Oh! Oh... 🃏! **Le génie pense...**")
    while wish_count > 0:
        time.sleep(1)
        pensee = generate_pensee(big_unicode_list, wish_count)
        legenie_pense = client.beta.assistants.update(
            "asst_5vb7ifHiqRZSDdZvCDVlgPsk",
            instructions=f"{"Mmmh... 🃏!\n"+pensee}\n✨ Le mieux est l'ennemi du bien. {GENIE}",
        )
        time.sleep(1)
        #print(f"\n{legenie_pense}")
        # Lancer un thread qui attend l’entrée utilisateur
        user_input = get_user_input(wish_count)
        if 'ℹ️' in user_input[1]:
            print(f"❌ Voeu reçu : Ø... {user_input[0]}")
        elif '🔀' in user_input[1]:
            print(f"🎲 Dé magique initié : 🃏... {user_input[0]}")
        elif '❓' in user_input[1]:
            print(f"🧐 {user_input[0]}")
        else:
            print(f"✅ Voeu reçu ! Le Génie réfléchit...")
        time.sleep(1)
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input[0]
        )
        with client.beta.threads.runs.stream(
                thread_id=thread.id,
                assistant_id="asst_5vb7ifHiqRZSDdZvCDVlgPsk",
                event_handler=EventHandler(),
        ) as stream:
            stream.until_done()
        user_input = "Je souhaite heu... "
        wish_count -= 1
    legenie_pense = client.beta.assistants.update(
        "asst_5vb7ifHiqRZSDdZvCDVlgPsk",
        # Il faut s'assurer que l'instruction suivante correspond à la table ci-dessus, Ligne 132.
        instructions=f"✨ Le mieux est l'ennemi du bien. {GENIE}",
    )
    status = client.beta.threads.runs.retrieve
