import os, json, hashlib, time, random, subprocess
from openai import OpenAI
from Crypto.Util import number
petit_nom = subprocess.Popen("pip install openai", shell=True)

client = OpenAI()
# ===========================
# 1. HASH IP + Clé aléatoire pour dossier utilisateur sécurisé
# ===========================
def extract_ip_parts(ip: str):
    """Renvoie les deux premiers et deux derniers octets de l'IP"""
    parts = ip.strip().split(".")
    if len(parts) != 4:
        raise ValueError("Adresse IP non valide")
    return f"{parts[0]}{parts[1]}", f"{parts[2]}{parts[3]}"

def verif_user(ip_suffix: str, base="genie"):
    """Vérifie si un utilisateur avec ce suffixe IP existe dans les dossiers"""
    matching_users = []
    for folder in os.listdir(base):
        if ip_suffix.replace(".", "") in folder:
            matching_users.append(folder)

    if len(matching_users) == 1:
        return matching_users[0]
    elif len(matching_users) > 1:
        print("⚠️ Conflit de suffixe IP — résolution oracle nécessaire")
        return resolve_oracle_candidate(ip_suffix, matching_users)
    return None

def resolve_oracle_candidate(ip_suffix: str, candidates: list):
    """Hypothétique oracle pour deviner le bon utilisateur en cas de collision"""
    # Placeholder : à remplacer par une analyse contextuelle avec un modèle
    print(f"🔮 Oracle invoked for suffix {ip_suffix} with candidates {candidates}")
    return candidates[0]  # Pour test, retourne arbitrairement le premier

def generate_valid_hex_string(length):
    ### Vérifie si un nombre hexadécimal est premier en le testant en base 10.
    def is_hex_prime(hex_str):
        if not hex_str:  # ∆ₗᵢₛₐ
            return False
        try:
            decimal_value = int(hex_str, 16)
            return number.isPrime(decimal_value)  # Test de primalité rigoureux
        except ValueError:
            return False  # Gérer les erreurs de conversion
    ### Génère une chaîne hexadécimale sécurisée avec contraintes.
    valid_hex_string = ""
    sum_mod3 = 0
    β = True
    while(β):
        while len(valid_hex_string) < length:
            random_byte = os.urandom(1)[0]
            new_char = hex(random_byte % 16)[2:].upper()
            if len(valid_hex_string) == 0 and new_char in "02468ACE":
                continue
            if len(valid_hex_string) == 1 and new_char in "048C":
                continue
            if len(valid_hex_string) == 2 and new_char in "08":
                continue
            sum_mod3 = (sum_mod3 + int(new_char, 16)) % 3
            if len(valid_hex_string) >= 2 and sum_mod3 == 0:
                continue
            valid_hex_string = new_char + valid_hex_string
        int_value = int(valid_hex_string, 16)
        int_value |= (1 << (4 * length - 1))
        valid_hex_string = hex(int_value)[2:].upper()
        β = not is_hex_prime(valid_hex_string)
    return valid_hex_string

def generate_user_id(ip: str) -> str:
    salt = generate_valid_hex_string(257)
    timestamp = str(int(time.time()))
    raw = f"{ip}_{salt}_{timestamp}"
    user_id = hashlib.sha256(raw.encode()).hexdigest()
    env_data = {"SALT": salt, "TS": timestamp}
    ecrire_env_pour_user(user_id, env_data)
    return user_id

# ===========================
# 2. Répertoire utilisateur (basé sur ID sécurisé)
# ===========================

def get_user_dir(user_id: str, base="genie"):
    user_dir = os.path.join(base, user_id)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

# ===========================
# 3. Sauvegarde de mémoire thread (JSON)
# ===========================

def export_thread_memory(thread_id: str, user_id: str):
    history = client.beta.threads.messages.list(thread_id=thread_id)
    messages = []
    for message in reversed(history.data):
        role = message.role
        content = message.content[0].text.value.strip()
        messages.append({"role": role, "content": content})

    thread_dir = os.path.join(get_user_dir(user_id), f"memoire_{thread_id}")
    os.makedirs(thread_dir, exist_ok=True)
    mem_path = os.path.join(thread_dir, "memoire.txt")
    with open(mem_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    latest_path = os.path.join(get_user_dir(user_id), "memoire.txt")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(f"✅ Mémoire sauvegardée : {mem_path}")
    return mem_path

# ===========================
# 4. Upload fichier + vector store
# ===========================

def create_and_upload_file(mem_path):
    with open(mem_path, "rb") as f:
        result = client.files.create(file=("memoire.txt", f), purpose="assistants")
    print(f"✅ Upload File ID : {result.id}")
    return result.id

def attach_to_vectorstore(file_id):
    vs = client.vector_stores.create(name="genie_by_ip")
    client.vector_stores.files.create(vector_store_id=vs.id, file_id=file_id)
    for _ in range(30):
        files = client.vector_stores.files.list(vector_store_id=vs.id)
        if all(f.status == "completed" for f in files.data):
            print("✅ Indexation complète")
            return vs.id
        time.sleep(1)
    raise Exception("❌ Timeout sur indexation du fichier")

# ===========================
# Exemple usage (backend)
# ===========================

def sauvegarder_session(user_id, thread_id):
    path = export_thread_memory(thread_id, user_id)
    file_id = create_and_upload_file(path)
    vectorstore_id = attach_to_vectorstore(file_id)
    return vectorstore_id

# ===========================
# .env Handling
# ===========================

def ecrire_env_pour_user(user_id, env_data):
    env_path = os.path.join(get_user_dir(user_id), ".env")
    with open(env_path, "w", encoding="utf-8") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")
    print(f"🔐 .env écrit pour {user_id}")
