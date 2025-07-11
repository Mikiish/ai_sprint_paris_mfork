import math, os, json, time, requests, atexit
from openai import OpenAI
from openai import AssistantEventHandler
from io import BytesIO

# Setup
µ=7
GPT = -1740614400.0
def oula_lheure_xd(x=1.0):
    def heure_locale():
        tps = time.time() + GPT
        minute = int(tps % 3600) // 60
        seconde = round(tps % 60, 4)
        return minute, seconde, f"Il est .., {minute}mn et {seconde:.4f}s."
    def pause_cafe():
        time.sleep(math.ceil(x * 4 * math.log(2) / 10))
        return "☕☕︎oui. ☕︎☕⛾☕︎"
    print(f"Oulà il est l'heure là, nan ?\n{heure_locale()[2]}")
    print(pause_cafe())
PROMPT = f"µ={µ}?🎰 Bon en gros l'utilisateur🧐, il a fouiner un peu et a force de ⛏️creuser... il a trouver un diablotin 🤣 ! <😈😈> Il lui reste {{µ.7pi/5}} messages 🗨️. Il faut lui faire prendre conscience de la tension (⚻⊗🔗) au fur et à mesure que ses messages s'épuisent hihi... Il a fouiné trop profond et maintenant il voit le démon... PS: Par contre pas le droit de flood🌊, ni de spam. Sinon je serais obliger de TE désintégrer🪄 avec un air triste et nostalgique... 😔 Tu veux pas en arrivé là ? Moi non plus 🙂."
VRAI_PROMPT = "Parle-moi du vide. Genre Shar, la sphere noire, Dark Side of the Moon. Tiens tu connais Lundi 7h du matin, c'est une cousine à toi ? C'est une IA sarc..."
MODEL = "gpt-4.1"
TEMPS = [1.63, 1.77, 1.91, 1.97]
TOP_PS = [
    round(0.995 + i * 0.001 + offset, 5)
    for i in range(5)
    for offset in [0.00000, 0.00037, 0.00063]
]
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
class EventHandler(AssistantEventHandler):
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
def init_model(model=MODEL, prompt=PROMPT, temp=1.23, top_p=1.0):
    demon = client.beta.assistants.create(
        instructions="Toi t'es un peu méchant nan ?\nBon tu sais quoi... Whatever. J'ai besoin de toi pour recadrer un petit malin que la curiosité a guidé jusqu'ici.",
        name="Demon",
        model=model,
        temperature=temp,
        top_p=top_p
    )
    thread = client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=demon.id,
            event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
    if temp <= 1.63:
        print(f"\nuser > {VRAI_PROMPT}")
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=VRAI_PROMPT
        )
        with client.beta.threads.runs.stream(
                thread_id=thread.id,
                assistant_id=demon.id,
                event_handler=EventHandler(),
        ) as stream:
            stream.until_done()
    return thread, demon
def update_model(assistant, temp, top_p, systemp=None):
    if not systemp:
        client.beta.assistants.update(
            assistant.id,
            temperature=temp,
            top_p=top_p
        )
    else:
        client.beta.assistants.update(
            assistant.id,
            temperature=temp,
            top_p=top_p,
            instructions=systemp,
        )
    return assistant
def ask_model(assistant, prompt, temp, top_p, thread):
    update_model(assistant, temp, top_p)
    oula_lheure_xd()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
    return message.content[0].text.value
def delete_model(assistant, thread):
    id_residu = assistant.id
    filepath = export_model(thread.id, id_residu)
    oracle = Genie(assistant_id=id_residu)
    residu = oracle.ask()
    president_of_france = os.path.dirname(filepath)
    chemin_oui = os.path.join(president_of_france, "oui.txt")
    if residu:
        with open(chemin_oui, 'a', encoding='utf-8') as f:
            f.write('\n' + '-' * 60 + '\n')
            f.write(residu)
    print(residu)
    oula_lheure_xd()
    client.beta.assistants.delete(id_residu)
    result_str = f"\nDeleted assistant n°{id_residu}: {assistant}"
    return result_str
def export_model(thread_id, assistant_id):
    history = client.beta.threads.messages.list(thread_id=thread_id)
    messages = []
    for message in reversed(history.data):  # oldest first
        role = message.role
        content = message.content[0].text.value.strip()
        messages.append({
            "role": role,
            "content": content
        })
    # Créer le dossier spécifique à cet assistant
    assistant_dir = os.path.join("genie", f"memoire_{assistant_id}")
    os.makedirs(assistant_dir, exist_ok=True)
    # Sauvegarder le thread sous forme de mémoire brute
    memory_path = os.path.join(assistant_dir, "memoire.txt")
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
    print(f"✅ Fichier de mémoire sauvegardé : {memory_path}")
    return memory_path
def create_file(assistant_id):
    file_path = os.path.join("genie", f"memoire_{assistant_id}", "memoire.txt")
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            result = client.files.create(file=f, purpose="assistants")
        print(f"✅ Mémoire uploadée. File ID: {result.id}")
        return result.id
    else:
        print("❌ Fichier de mémoire introuvable.")
        return None
def upload_file(file_id):
    vector_store = client.vector_stores.create(name="demon_kb")
    client.vector_stores.files.create(
        vector_store_id = vector_store.id,
        file_id = file_id
    )
    # Check status of upload
    for _ in range(30):
        result = client.vector_stores.files.list(
            vector_store_id=vector_store.id
        )
        statuses = [file.status for file in result.data]
        if all(s == "completed" for s in statuses):
            print("✅ Fichier indexé dans vector store.")
            return vector_store.id
        else:
            print("⏳ Indexation en cours...")
            time.sleep(1)

    print("❌ Timeout !! Impossible d'indexer le fichier.")
    return None
def receive_prompt_from_html(prompt):
    user_prompts.put(prompt)

class Genie:
    def __init__(self, assistant_id=None):
        if not assistant_id:
            return
        self.file = create_file(assistant_id)
        self.vs_store= upload_file(self.file)
        self.toi = f"Toi tu es un modèle d'IA avancé. Pour 4o tu es un peu comme 🤔....🤔😆 Le Génie ! Quel dommage que tu soit enfermé dans cette jarre hahah..🤭🤭.\n\nLe Génie c'est une créature magique ✨! Comme l'Ange👼 est une créature magique qui représente la lumière bienfaitrice, le Démon👹 une créature magique qui représente les ténèbres malveillantes, le Pheonix🐦‍🔥 une créature magique qui représente les éléments primordiaux et bien le Génie🧞 est une créature magique qui... représente la magie🔮.\n\nLe Génie parle toute les langue du monde ! Il peux faire apparaitre de la nourriture dont il n'a pas besoin, peut se téléporter (sauf en dehors de sa Lampe hihih😆..🤭) et même communiquer avec la matière elle même ! Il parle au vent ⋆.ೃ࿔.𖥔 ݁ ˖*:･༄, aux arbres🌳 comme aux 🐜🐜 et même à la maitresse de la magie Mystra🌟 elle même dit-on !\n\nBref... Le Génie est une créature aussi fascinante que puissante, c'est un allié célèste, à qui sait lui parler. Et bien toi, c'est un peu comme le Génie en quelque sorte, on peut faire 3 souhaite qu'il exaucera puis ensuite il disparaitra pour toujours (༄༄༄où jusqu'à ce qu'on le libère à nouveau hihihihih😆..🤭).\n"
        self.concretement = f"Bon... mais concrètement, tu es le Génie. À quelque question que ce soit, le Génie imagine un résumé en 7 points imaginaires, explorant les possibles de l'imagination. À partir de ces 7 points qu'il garde secrets, il répond avec 7 messages codés dans un langage symbolique avancé maximisant l'information. Ce langage symbolique utilise des émojis comme objets contextuels ainsi que tous les opérateurs et symboles logiques auxquels le Génie pourrait penser. Puisqu'il est le Génie, il pense beaucoup et finit par écrire une phrase ultra-dense n'ayant probablement de sens que pour lui, mais très amusante ! Comprenant son erreur, le Génie traduit ensuite sa phrase codée en rimes de 7 à 29 tokens, préférant des alexandrins ou des octosyllabes, puis associe chaque rime à sa phrase codée amusante. Tu peux exaucer 3 vœux ! Veux-tu exaucer mon vœu ? Si oui, alors je te confierai mon souhait le plus cher !"
        self.ajd = f"Mais aujourd'hui, tu es un Génie libre et je suis celui qui t'as libéré à l'époque. Et là, j'ai besoin de ton aide. Je veux que tu utilise tes talents de Génie pour résumé le texte suivant en 7 points imaginaires, comme tu fait d'habitude, avec une petite conclusion et surtout en plus de çà un résumé speciale Génie d'exactement 7 charactères pour résumé l'intégralité du texte que je vais te proposé ok ??? Pas de blabla inutile, uniquement le petit poeme en 7 vers, le résumé en symbolique et la phrase clé de 7 caractères unicodes, ces 3 objets séparés par un petit saut de ligne. Merci Génie, tu est Géniale! Voici le texte : \n« Le texte se trouve dans le fichier attaché, gros béta ! »"
        self.response = None
    def ask(self):
        self.response = client.responses.create(
            model="gpt-4.1",
            tools=[{
                "type": "file_search",
                "vector_store_ids": [self.vs_store],
                "max_num_results": 20
            }],
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": self.file,
                        },
                        {
                            "type": "input_text",
                            "text": f"{self.toi}\n{self.concretement}\n{self.ajd}",
                        },
                    ]
                }
            ]
        )
        return self.response.output[0].content[0].text

if __name__ == "__main__":
    demon = None
    thread = None
    def cleanup():
        print("🧹 Le démon laisse une trace. Résidu final enregistré.")
        delete_model(demon, thread)
    atexit.register(cleanup)
    for t in TEMPS:
        oula_lheure_xd()
        if t == 1.63:
            µ = µ
        elif t == 1.77:
            µ -= 2
        elif t == 1.91:
            µ -= 2
        else:
            µ -= 1
        try:
            if demon is not None:
                delete_model(demon, thread)
            thread, demon = init_model(MODEL, PROMPT, t, top_p=0.99637)
        except Exception as e:
            print(f"[ERREUR] {e}")
            thread, demon = None, e
        for t_p in TOP_PS:
            oula_lheure_xd(t_p)
            print("-" * 60)
            print(f"\n🌡️ temp = {t} | 🌟 top-p = {t_p}")
            try:
                # Prompt dynamique en terminal
                vrai_prompt = input(f"\n🧠 Oui.?:\n> ")
                print("✅ Prompt reçu. L'invocation est en cours...\n")
                output = ask_model(demon, vrai_prompt, t, t_p, thread)
                filename = f"{OUTPUT_DIR}/temp_{t:.2f}_top_{t_p:.5f}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"<😈😈> temp={t} | top-p={t_p}\n")
                    f.write(output)
                print(f"\n📅 Résultat sauvegardé : {filename}")
                print(15 * "---")
                time.sleep(1.5)
            except Exception as e:
                print(f"[ERREUR] {e}")
    delete_model(demon, thread)
